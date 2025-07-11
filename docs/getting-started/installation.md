# Installation

This guide will walk you through installing Clarify+ and its dependencies.

## Prerequisites

Before installing Clarify+, you'll need:

- Python 3.9 or higher
- Node.js 18 or higher (for the frontend components)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/mj-jpgt/clarify-plus.git
cd clarify-plus
```

### 2. Install Backend Dependencies

Navigate to the backend directory and install the Python dependencies:

```bash
cd backend
pip install -r requirements.txt
cd ..
```

### 3. Install Frontend Dependencies (Optional)

If you want to use the frontend components:

```bash
cd frontend
npm install
cd ..
```

### 4. Verify Installation

You can verify that the installation was successful by running:

```bash
python -m backend.scraper --demo
```

This should extract content from a sample PDF in the docs directory and output to the `output` directory.

## Development Installation

For developers who want to contribute to Clarify+:

```bash
# Clone the repository
git clone https://github.com/mj-jpgt/clarify-plus.git
cd clarify-plus

# Install backend dependencies with dev extras
cd backend
pip install -r requirements.txt
pip install -e ".[dev]"

# Install frontend dependencies
cd ../frontend
npm install

# Run tests
cd ..
pytest
npm test --prefix frontend
```

## Docker Installation (Coming Soon)

A Docker installation option will be available in a future release to simplify deployment.
