# EquiCheck

EquiCheck is Clarify+'s Cultural-Equity & Readability Audit engine. It analyzes text content to determine readability metrics and identifies culturally relevant keywords to assess how well the content is tailored to diverse audiences.

## Features

- **Readability Analysis**: Calculate SMOG & Gunning-Fog readability indices
- **Cultural Tailoring Score (CTS)**: Analyze frequency of culturally relevant keywords
- **JSON Output**: Generate structured analysis results
- **Integration with Scraper**: Analyze PDFs and webpages directly

## Usage

### Command Line Interface

```bash
python -m backend.equicheck [source] [options]
```

#### Options

- `source`: Text file, PDF file, or URL to analyze
- `-k, --keywords`: Path to CSV file with CTS keywords (optional)
- `-o, --output`: Output JSON file path (default: scores.json)
- `-v, --verbose`: Print detailed information during analysis

### Examples

#### Analyze a PDF document

```bash
python -m backend.equicheck path/to/document.pdf -o analysis_results.json
```

#### Analyze with custom keywords

```bash
python -m backend.equicheck path/to/document.pdf -k path/to/custom_keywords.csv
```

### Programmatic Usage

You can also use the EquiCheck class in your Python code:

```python
from backend.equicheck import EquiCheck

# Initialize EquiCheck with CTS keywords
equicheck = EquiCheck(cts_keywords_path="path/to/keywords.csv", verbose=True)

# Analyze text directly
result = equicheck.analyze_text("Text content to analyze")

# Analyze a file using the scraper integration
from backend.scraper import Scraper
scraper = Scraper(output_dir="output")
scraper_result = scraper.extract_from_pdf("path/to/document.pdf")
result = equicheck.analyze_from_scraper_output(scraper_result)

# Save results
equicheck.save_json(result, "analysis_results.json")
```

## CTS Keywords Format

The Cultural Tailoring Score analysis requires a CSV file with the following format:

```csv
keyword,category,weight
diabetes,medical_condition,1.0
insulin,medical_treatment,1.0
elderly,age_group,0.8
african american,ethnicity,1.5
```

- `keyword`: The term to search for in the text
- `category`: The cultural/topical category of the keyword
- `weight`: A weight factor for calculating weighted frequencies

## Output Format

EquiCheck generates a JSON structure with the following format:

```json
{
  "readability": {
    "smog_index": 9.2,
    "gunning_fog": 10.5,
    "flesch_kincaid_grade": 8.7,
    "average_grade_level": 9.5
  },
  "cts_keywords": {
    "total_matches": 15,
    "matches_by_category": {
      "medical_condition": {
        "count": 5,
        "weighted_count": 5.0
      },
      "ethnicity": {
        "count": 3,
        "weighted_count": 4.5
      }
    },
    "matched_keywords": [
      {
        "keyword": "diabetes",
        "category": "medical_condition",
        "count": 3,
        "weight": 1.0
      }
    ]
  },
  "metadata": {
    "title": "Sample Decision Aid",
    "page_count": 5
  }
}
```

## Interpreting Readability Scores

- **SMOG Index**: Generally, SMOG index values correspond to the U.S. school grade level needed to understand the text. For patient education materials, aim for 6-8.
- **Gunning Fog**: Similar to SMOG, this indicates the years of formal education needed. For general public content, aim for 8 or below.
- **Average Grade Level**: A combined metric averaging SMOG, Gunning Fog, and Flesch-Kincaid Grade Level.

## API Reference

For detailed API documentation, see the [EquiCheck API Reference](../api/equicheck.md).
