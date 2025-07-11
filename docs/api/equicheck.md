# EquiCheck API Reference

This page provides detailed API documentation for the EquiCheck component.

## `EquiCheck` Class

```python
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
```

### Methods

#### `load_cts_keywords`

```python
def load_cts_keywords(self, file_path: str) -> None:
    """
    Load CTS keywords from a CSV file.
    
    Expected format: keyword,category,weight
    
    Args:
        file_path: Path to CSV file with CTS keywords
    """
```

This method:
- Reads a CSV file containing cultural keywords
- Parses each keyword entry with its category and weight
- Stores the keywords in a dictionary for analysis

#### `analyze_text`

```python
def analyze_text(self, text: str) -> Dict:
    """
    Analyze text for readability and CTS keywords.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with analysis results
    """
```

This method:
- Analyzes the given text for readability metrics
- Identifies CTS keywords in the text
- Returns a structured dictionary with analysis results

#### `_calculate_readability`

```python
def _calculate_readability(self, text: str) -> Dict:
    """
    Calculate readability metrics for the given text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with readability scores
    """
```

This method calculates:
- SMOG index
- Gunning Fog index
- Flesch-Kincaid grade level
- Average grade level across all metrics

#### `_find_cts_keywords`

```python
def _find_cts_keywords(self, text: str) -> Dict:
    """
    Find CTS keywords in the text and analyze their frequency.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with CTS keyword analysis
    """
```

This method:
- Searches for each defined keyword in the text
- Counts occurrences of each keyword
- Groups results by category
- Calculates weighted frequencies based on keyword weights

#### `analyze_from_scraper_output`

```python
def analyze_from_scraper_output(self, scraper_output: Dict) -> Dict:
    """
    Analyze text from scraper output.
    
    Args:
        scraper_output: Dictionary output from Scraper
        
    Returns:
        Dictionary with analysis results
    """
```

This method:
- Takes output from the Scraper component
- Extracts the text content from the scraper output
- Analyzes the text using the analyze_text method
- Adds metadata from the scraper output to the analysis results

#### `save_json`

```python
def save_json(self, data: Dict, output_path: str) -> str:
    """
    Save analysis results as JSON.
    
    Args:
        data: Dictionary with analysis results
        output_path: Path to save JSON file
        
    Returns:
        Path to the saved JSON file
    """
```

This method saves the analysis results as a JSON file at the specified path.

## Command Line Interface

```python
def main():
    """Main function to run the EquiCheck from the command line."""
```

The module can be run as a script with the following arguments:
- `source`: Text file, PDF file, or URL to analyze
- `-k, --keywords`: Path to CSV file with CTS keywords
- `-o, --output`: Output JSON file path (default: scores.json)
- `-v, --verbose`: Print detailed information during analysis

## Example Usage

```python
# Initialize EquiCheck
equicheck = EquiCheck(cts_keywords_path="keywords.csv", verbose=True)

# Analyze text
text = "Sample text content to analyze..."
result = equicheck.analyze_text(text)

# Analyze PDF via scraper
from scraper import Scraper
scraper = Scraper()
scraper_output = scraper.extract_from_pdf("document.pdf")
result = equicheck.analyze_from_scraper_output(scraper_output)

# Save results
equicheck.save_json(result, "analysis.json")
```
