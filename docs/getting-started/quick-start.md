# Quick Start Guide

This guide will help you get started with Clarify+ and demonstrate its basic functionality.

## Basic Usage

### Analyzing a PDF Document

To analyze a Patient Decision Aid (PtDA) PDF:

```bash
# Navigate to the project directory
cd clarify-plus

# Run EquiCheck on a PDF
python -m backend.equicheck path/to/your/document.pdf -o analysis_results.json
```

The command will:
1. Extract text and images from the PDF
2. Calculate readability metrics (SMOG & Gunning-Fog)
3. Perform Cultural Tailoring Score (CTS) analysis
4. Save the results to `analysis_results.json`

### Using the Demo Mode

For a quick demonstration using a sample document:

```bash
python -m backend.equicheck --demo
```

This will run the analysis on one of the sample PDFs in the `docs` directory.

## Understanding the Output

The output JSON contains:

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

### Interpreting Readability Scores

- **SMOG Index**: 8.0 = 8th grade reading level
- **Gunning Fog**: 10.0 = 10th grade reading level
- **Average Grade Level**: Target for patient materials is 6th-8th grade

## Next Steps

For more advanced usage, see:
- [EquiCheck Component Documentation](../components/equicheck.md)
- [API Reference](../api/equicheck.md)
