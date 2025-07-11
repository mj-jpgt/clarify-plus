#!/usr/bin/env python3
"""
Unit tests for the Clarify+ EquiCheck module.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from equicheck import EquiCheck


class TestEquiCheck(unittest.TestCase):
    """Test cases for the EquiCheck class."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create a test keywords file
        self.keywords_path = os.path.join(self.test_dir, "test_keywords.csv")
        with open(self.keywords_path, 'w', encoding='utf-8') as f:
            f.write("keyword,category,weight\n")
            f.write("diabetes,medical_condition,1.0\n")
            f.write("doctor,medical_professional,1.0\n")
            f.write("elderly,age_group,0.8\n")
            f.write("african american,ethnicity,1.5\n")
        
        # Initialize EquiCheck with test keywords
        self.equicheck = EquiCheck(
            cts_keywords_path=self.keywords_path,
            verbose=False
        )
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_load_cts_keywords(self):
        """Test loading CTS keywords from CSV."""
        # Check that keywords were loaded correctly
        self.assertEqual(len(self.equicheck.cts_keywords), 4)
        self.assertIn("diabetes", self.equicheck.cts_keywords)
        self.assertIn("doctor", self.equicheck.cts_keywords)
        self.assertIn("elderly", self.equicheck.cts_keywords)
        self.assertIn("african american", self.equicheck.cts_keywords)
        
        # Check keyword properties
        self.assertEqual(self.equicheck.cts_keywords["diabetes"]["category"], "medical_condition")
        self.assertEqual(self.equicheck.cts_keywords["diabetes"]["weight"], 1.0)
        self.assertEqual(self.equicheck.cts_keywords["elderly"]["weight"], 0.8)
        self.assertEqual(self.equicheck.cts_keywords["african american"]["weight"], 1.5)
    
    def test_analyze_text_empty(self):
        """Test analyzing empty text."""
        result = self.equicheck.analyze_text("")
        
        # Check that result contains expected sections
        self.assertIn("readability", result)
        self.assertIn("cts_keywords", result)
        
        # Check readability scores are None for empty text
        self.assertIsNone(result["readability"]["smog_index"])
        self.assertIsNone(result["readability"]["gunning_fog"])
        
        # Check CTS keywords are empty
        self.assertEqual(result["cts_keywords"]["total_matches"], 0)
        self.assertEqual(len(result["cts_keywords"]["matched_keywords"]), 0)
    
    def test_analyze_text_with_keywords(self):
        """Test analyzing text with CTS keywords."""
        text = "The doctor suggested that diabetes is common among the elderly population. African American patients may have different risk factors."
        
        result = self.equicheck.analyze_text(text)
        
        # Check readability scores are calculated
        self.assertIsNotNone(result["readability"]["smog_index"])
        self.assertIsNotNone(result["readability"]["gunning_fog"])
        self.assertIsNotNone(result["readability"]["average_grade_level"])
        
        # Check CTS keywords are found
        self.assertEqual(result["cts_keywords"]["total_matches"], 4)
        self.assertEqual(len(result["cts_keywords"]["matched_keywords"]), 4)
        
        # Check categories
        categories = result["cts_keywords"]["matches_by_category"]
        self.assertIn("medical_condition", categories)
        self.assertIn("medical_professional", categories)
        self.assertIn("age_group", categories)
        self.assertIn("ethnicity", categories)
        
        # Check counts
        self.assertEqual(categories["medical_condition"]["count"], 1)
        self.assertEqual(categories["medical_professional"]["count"], 1)
        self.assertEqual(categories["ethnicity"]["count"], 1)
        
        # Check weighted counts
        self.assertEqual(categories["medical_condition"]["weighted_count"], 1.0)
        self.assertEqual(categories["ethnicity"]["weighted_count"], 1.5)
    
    def test_analyze_text_no_keywords(self):
        """Test analyzing text without CTS keywords."""
        # Create an EquiCheck instance with no keywords
        equicheck_no_keywords = EquiCheck(verbose=False)
        
        text = "This text does not contain any of the keywords."
        
        result = equicheck_no_keywords.analyze_text(text)
        
        # Check readability scores are calculated
        self.assertIsNotNone(result["readability"]["smog_index"])
        self.assertIsNotNone(result["readability"]["gunning_fog"])
        
        # Check CTS keywords are empty
        self.assertEqual(result["cts_keywords"]["total_matches"], 0)
        self.assertEqual(len(result["cts_keywords"]["matches_by_category"]), 0)
    
    def test_calculate_readability(self):
        """Test calculating readability metrics."""
        text = "This is a simple test sentence. It should have a low readability score."
        
        readability = self.equicheck._calculate_readability(text)
        
        # Check that all metrics are calculated
        self.assertIn("smog_index", readability)
        self.assertIn("gunning_fog", readability)
        self.assertIn("flesch_kincaid_grade", readability)
        self.assertIn("average_grade_level", readability)
        
        # Check that values are reasonable
        self.assertIsInstance(readability["smog_index"], float)
        self.assertIsInstance(readability["gunning_fog"], float)
        self.assertGreaterEqual(readability["smog_index"], 0)
        self.assertGreaterEqual(readability["gunning_fog"], 0)
    
    def test_find_cts_keywords(self):
        """Test finding CTS keywords in text."""
        text = "Diabetes is a medical condition that affects many elderly people."
        
        result = self.equicheck._find_cts_keywords(text)
        
        # Check that keywords are found
        self.assertEqual(result["total_matches"], 2)
        self.assertEqual(len(result["matched_keywords"]), 2)
        
        # Check that matched keywords are correct
        keywords = [match["keyword"] for match in result["matched_keywords"]]
        self.assertIn("diabetes", keywords)
        self.assertIn("elderly", keywords)
        
        # Check categories
        self.assertIn("medical_condition", result["matches_by_category"])
        self.assertIn("age_group", result["matches_by_category"])
    
    def test_save_json(self):
        """Test saving analysis results as JSON."""
        data = {
            "readability": {"smog_index": 8.5},
            "cts_keywords": {"total_matches": 2}
        }
        
        output_path = os.path.join(self.test_dir, "test_output.json")
        self.equicheck.save_json(data, output_path)
        
        # Check that file exists
        self.assertTrue(os.path.exists(output_path))
        
        # Read file and check content
        import json
        with open(output_path, 'r') as f:
            saved_data = json.load(f)
            
        self.assertEqual(saved_data["readability"]["smog_index"], 8.5)
        self.assertEqual(saved_data["cts_keywords"]["total_matches"], 2)


