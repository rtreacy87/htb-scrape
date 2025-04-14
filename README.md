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
├── tests/                      # Unit tests and test files
│   ├── image/                      # Test images
│   ├── test_image.html             # Test HTML with images
│   └── test_complex.html           # Complex test HTML for structure testing
├── images/                     # Downloaded images directory
├── .gitignore                  # Git ignore file
├── scrape_env.yml              # Conda environment file
└── README.md                   # This file
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
