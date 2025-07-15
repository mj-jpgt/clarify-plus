#!/usr/bin/env python3
"""
Clarify+ EquiCheck Module

This module analyzes text for readability metrics (SMOG & Gunning-Fog)
and performs Cultural Tailoring Score (CTS) keyword analysis.
"""

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional

import textstat
from .scraper import Scraper


class EquiCheck:
    """
    Analyze text for readability and cultural equity factors.
    
    This class implements the EquiCheck engine, which calculates:
    1. Readability scores (SMOG & Gunning-Fog)
    2. Cultural Tailoring Score (CTS) keyword frequency
    """

    def __init__(self, 
                cts_keywords_path: Optional[str] = None,
                verbose: bool = False):
        """
        Initialize the EquiCheck analyzer.
        
        Args:
            cts_keywords_path: Path to CSV file with CTS keywords
            verbose: Whether to print detailed information
        """
        self.verbose = verbose
        self.cts_keywords = {}
        
        if cts_keywords_path:
            self.load_cts_keywords(cts_keywords_path)
        else:
            default_path = Path(__file__).parent / "cts_keywords.csv"
            if default_path.exists():
                self.load_cts_keywords(str(default_path))
            elif self.verbose:
                print("Warning: Default CTS keywords file not found. No CTS analysis will be performed.")
                
        if self.verbose:
            print(f"Initialized EquiCheck with {len(self.cts_keywords)} CTS keywords")

    def load_cts_keywords(self, file_path: str) -> None:
        """
        Load CTS keywords from a CSV file.
        Expected format: keyword,category,weight
        """
        if not os.path.exists(file_path):
            if self.verbose:
                print(f"Warning: CTS keywords file not found at {file_path}")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'keyword' in row and 'category' in row:
                        keyword = row['keyword'].lower().strip()
                        category = row['category'].strip()
                        weight = float(row.get('weight', 1.0))
                        
                        self.cts_keywords[keyword] = {
                            'category': category,
                            'weight': weight
                        }
            if self.verbose:
                print(f"Loaded {len(self.cts_keywords)} CTS keywords from {file_path}")
        except Exception as e:
            print(f"Error loading CTS keywords: {e}")

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text for readability and CTS keywords.
        """
        if not text:
            if self.verbose:
                print("Warning: Empty text provided for analysis")
            return {
                "readability": {},
                "cts_keywords": {}
            }
            
        readability = self._calculate_readability(text)
        cts_analysis = self._find_cts_keywords(text)
        
        return {
            "readability": readability,
            "cts_keywords": cts_analysis
        }

    def run(self, text: str) -> Dict:
        """
        Run the full analysis on the given text.
        """
        if self.verbose:
            print(f"Analyzing text ({len(text)} characters)...")
        
        results = self.analyze_text(text)
        
        if self.verbose:
            print("Analysis complete.")
            
        return results

    def _calculate_readability(self, text: str) -> Dict:
        """
        Calculate readability metrics for the given text.
        """
        try:
            smog = textstat.smog_index(text)
            gunning_fog = textstat.gunning_fog(text)
            flesch_kincaid = textstat.flesch_kincaid_grade(text)
            average_grade_level = (smog + gunning_fog + flesch_kincaid) / 3
            
            return {
                "smog_index": round(smog, 2),
                "gunning_fog": round(gunning_fog, 2),
                "flesch_kincaid_grade": round(flesch_kincaid, 2),
                "average_grade_level": round(average_grade_level, 2)
            }
        except Exception as e:
            if self.verbose:
                print(f"Could not calculate readability: {e}")
            return {}

    def _find_cts_keywords(self, text: str) -> Dict:
        """
        Find CTS keywords in the text and analyze their frequency.
        """
        if not self.cts_keywords:
            return {
                "total_matches": 0,
                "matches_by_category": {},
                "matched_keywords": []
            }
            
        text_lower = text.lower()
        matches = []
        for keyword, info in self.cts_keywords.items():
            pattern = r'\b' + re.escape(keyword) + r'\b'
            count = len(re.findall(pattern, text_lower))
            
            if count > 0:
                matches.append({
                    "keyword": keyword,
                    "category": info['category'],
                    "count": count,
                    "weight": info['weight']
                })
        
        categories = {}
        for match in matches:
            category = match['category']
            if category not in categories:
                categories[category] = {
                    "count": 0,
                    "weighted_count": 0
                }
            categories[category]["count"] += match['count']
            categories[category]["weighted_count"] += match['count'] * match['weight']
        
        return {
            "total_matches": sum(match['count'] for match in matches),
            "matches_by_category": categories,
            "matched_keywords": matches
        }

def main():
    """Main function to run the EquiCheck from the command line."""
    parser = argparse.ArgumentParser(
        description="Analyze text for readability and cultural equity factors."
    )
    parser.add_argument(
        "source",
        help="Path to a text file, PDF file, or a URL to be analyzed."
    )
    parser.add_argument(
        "-k", "--keywords",
        dest="cts_keywords_path",
        help="Path to a custom CTS keywords CSV file."
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_path",
        type=Path,
        default=Path("output/equicheck_results.json"),
        help="Path to save the output JSON file."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )
    args = parser.parse_args()

    equicheck = EquiCheck(cts_keywords_path=args.cts_keywords_path, verbose=args.verbose)

    text_to_analyze = ""
    if args.source.startswith(('http', 'https')) or args.source.lower().endswith('.pdf'):
        if args.verbose:
            print(f"Source is a URL or PDF. Running scraper...")
        scraper = Scraper(verbose=args.verbose)
        scraped_output_path = args.output_path.parent / "scraped_content.json"
        scraper.run(args.source, scraped_output_path)
        with open(scraped_output_path, 'r', encoding='utf-8') as f:
            scraped_data = json.load(f)
        text_to_analyze = scraped_data.get('text', '')
    elif args.source.lower().endswith(('.txt', '.json')):
        if args.verbose:
            print(f"Source is a text or JSON file. Reading content...")
        with open(args.source, 'r', encoding='utf-8') as f:
            if args.source.lower().endswith('.json'):
                text_to_analyze = json.load(f).get('text', '')
            else:
                text_to_analyze = f.read()
    else:
        print(f"Error: Unsupported source type for '{args.source}'. Please provide a URL, or a path to a .pdf, .txt, or .json file.")
        sys.exit(1)

    if not text_to_analyze:
        print("Error: Could not extract text from the source.")
        sys.exit(1)

    results = equicheck.run(text_to_analyze)

    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

    if args.verbose:
        print(f"EquiCheck analysis complete. Results saved to {args.output_path}")

if __name__ == "__main__":
    main()