# Additional test cases to run with pytest
def test_equicheck_initialization():
    """Test EquiCheck initialization without keywords."""
    equicheck = EquiCheck(verbose=False)
    assert len(equicheck.cts_keywords) == 0


@pytest.mark.parametrize("text,expected_matches", [
    ("No keywords here", 0),
    ("The doctor said I have diabetes", 2),
    ("Elderly African American patients", 2),
    ("The doctor discussed diabetes with elderly African American patients", 4),
])
def test_keyword_matching(text, expected_matches):
    """Test keyword matching with different texts."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create a test keywords file
        keywords_path = os.path.join(tmpdirname, "test_keywords.csv")
        with open(keywords_path, 'w', encoding='utf-8') as f:
            f.write("keyword,category,weight\n")
            f.write("diabetes,medical_condition,1.0\n")
            f.write("doctor,medical_professional,1.0\n")
            f.write("elderly,age_group,0.8\n")
            f.write("african american,ethnicity,1.5\n")
        
        # Initialize EquiCheck with test keywords
        equicheck = EquiCheck(
            cts_keywords_path=keywords_path,
            verbose=False
        )
        
        result = equicheck.analyze_text(text)
        assert result["cts_keywords"]["total_matches"] == expected_matches


if __name__ == '__main__':
    unittest.main()
