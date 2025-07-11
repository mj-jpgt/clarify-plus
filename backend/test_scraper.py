#!/usr/bin/env python3
"""
Unit tests for the Clarify+ scraper module.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests_mock

from scraper import Scraper


class TestScraper(unittest.TestCase):
    """Test cases for the Scraper class."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test outputs
        self.test_output_dir = tempfile.mkdtemp()
        self.scraper = Scraper(output_dir=self.test_output_dir, verbose=False)
        
    def tearDown(self):
        """Clean up after each test."""
        # Remove the temporary directory
        shutil.rmtree(self.test_output_dir)
    
    @patch('fitz.open')
    def test_extract_from_pdf_empty(self, mock_open):
        """Test extracting from an empty PDF."""
        # Mock PDF document
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 0
        mock_doc.metadata = {}
        mock_open.return_value = mock_doc
        
        result = self.scraper.extract_from_pdf("nonexistent.pdf")
        
        # Check that the result contains expected fields
        self.assertIn("text", result)
        self.assertIn("images", result)
        self.assertIn("metadata", result)
        self.assertIn("pages", result)
        self.assertEqual(result["text"], "")
        self.assertEqual(len(result["images"]), 0)
        self.assertEqual(len(result["pages"]), 0)
    
    @patch('fitz.open')
    def test_extract_from_pdf_with_content(self, mock_open):
        """Test extracting from a PDF with content."""
        # Mock PDF document with one page
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 1
        mock_doc.metadata = {
            "title": "Test PDF",
            "author": "Test Author",
        }
        
        # Mock page
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Sample PDF text"
        mock_page.get_images.return_value = []
        
        mock_doc.__iter__.return_value = [mock_page]
        mock_open.return_value = mock_doc
        
        result = self.scraper.extract_from_pdf("sample.pdf")
        
        # Check that the result contains expected content
        self.assertEqual(result["text"], "Sample PDF text")
        self.assertEqual(len(result["images"]), 0)
        self.assertEqual(len(result["pages"]), 1)
        self.assertEqual(result["metadata"]["title"], "Test PDF")
        self.assertEqual(result["metadata"]["author"], "Test Author")
        self.assertEqual(result["metadata"]["page_count"], 1)
    
    def test_extract_from_html(self):
        """Test extracting from an HTML page."""
        with requests_mock.Mocker() as m:
            m.get('http://example.com', text="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <h1>Test Heading</h1>
                <p>This is a test paragraph.</p>
                <img src="http://example.com/image.jpg" alt="Test Image">
            </body>
            </html>
            """)
            
            # Mock image response
            m.get('http://example.com/image.jpg', content=b'fake image data')
            
            result = self.scraper.extract_from_html('http://example.com')
            
            # Check that the result contains expected content
            self.assertIn("Test Heading", result["text"])
            self.assertIn("This is a test paragraph", result["text"])
            self.assertEqual(len(result["images"]), 1)
            self.assertEqual(result["metadata"]["title"], "Test Page")
            self.assertEqual(result["metadata"]["url"], "http://example.com")
            
    def test_save_json(self):
        """Test saving extracted data as JSON."""
        test_data = {
            "text": "Sample text",
            "images": [{"filename": "test.jpg"}]
        }
        
        output_path = self.scraper.save_json(test_data, "test_output.json")
        
        # Check that the file exists and contains the expected data
        self.assertTrue(os.path.exists(output_path))
        
        # Read the file and check content
        import json
        with open(output_path, 'r') as f:
            saved_data = json.load(f)
            
        self.assertEqual(saved_data["text"], "Sample text")
        self.assertEqual(len(saved_data["images"]), 1)
        self.assertEqual(saved_data["images"][0]["filename"], "test.jpg")


# Additional test cases to run with pytest
def test_scraper_initialization():
    """Test scraper initialization creates output directories."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        scraper = Scraper(output_dir=tmpdirname)
        assert os.path.exists(tmpdirname)
        assert os.path.exists(os.path.join(tmpdirname, "images"))

@pytest.mark.parametrize("url,is_html", [
    ("http://example.com", True),
    ("https://example.com", True),
    ("file.pdf", False),
    ("/path/to/file.pdf", False),
])
def test_source_type_detection(url, is_html):
    """Test detection of source type (HTML or PDF)."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        scraper = Scraper(output_dir=tmpdirname)
        
        if is_html:
            with requests_mock.Mocker() as m:
                m.get(url, text="<html><body>Test</body></html>")
                with patch.object(scraper, 'extract_from_html') as mock_html:
                    mock_html.return_value = {"text": "Test"}
                    with patch.object(scraper, 'extract_from_pdf') as mock_pdf:
                        # Call main function with this URL
                        from scraper import main
                        with patch('sys.argv', ['scraper.py', url]):
                            with pytest.raises(SystemExit):
                                main()
                        
                        # Check that extract_from_html was called, not extract_from_pdf
                        mock_html.assert_called_once()
                        mock_pdf.assert_not_called()


if __name__ == '__main__':
    unittest.main()
