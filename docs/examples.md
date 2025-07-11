# Examples

This page contains examples of using Clarify+ for various use cases.

## Example 1: Analyzing a Diabetes Patient Decision Aid

This example demonstrates analyzing a diabetes PtDA for readability and cultural equity factors.

### Command

```bash
python -m backend.equicheck docs/DiabetesPtDA.pdf -o diabetes_analysis.json -v
```

### Output

The analysis produces a JSON file (`diabetes_analysis.json`) with readability metrics and CTS keyword matches:

```json
{
  "readability": {
    "smog_index": 9.2,
    "gunning_fog": 10.5,
    "flesch_kincaid_grade": 8.7,
    "average_grade_level": 9.5
  },
  "cts_keywords": {
    "total_matches": 24,
    "matches_by_category": {
      "medical_condition": {
        "count": 8,
        "weighted_count": 8.0
      },
      "ethnicity": {
        "count": 4,
        "weighted_count": 6.0
      }
    }
  }
}
```

### Interpretation

The average grade level of 9.5 indicates the text is written at approximately a 9th-10th grade reading level, which is higher than the recommended 6th-8th grade level for patient materials. The analysis also found 24 cultural keywords, with medical conditions and ethnic references being the most common categories.

## Example 2: Batch Processing Multiple Documents

This example shows how to process multiple documents and compare their results.

### Script

```python
from backend.scraper import Scraper
from backend.equicheck import EquiCheck
import os
import json

# Initialize components
scraper = Scraper(output_dir="batch_output")
equicheck = EquiCheck(cts_keywords_path="backend/cts_keywords.csv")

# List of documents to process
documents = [
    "docs/DiabetesPtDA.pdf",
    "docs/OsteoarthritisPtDA.pdf",
    "docs/StatinPtDA.pdf"
]

# Process each document
results = {}
for doc in documents:
    doc_name = os.path.basename(doc).split('.')[0]
    print(f"Processing {doc_name}...")
    
    # Extract content
    scraper_output = scraper.extract_from_pdf(doc)
    
    # Analyze content
    analysis = equicheck.analyze_from_scraper_output(scraper_output)
    
    # Store results
    results[doc_name] = {
        "average_grade_level": analysis["readability"]["average_grade_level"],
        "total_cts_matches": analysis["cts_keywords"]["total_matches"]
    }

# Print comparison
print("\nReadability Comparison:")
print("-" * 50)
print(f"{'Document':<20} {'Grade Level':<15} {'CTS Matches':<15}")
print("-" * 50)
for doc, data in results.items():
    print(f"{doc:<20} {data['average_grade_level']:<15.1f} {data['total_cts_matches']:<15}")

# Save consolidated results
with open("batch_output/comparison.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Sample Output

```
Readability Comparison:
--------------------------------------------------
Document             Grade Level      CTS Matches    
--------------------------------------------------
DiabetesPtDA        9.5              24             
OsteoarthritisPtDA  8.7              18             
StatinPtDA          10.2             15             
```

## Full Example Output

For a complete example of the JSON output structure, see the [sample output file](examples/sample_output.json).

## Next Steps

After analyzing the readability and cultural tailoring of your documents, you might:

1. Identify passages with high grade levels for simplification
2. Check which cultural categories are underrepresented
3. Use the upcoming NumiCraft component to improve numerical representations
4. Apply the Plain-Language Rewriter to problematic sections
