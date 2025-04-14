# HTB-Scrape

A Python tool for extracting and formatting content from HackTheBox Academy HTML pages.

## Description

HTB-Scrape is a utility that extracts structured content from HackTheBox Academy HTML pages and converts it into clean, formatted text or JSON. It's designed to help users extract learning materials in a format that's easy to read, study, or process with language models.

## Overview

HTB-Scrape is designed specifically for LLM consumption. It creates a hierarchical structure where images are embedded within their parent elements (lists, table cells, etc.), making it easier for LLMs to understand the relationships between text and images.

## Features

- Extract content from local HTML files or directly from URLs
- Parse HackTheBox Academy's specific HTML structure
- Extract various content types (headings, paragraphs, code blocks, lists, images, tables, alerts)
- Download and save images from HTML content
- Maintain proper order of elements including images
- Create LLM-friendly structured output with embedded images
- Extract questions from modules
- Output in plain text (formatted for readability) or JSON
- Modular and extensible design

## Installation

### Prerequisites

- Miniconda or Anaconda installed on your system
- Git (optional, for cloning the repository)

### Setup with Conda Environment

This project uses a conda environment defined in the included `scrape_env.yml` file. This ensures consistent dependencies across different systems.

```bash
# Clone the repository (or download it)
git clone https://github.com/rtreacy87/htb-scrape.git
cd htb-scrape

# Create the conda environment from the provided yml file
conda env create -f scrape_env.yml

# Activate the environment
conda activate scrape
```

The environment includes all necessary dependencies:
- Python 3.12
- beautifulsoup4 and bs4
- requests
- pytest (for running tests)
- certifi

### Alternative: Manual Installation

If you prefer not to use conda, you can install the dependencies manually:

```bash
# Clone the repository
git clone https://github.com/rtreacy87/htb-scrape.git
cd htb-scrape

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install beautifulsoup4 bs4 requests pytest
```

## Testing

The project includes comprehensive tests to ensure functionality and reliability. Tests are organized by component, with detailed documentation for each test case.

### Running Tests

```bash
# Activate the conda environment
conda activate scrape

# Run all tests
python -m pytest

# Run tests for a specific component
python -m pytest tests/BaseHTMLExtractor/test_BaseHTMLExtractor.py

# Run a specific test
python -m pytest tests/BaseHTMLExtractor/test_BaseHTMLExtractor.py::test_process_code_block_with_language_SCP_BHTML005
```

### Test Documentation

Each test folder contains a README.md file with detailed descriptions of the tests, including:
- Test inputs and expected outputs
- What each test is checking
- Test categories and organization

For example, see the [BaseHTMLExtractor tests documentation](tests/BaseHTMLExtractor/README.md) for details on the HTML extraction tests.

## Usage

### Basic Usage

```bash
# Extract content from a local HTML file
python htb_scraper.py --file path/to/file.html

# Extract content from a URL
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123

# Specify output format (text or JSON)
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --format json

# Save output to a file
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --output output.txt

# Download images from HTML content
python htb_scraper.py --file path/to/file.html --download-images

# Specify a custom directory for downloaded images
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --image-dir custom_images
```

### Example Output

#### Text Format

```
# Introduction to Web Applications

Web applications are computer programs that run on web servers and are accessed through web browsers...

## Web Application Architecture

Web applications typically consist of:

- Front-end (client-side)
  ![Architecture diagram](images/architecture.png)
- Back-end (server-side)
- Database

## Questions

Question 1: What is the primary language used for front-end web development?
```

#### JSON Format

```json
{
  "title": "Introduction to Web Applications",
  "content": [
    {
      "type": "paragraph",
      "text": "Web applications are computer programs that run on web servers and are accessed through web browsers..."
    },
    {
      "type": "heading",
      "level": 2,
      "text": "Web Application Architecture"
    },
    {
      "type": "paragraph",
      "text": "Web applications typically consist of:"
    },
    {
      "type": "list",
      "list_type": "unordered",
      "items": [
        [
          {
            "type": "text",
            "content": "Front-end (client-side)"
          },
          {
            "type": "image",
            "src": "architecture.png",
            "alt": "Architecture diagram",
            "local_path": "images/architecture.png"
          }
        ],
        [
          {
            "type": "text",
            "content": "Back-end (server-side)"
          }
        ],
        [
          {
            "type": "text",
            "content": "Database"
          }
        ]
      ]
    }
  ],
  "questions": [
    "What is the primary language used for front-end web development?"
  ]
}
```

### Example Files

The project includes example files in the `examples/` directory to help you understand how the scraper works:

- `htb_page.html`: An example HTB Academy page that can be used for testing
- `output.txt`: The text output generated from the example page
- `output.json`: The JSON output generated from the example page

You can use these files to see how the scraper processes HTML content and formats it for different outputs:

```bash
# Process the example HTB page and generate text output
python htb_scraper.py --file examples/htb_page.html --output examples/output.txt

# Process the example HTB page and generate JSON output
python htb_scraper.py --file examples/htb_page.html --format json --output examples/output.json
```

## Project Structure

```
htb-scrape/
├── htb_scraper.py                  # Main scraper script
├── src/
│   ├── BaseHTMLExtractor.py        # Abstract base class for HTML extraction
│   ├── LLMStructuredExtractor.py   # LLM-friendly structured extractor
│   ├── fetch_html_from_url.py      # URL fetching utilities
│   ├── format_for_llm_structured.py # Formatting for LLM with embedded images
│   ├── image_handler.py            # Image downloading and processing
│   └── main_functions.py           # Core functionality
├── tests/                          # Unit tests and test files
│   ├── BaseHTMLExtractor/          # Tests for BaseHTMLExtractor class
│   │   ├── test_BaseHTMLExtractor.py # Test cases for BaseHTMLExtractor
│   │   └── README.md               # Detailed test documentation
│   ├── images/                      # Test images
│   ├── test_image.html             # Test HTML with images
│   └── test_complex.html           # Complex test HTML for structure testing
|   └── test_order.html             # Test HTML for element order testing
├── examples/                       # Example files
│   ├── htb_page.html               # Example HTB Academy page
│   ├── output.txt                  # Example text output
│   └── output.json                 # Example JSON output
├── images/                         # Downloaded images directory
├── .gitignore                      # Git ignore file
├── scrape_env.yml                  # Conda environment file
└── README.md                       # This file
```

## Code Quality

This project follows clean code principles to ensure maintainability and readability:

- **Single Responsibility Principle**: Each method has a single, well-defined responsibility
- **Small Methods**: Large methods are broken down into smaller, focused submethods
- **Descriptive Naming**: Clear method and variable names that describe their purpose
- **Comprehensive Documentation**: Detailed docstrings and comments
- **Organized Tests**: Well-structured tests with detailed documentation

### Recent Improvements

- Refactored `BaseHTMLExtractor._process_elements_in_order` method into smaller, focused submethods
- Reduced method parameter count by moving common parameters to class initialization
- Organized tests into separate folders with detailed documentation
- Improved test assertions to be more resilient to implementation changes

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
