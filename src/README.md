# HTB-Scrape Source Code Documentation

This directory contains the source code for the HTB-Scrape tool, which extracts and formats content from HackTheBox Academy HTML pages.

## Overview

The HTB-Scrape tool is designed to extract structured content from HTML pages and format it in a way that's easy to read and process. It's particularly focused on handling HackTheBox Academy pages, but can be used for other HTML content as well.

## File Structure

The source code is organized into several modules, each with a specific responsibility:

| File | Description |
|------|-------------|
| [BaseHTMLExtractor.py](BaseHTMLExtractor.md) | Abstract base class for HTML extraction with core functionality |
| [LLMStructuredExtractor.py](LLMStructuredExtractor.md) | Specialized extractor that creates a hierarchical structure for LLM consumption |
| [htb_scraper_utils.py](htb_scraper_utils.md) | Utility functions for handling command-line arguments, file I/O, and content formatting |
| [fetch_html_from_url.py](fetch_html_from_url.md) | Functions for fetching HTML content from URLs |
| [format_for_llm_structured.py](format_for_llm_structured.md) | Functions for formatting extracted content into LLM-friendly text |
| [image_handler.py](image_handler.md) | Functions for downloading, processing, and handling images |

## Data Flow

The typical data flow through the application is:

1. User provides a URL or file path via command-line arguments (processed by `htb_scraper_utils.py`)
2. HTML content is fetched from the URL or file (using `fetch_html_from_url.py` or file I/O functions)
3. Content is extracted and structured (using `LLMStructuredExtractor.py`)
4. Images are downloaded and processed if requested (using `image_handler.py`)
5. Content is formatted for output (using `format_for_llm_structured.py`)
6. Formatted content is written to a file or displayed to the console (using functions in `htb_scraper_utils.py`)

## Dependencies

The code relies on the following external libraries:
- BeautifulSoup4: For HTML parsing
- Requests: For HTTP requests
- Re: For regular expression operations

## Getting Started

To understand how the code works, start by looking at the main script (`htb_scraper.py` in the root directory), which orchestrates the overall process. Then, explore the individual modules to understand the specific functionality each provides.

For detailed information about each module, refer to the linked README files above.
