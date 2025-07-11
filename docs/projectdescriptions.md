# Project Descriptions

This document provides detailed descriptions of each sprint in the Clarify+ project development process.

## Sprint 1: Core Engines

**Duration**: Weeks 3-4, ~30 hours total

### Overview

Sprint 1 focused on developing the core engines of the Clarify+ platform. The primary goal was to create the foundational components that would extract content from PDFs and HTML pages, analyze readability metrics, and assess cultural tailoring through keyword analysis. This sprint laid the groundwork for subsequent development phases by establishing the data extraction and analysis pipeline.

### Key Deliverables

1. **PDF/HTML Scraper** (`scraper.py`)
   - Built using PyMuPDF for PDF content extraction
   - Implemented HTML scraping using requests and BeautifulSoup
   - Added support for extracting and saving images
   - Created structured JSON output format with metadata, text, and image paths
   - Implemented a `--demo` flag for easy testing with sample documents

2. **Readability & Cultural Tailoring Score Analysis** (`equicheck.py`)
   - Integrated textstat library to calculate SMOG & Gunning-Fog readability metrics
   - Implemented Flesch-Kincaid grade level calculation for comprehensive readability assessment
   - Created a CSV-based Cultural Tailoring Score (CTS) keyword system
   - Developed pattern matching to identify culturally relevant keywords in extracted text
   - Added category-based analysis with frequency counting and weighted scoring
   - Generated comprehensive JSON output with both readability and cultural equity metrics

3. **Unit Tests & CLI**
   - Created comprehensive test suite using pytest
   - Implemented tests for edge cases (empty documents, missing files, etc.)
   - Added mock testing for external dependencies
   - Built a command-line interface for both scraper and equicheck modules
   - Ensured modularity for both standalone usage and programmatic integration

4. **Documentation**
   - Set up mkdocs with material theme for project documentation
   - Created comprehensive installation guide and quick start tutorial
   - Added detailed component documentation for both scraper and equicheck
   - Included API references with method descriptions and examples
   - Provided sample outputs and use cases

### Technical Implementation Details

#### PDF/HTML Scraper

The scraper module uses PyMuPDF (a Python binding for the MuPDF library) to extract text and images from PDF files. It processes PDFs page by page, extracting text content and identifying embedded images. For each image, it saves the binary data to disk and records metadata such as location and format.

For HTML content, the scraper uses requests to fetch webpages and BeautifulSoup for parsing. It extracts clean text by removing script and style elements, and downloads images referenced in img tags.

All extracted content is organized into a structured JSON format that includes:
- Full text content
- Metadata (title, author, etc.)
- Page-by-page breakdown of content
- Paths to extracted images

#### EquiCheck Engine

The EquiCheck module analyzes text for both readability and cultural tailoring factors. It uses the textstat library to calculate three readability metrics:

1. SMOG Index - Estimates the years of education needed to understand a text
2. Gunning Fog Index - Measures the readability based on sentence length and complex words
3. Flesch-Kincaid Grade Level - Calculates grade level based on sentence length and syllable count

For cultural tailoring analysis, EquiCheck loads a CSV file containing keywords, their categories, and weights. It then searches for these keywords in the text and calculates both raw and weighted frequencies, grouped by category. This helps identify how well the text addresses various cultural factors such as:
- Medical conditions and treatments
- Age groups and life stages
- Ethnic and cultural references
- Gender and identity considerations
- Socioeconomic factors

### Integration and Workflow

The components are designed to work both independently and together in a pipeline:

1. The user provides a PDF or URL to analyze
2. The scraper extracts the content and saves it as JSON
3. EquiCheck analyzes the text for readability and cultural factors
4. The results are saved as structured JSON for further processing or visualization

### Technical Challenges Addressed

1. **PDF Extraction Complexity**: Handled variations in PDF structure and encoding
2. **Error Handling**: Added robust error handling for malformed documents and network issues
3. **Performance Optimization**: Ensured efficient processing even for large documents
4. **Modular Design**: Created components that can be used independently or in combination
5. **Testing Edge Cases**: Built tests for unusual scenarios like blank pages or scanned PDFs

### Milestone Achievement

The Sprint 1 milestone deliverable was successfully completed: `equicheck.py` returns readability and CTS keyword analysis for any Patient Decision Aid in less than 3 seconds, meeting the performance target while providing comprehensive analysis.

This foundation sets the stage for Sprint 2, which will build upon these core engines to implement the NumiCraft risk literacy engine and begin frontend integration.
