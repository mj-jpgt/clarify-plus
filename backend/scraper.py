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

import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup


class Scraper:
    """Main scraper class for extracting text and images from PDF/HTML documents."""

    def __init__(self, 
                output_dir: str = "output", 
                verbose: bool = False):
        """
        Initialize the scraper with output directory and verbosity settings.

        Args:
            output_dir: Directory to save extracted content
            verbose: Whether to print detailed information
        """
        self.output_dir = output_dir
        self.verbose = verbose
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        
        if self.verbose:
            print(f"Initialized scraper. Output will be saved to {output_dir}")

    def extract_from_pdf(self, pdf_path: str) -> Dict:
        """
        Extract text and images from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary with extracted text and image paths
        """
        if self.verbose:
            print(f"Processing PDF: {pdf_path}")
            
        result = {
            "text": "",
            "images": [],
            "metadata": {},
            "pages": []
        }
        
        try:
            # Open the PDF file
            doc = fitz.open(pdf_path)
            
            # Extract metadata
            result["metadata"] = {
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "keywords": doc.metadata.get("keywords", ""),
                "producer": doc.metadata.get("producer", ""),
                "page_count": len(doc)
            }
            
            # Process each page
            full_text = ""
            for page_num, page in enumerate(doc):
                page_text = page.get_text()
                full_text += page_text
                
                page_data = {
                    "page_num": page_num + 1,
                    "text": page_text,
                    "images": []
                }
                
                # Extract images
                image_list = page.get_images(full=True)
                for img_index, img_info in enumerate(image_list):
                    img_index_str = str(img_index)
                    xref = img_info[0]
                    base_img = doc.extract_image(xref)
                    img_bytes = base_img["image"]
                    img_ext = base_img["ext"]
                    img_filename = f"page{page_num+1}_img{img_index}.{img_ext}"
                    img_path = os.path.join(self.output_dir, "images", img_filename)
                    
                    # Save the image
                    with open(img_path, "wb") as img_file:
                        img_file.write(img_bytes)
                    
                    # Add image info to results
                    img_info = {
                        "path": img_path,
                        "filename": img_filename,
                        "extension": img_ext
                    }
                    result["images"].append(img_info)
                    page_data["images"].append(img_info)
                
                result["pages"].append(page_data)
            
            result["text"] = full_text
            
            # Save the extracted text to a file
            text_file_path = os.path.join(self.output_dir, "text.txt")
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(full_text)
                
            if self.verbose:
                print(f"Extracted {len(result['images'])} images and {len(full_text)} characters of text")
                
            return result
            
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
                    img_path = os.path.join(self.output_dir, "images", img_filename)
                    
                    # Save the image
                    with open(img_path, "wb") as img_file:
                        img_file.write(img_response.content)
                    
                    # Add image info to results
                    img_info = {
                        "path": img_path,
                        "filename": img_filename,
                        "extension": img_ext,
                        "original_url": img_url,
                        "alt_text": img.get('alt', '')
                    }
                    result["images"].append(img_info)
                    result["pages"][0]["images"].append(img_info)
                    
                except Exception as e:
                    print(f"Error downloading image {img_url}: {e}")
            
            # Save the extracted text to a file
            text_file_path = os.path.join(self.output_dir, "text.txt")
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(text)
                
            if self.verbose:
                print(f"Extracted {len(result['images'])} images and {len(text)} characters of text")
                
            return result
            
        except Exception as e:
            print(f"Error extracting content from HTML: {e}")
            return result
            
    def save_json(self, data: Dict, filename: str = "extracted_content.json") -> str:
        """
        Save extracted data as JSON.

        Args:
            data: Dictionary with extracted data
            filename: Output JSON filename

        Returns:
            Path to the saved JSON file
        """
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        if self.verbose:
            print(f"Saved extracted content to {output_path}")
            
        return output_path


def main():
    """Main function to run the scraper from the command line."""
    parser = argparse.ArgumentParser(
        description="Extract text and images from PDF files or HTML pages"
    )
    parser.add_argument(
        "source", 
        help="PDF file path or URL to an HTML page"
    )
    parser.add_argument(
        "-o", "--output", 
        default="output",
        help="Output directory for extracted content (default: 'output')"
    )
    parser.add_argument(
        "--demo", 
        action="store_true",
        help="Run on sample PtDA and output to text.txt and images/"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Print detailed information during extraction"
    )
    
    args = parser.parse_args()
    
    # Initialize the scraper
    scraper = Scraper(output_dir=args.output, verbose=args.verbose)
    
    # Handle demo mode
    if args.demo:
        # Look for sample files in the docs directory
        docs_dir = Path(__file__).parent.parent / "docs"
        sample_files = list(docs_dir.glob("*.pdf"))
        
        if not sample_files:
            print("Error: No sample PDF files found in the docs directory")
            sys.exit(1)
        
        # Use the first PDF file found
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
