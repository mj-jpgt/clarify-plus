#!/usr/bin/env python3
"""
Clarify+ PDF/HTML Scraper

This module extracts text and images from PDF files and HTML documents.
It can be used as a standalone script or imported as a module.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional

import PyPDF2
import requests
from bs4 import BeautifulSoup


class Scraper:
    """Main scraper class for extracting text and images from PDF/HTML documents."""

    def __init__(self, verbose: bool = False):
        """
        Initialize the scraper.

        Args:
            verbose: Whether to print detailed information.
        """
        self.verbose = verbose
        if self.verbose:
            print("Initialized scraper.")

    def extract_from_pdf(self, pdf_path: str) -> Dict:
        """
        Extract text from a PDF file using PyPDF2.
        Note: Image extraction from PDFs is not supported with PyPDF2.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary with extracted text and metadata
        """
        if self.verbose:
            print(f"Processing PDF: {pdf_path}")
            
        result = {
            "text": "",
            "images": [],  # PDF Image extraction disabled
            "metadata": {},
            "pages": []
        }
        
        try:
            with open(pdf_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                metadata = reader.metadata
                
                result["metadata"] = {
                    "title": metadata.title if metadata else "",
                    "author": metadata.author if metadata else "",
                    "subject": metadata.subject if metadata else "",
                    "producer": metadata.producer if metadata else "",
                    "page_count": len(reader.pages)
                }
                
                full_text = ""
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    full_text += page_text
                    
                    page_data = {
                        "page_num": page_num + 1,
                        "text": page_text,
                        "images": [] # PDF Image extraction disabled
                    }
                    result["pages"].append(page_data)
                
                result["text"] = full_text

            if self.verbose:
                print(f"Extracted {len(full_text)} characters of text from PDF.")

        except Exception as e:
            print(f"Error extracting content from PDF: {e}")
        
        return result

    def extract_from_html(self, url: str) -> Dict:
        """
        Extract text and images from an HTML page.

        Args:
            url: URL of the webpage

        Returns:
            Dictionary with extracted text and image paths
        """
        if self.verbose:
            print(f"Processing HTML: {url}")
            
        result = {
            "text": "",
            "images": [],
            "metadata": {},
            "pages": [{"page_num": 1, "text": "", "images": []}]
        }
        
        try:
            # Fetch the HTML content
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract metadata
            result["metadata"] = {
                "title": soup.title.string if soup.title else "",
                "url": url
            }
            
            # Extract text (excluding script and style content)
            for script in soup(["script", "style"]):
                script.extract()
            
            text = soup.get_text()
            # Clean the text (remove extra whitespace and normalize line breaks)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            result["text"] = text
            result["pages"][0]["text"] = text
            
            # Extract images
            for img_index, img in enumerate(soup.find_all('img')):
                img_url = img.get('src', '')
                if not img_url:
                    continue
                
                # Handle relative URLs
                if not img_url.startswith(('http://', 'https://')):
                    base_url = '/'.join(url.split('/')[:3])  # Get domain
                    img_url = f"{base_url}/{img_url.lstrip('/')}"
                
                try:
                    img_response = requests.get(img_url)
                    img_response.raise_for_status()
                    
                    # Determine image extension from URL or content-type
                    img_ext = img_url.split('.')[-1].lower()
                    if img_ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']:
                        content_type = img_response.headers.get('content-type', '')
                        if 'jpeg' in content_type or 'jpg' in content_type:
                            img_ext = 'jpg'
                        elif 'png' in content_type:
                            img_ext = 'png'
                        elif 'gif' in content_type:
                            img_ext = 'gif'
                        elif 'webp' in content_type:
                            img_ext = 'webp'
                        elif 'svg' in content_type:
                            img_ext = 'svg'
                        else:
                            img_ext = 'unknown'
                    
                    img_filename = f"img{img_index}.{img_ext}"
                    img_path = self.images_dir / img_filename
                    
                    # Save the image
                    with open(img_path, "wb") as img_file:
                        img_file.write(img_response.content)
                    
                    # Add image info to results
                    img_info = {
                        "path": str(img_path),
                        "filename": img_filename,
                        "extension": img_ext,
                        "original_url": img_url,
                        "alt_text": img.get('alt', '')
                    }
                    result["images"].append(img_info)
                    result["pages"][0]["images"].append(img_info)
                    
                except Exception as e:
                    print(f"Error downloading image {img_url}: {e}")
                
            if self.verbose:
                print(f"Extracted {len(result['images'])} images and {len(text)} characters of text")
                
            return result
            
        except Exception as e:
            print(f"Error extracting content from HTML: {e}")
            return result
            
    def run(self, source: str, output_path: Path):
        """
        Run the full extraction process for a given source and save to output path.
        """
        # Ensure output directories exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.images_dir = output_path.parent / "images"
        self.images_dir.mkdir(exist_ok=True)

        if source.startswith(('http://', 'https://')):
            data = self.extract_from_html(source)
        elif Path(source).is_file() and Path(source).suffix.lower() == '.pdf':
            data = self.extract_from_pdf(source)
        else:
            raise ValueError("Source must be a valid URL or path to a PDF file.")

        self.save_json(data, output_path)
        if self.verbose:
            print(f"[bold green]Scraping complete. Results saved to {output_path}[/bold green]")

    def save_json(self, data: Dict, output_path: Path):
        """
        Save the extracted data to a JSON file.

        Args:
            data: Dictionary with extracted data
            output_path: Path to the output JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        if self.verbose:
            print(f"Saved JSON data to {output_path}")


def main():
    """Main function to run the scraper from the command line."""
    parser = argparse.ArgumentParser(description="Clarify+ PDF/HTML Scraper")
    parser.add_argument("source", help="Path or URL to the document to process")
    parser.add_argument("-o", "--output", dest="output_path", type=Path, default=Path("output/scraped_content.json"), help="Path to save the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    scraper = Scraper(verbose=args.verbose)
    try:
        scraper.run(args.source, args.output_path)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)
        sample_file = str(sample_files[0])
        print(f"Demo mode: Using sample file {sample_file}")
        source = sample_file
    else:
        source = args.source
    
    # Process based on source type
    if source.lower().startswith(("http://", "https://")):
        # It's a URL, extract from HTML
        result = scraper.extract_from_html(source)
    else:
        # It's a file path, extract from PDF
        if not os.path.isfile(source):
            print(f"Error: File not found - {source}")
            sys.exit(1)
        result = scraper.extract_from_pdf(source)
    
    # Save results as JSON
    scraper.save_json(result)


if __name__ == "__main__":
    main()
