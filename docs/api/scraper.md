# Scraper API Reference

This page provides detailed API documentation for the Scraper component.

## `Scraper` Class

```python
class Scraper:
    """Main scraper class for extracting text and images from PDF/HTML documents."""

    def __init__(self, output_dir: str = "output", verbose: bool = False):
        """
        Initialize the scraper with output directory and verbosity settings.

        Args:
            output_dir: Directory to save extracted content
            verbose: Whether to print detailed information
        """
```

### Methods

#### `extract_from_pdf`

```python
def extract_from_pdf(self, pdf_path: str) -> Dict:
    """
    Extract text and images from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Dictionary with extracted text and image paths
    """
```

This method:
- Opens a PDF file using PyMuPDF
- Extracts metadata like title, author, etc.
- Extracts text content from each page
- Finds and saves images to the output directory
- Returns a structured dictionary with all extracted content

#### `extract_from_html`

```python
def extract_from_html(self, url: str) -> Dict:
    """
    Extract text and images from an HTML page.

    Args:
        url: URL of the webpage

    Returns:
        Dictionary with extracted text and image paths
    """
```

This method:
- Fetches HTML content from the specified URL
- Extracts metadata like title
- Parses HTML to extract clean text content
- Downloads and saves images from the page
- Returns a structured dictionary with all extracted content

#### `save_json`

```python
def save_json(self, data: Dict, filename: str = "extracted_content.json") -> str:
    """
    Save extracted data as JSON.

    Args:
        data: Dictionary with extracted data
        filename: Output JSON filename

    Returns:
        Path to the saved JSON file
    """
```

This method saves the extracted data as a JSON file in the output directory.

## Command Line Interface

```python
def main():
    """Main function to run the scraper from the command line."""
```

The module can be run as a script with the following arguments:
- `source`: Path to PDF file or URL to HTML page
- `-o, --output`: Output directory (default: 'output')
- `--demo`: Run on sample PtDA and output to text.txt and images/
- `-v, --verbose`: Print detailed information during extraction

## Example Usage

```python
# Initialize scraper
scraper = Scraper(output_dir="my_output", verbose=True)

# Process a PDF
pdf_result = scraper.extract_from_pdf("document.pdf")

# Process a webpage
html_result = scraper.extract_from_html("https://example.com")

# Save results
json_path = scraper.save_json(pdf_result, "pdf_content.json")
```
