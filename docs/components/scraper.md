# PDF/HTML Scraper

The Clarify+ Scraper is responsible for extracting text and images from PDF documents and HTML webpages. This component is the first step in the Clarify+ pipeline, providing the raw content that will be analyzed by other components.

## Features

- **PDF Content Extraction**: Extract text and images from PDF documents using PyMuPDF
- **HTML Content Extraction**: Scrape text and images from webpages
- **Metadata Extraction**: Retrieve document metadata (title, author, etc.)
- **Image Saving**: Save extracted images to disk
- **JSON Output**: Generate structured JSON output with extracted content

## Usage

### Command Line Interface

```bash
python -m backend.scraper [source] [options]
```

#### Options

- `source`: Path to PDF file or URL to HTML page
- `-o, --output`: Output directory (default: 'output')
- `--demo`: Run on a sample PtDA from the docs directory
- `-v, --verbose`: Print detailed information during extraction

### Examples

#### Extract from a PDF file

```bash
python -m backend.scraper path/to/document.pdf -o extracted_content
```

#### Extract from a webpage

```bash
python -m backend.scraper https://example.com/patient-info -o extracted_content
```

#### Use demo mode

```bash
python -m backend.scraper --demo -v
```

### Programmatic Usage

You can also use the Scraper class in your Python code:

```python
from backend.scraper import Scraper

# Initialize the scraper
scraper = Scraper(output_dir="output", verbose=True)

# Extract from PDF
result = scraper.extract_from_pdf("path/to/document.pdf")

# Extract from HTML
result = scraper.extract_from_html("https://example.com/page")

# Save results
scraper.save_json(result, "extracted_content.json")
```

## Output Format

The Scraper generates a JSON structure with the following format:

```json
{
  "text": "Full text content of the document",
  "images": [
    {
      "path": "output/images/page1_img0.png",
      "filename": "page1_img0.png",
      "extension": "png"
    }
  ],
  "metadata": {
    "title": "Document Title",
    "author": "Document Author",
    "subject": "Document Subject",
    "keywords": "Keywords",
    "page_count": 5
  },
  "pages": [
    {
      "page_num": 1,
      "text": "Text content of page 1",
      "images": [...]
    }
  ]
}
```

## API Reference

For detailed API documentation, see the [Scraper API Reference](../api/scraper.md).
