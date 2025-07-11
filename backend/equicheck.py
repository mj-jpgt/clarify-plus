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
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional

import textstat
from scraper import Scraper


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
        
        # Load CTS keywords if path is provided
        if cts_keywords_path:
            self.load_cts_keywords(cts_keywords_path)
        else:
            # Try to find cts_keywords.csv in the same directory as this file
            default_path = os.path.join(os.path.dirname(__file__), "cts_keywords.csv")
            if os.path.exists(default_path):
                self.load_cts_keywords(default_path)
                
        if self.verbose:
            print(f"Initialized EquiCheck with {len(self.cts_keywords)} CTS keywords")

    def load_cts_keywords(self, file_path: str) -> None:
        """
        Load CTS keywords from a CSV file.
        
        Expected format: keyword,category,weight
        
        Args:
            file_path: Path to CSV file with CTS keywords
        """
        if not os.path.exists(file_path):
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
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with analysis results
        """
        if not text:
            print("Warning: Empty text provided for analysis")
            return {
                "readability": {
                    "smog_index": None,
                    "gunning_fog": None,
                    "flesch_kincaid_grade": None,
                    "average_grade_level": None
                },
                "cts_keywords": {
                    "total_matches": 0,
                    "matches_by_category": {},
                    "matched_keywords": []
                }
            }
            
        # Calculate readability metrics
        readability = self._calculate_readability(text)
        
        # Find CTS keywords
        cts_analysis = self._find_cts_keywords(text)
        
        return {
            "readability": readability,
            "cts_keywords": cts_analysis
        }

    def _calculate_readability(self, text: str) -> Dict:
        """
        Calculate readability metrics for the given text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with readability scores
        """
        # Calculate SMOG index
        smog = textstat.smog_index(text)
        
        # Calculate Gunning Fog index
        gunning_fog = textstat.gunning_fog(text)
        
        # Add Flesch-Kincaid grade level for additional context
        flesch_kincaid = textstat.flesch_kincaid_grade(text)
        
        # Calculate average grade level
        average_grade_level = (smog + gunning_fog + flesch_kincaid) / 3
        
        return {
            "smog_index": round(smog, 2),
            "gunning_fog": round(gunning_fog, 2),
            "flesch_kincaid_grade": round(flesch_kincaid, 2),
            "average_grade_level": round(average_grade_level, 2)
        }

    def _find_cts_keywords(self, text: str) -> Dict:
        """
        Find CTS keywords in the text and analyze their frequency.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with CTS keyword analysis
        """
        if not self.cts_keywords:
            if self.verbose:
                print("Warning: No CTS keywords loaded, skipping keyword analysis")
            return {
                "total_matches": 0,
                "matches_by_category": {},
                "matched_keywords": []
            }
            
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Count occurrences of each keyword
        matches = []
        for keyword, info in self.cts_keywords.items():
            # Simple word boundary matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            count = len(re.findall(pattern, text_lower))
            
            if count > 0:
                matches.append({
                    "keyword": keyword,
                    "category": info['category'],
                    "count": count,
                    "weight": info['weight']
                })
        
        # Summarize by category
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
        
    def analyze_from_scraper_output(self, scraper_output: Dict) -> Dict:
        """
        Analyze text from scraper output.
        
        Args:
            scraper_output: Dictionary output from Scraper
            
        Returns:
            Dictionary with analysis results
        """
        text = scraper_output.get('text', '')
        result = self.analyze_text(text)
        
        # Add basic metadata from scraper
        result['metadata'] = scraper_output.get('metadata', {})
        
        return result
        
    def save_json(self, data: Dict, output_path: str) -> str:
        """
        Save analysis results as JSON.
        
        Args:
            data: Dictionary with analysis results
            output_path: Path to save JSON file
            
        Returns:
            Path to the saved JSON file
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        if self.verbose:
            print(f"Saved analysis results to {output_path}")
            
        return output_path


def main():
    """Main function to run the EquiCheck from the command line."""
    parser = argparse.ArgumentParser(
        description="Analyze text for readability and cultural equity factors"
    )
    parser.add_argument(
        "source", 
        help="Text file, PDF file, or URL to analyze"
    )
    parser.add_argument(
        "-k", "--keywords",
        help="Path to CSV file with CTS keywords"
    )
    parser.add_argument(
        "-o", "--output",
        default="scores.json",
        help="Output JSON file path (default: scores.json)"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Print detailed information during analysis"
    )
    
    args = parser.parse_args()
    
    # Initialize EquiCheck
    equicheck = EquiCheck(
        cts_keywords_path=args.keywords,
        verbose=args.verbose
    )
    
    # Process source based on type
    if args.source.lower().endswith('.txt'):
        # It's a text file
        with open(args.source, 'r', encoding='utf-8') as f:
            text = f.read()
        result = equicheck.analyze_text(text)
    else:
        # It's a PDF or URL, use scraper first
        output_dir = os.path.dirname(args.output)
        if not output_dir:
            output_dir = '.'
            
        scraper = Scraper(output_dir=output_dir, verbose=args.verbose)
        
        if args.source.lower().startswith(('http://', 'https://')):
            # It's a URL
            scraper_result = scraper.extract_from_html(args.source)
        else:
            # It's a file path
            scraper_result = scraper.extract_from_pdf(args.source)
            
        result = equicheck.analyze_from_scraper_output(scraper_result)
    
    # Save results
    equicheck.save_json(result, args.output)
    
    # Print summary
    if 'readability' in result:
        print("\nReadability Scores:")
        print(f"SMOG Index: {result['readability'].get('smog_index')}")
        print(f"Gunning Fog: {result['readability'].get('gunning_fog')}")
        print(f"Average Grade Level: {result['readability'].get('average_grade_level')}")
    
    if 'cts_keywords' in result:
        print("\nCTS Keyword Analysis:")
        print(f"Total Matches: {result['cts_keywords'].get('total_matches')}")
        for category, info in result['cts_keywords'].get('matches_by_category', {}).items():
            print(f"  {category}: {info.get('count')} matches")


if __name__ == "__main__":
    main()
