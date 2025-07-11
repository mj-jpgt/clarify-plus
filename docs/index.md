# Clarify+

> **A lightweight, open-source "decision-aid compiler" that makes any medical PDF or webpage *clearer, fairer, and easier to trust*—in one click.**

## Overview

Clarify+ is designed to transform complex medical decision aids into more accessible, culturally sensitive, and numerically transparent materials. With a focus on readability, cultural equity, and risk literacy, Clarify+ helps patients make better-informed health decisions.

## Core Features

### 1. EquiCheck — Cultural-Equity & Readability Audit
* Runs SMOG & Gunning-Fog readability metrics on the fly
* Flags jargon, idioms, and images that clash with the Cultural Tailoring Score (CTS) rubric
* Generates a live radar badge so authors can watch their equity score rise as they edit

### 2. NumiCraft — Interactive Risk Literacy Engine
* Detects every percentage, "1 in N," or relative-risk statement
* Auto-builds colour-blind-safe icon arrays or bar charts
* Embeds 30-second "micro-quests" that teach users how to read the graphic and raise Berlin Numeracy scores

### 3. Plain-Language Rewriter
* One-tap GPT-3.5 rewrite to 6-8ᵗʰ-grade English (Spanish toggle optional)

## Getting Started

Visit the [Quick Start](getting-started/quick-start.md) guide to begin using Clarify+.

## Project Structure

```
clarify-plus/
├── backend/               # Python backend for text processing
│   ├── scraper.py         # PDF/HTML content extraction
│   ├── equicheck.py       # Readability and CTS analysis
│   └── riskify.py         # Risk literacy engine (coming soon)
├── frontend/              # React frontend components
├── docs/                  # Documentation
└── tests/                 # Test suite
```

## License

This project is open source under the MIT license.
