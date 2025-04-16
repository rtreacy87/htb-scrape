# HTB Scraper Utilities

This document provides a detailed explanation of the `htb_scraper_utils.py` module, which contains utility functions for the HTB-Scrape tool.

## Overview

The `htb_scraper_utils.py` module serves as the backbone of the HTB-Scrape tool, providing essential utilities for:

1. Parsing command-line arguments
2. Reading HTML content from files or URLs
3. Formatting content for output
4. Writing formatted content to files

This module acts as a bridge between the user interface (command-line) and the core functionality of the scraper.

## Dependencies

The module relies on the following:

- `json`: For JSON serialization
- `argparse`: For command-line argument parsing
- `format_for_llm_structured`: For formatting content in a way that's friendly for language models
- `fetch_html_from_url`: For fetching HTML content from URLs

## Function Details

### `parse_arguments()`

This function sets up and processes command-line arguments for the HTB-Scrape tool.

#### Parameters
None

#### Returns
- `argparse.Namespace`: An object containing all the parsed command-line arguments

#### Argument Groups

1. **Input Source** (mutually exclusive, one is required):
   - `--file, -f`: Path to a local HTML file
   - `--url, -u`: URL of the webpage to scrape

2. **Output Options**:
   - `--output, -o`: Output file (default: prints to console)
   - `--format, -m`: Output format, either 'text' or 'json' (default: 'json')

3. **Image Options**:
   - `--download-images, -d`: Whether to download images (default: True)
   - `--image-dir, -i`: Directory to save downloaded images (default: 'images')

#### Example Usage
```python
args = parse_arguments()
if args.file:
    print(f"Processing file: {args.file}")
else:
    print(f"Processing URL: {args.url}")
```

### `get_html_content(args)`

This function retrieves HTML content from either a file or URL, based on the provided arguments.

#### Parameters
- `args` (argparse.Namespace): The parsed command-line arguments

#### Returns
- `tuple`: A tuple containing:
  - The HTML content as a string
  - The file path or URL (used as a base URL for resolving relative paths)

#### Behavior
- If `args.file` is provided, calls `get_content_from_file()`
- Otherwise, calls `get_content_from_url()`

#### Example Usage
```python
content, base_url = get_html_content(args)
if content:
    print(f"Retrieved {len(content)} bytes of HTML content")
else:
    print("Failed to retrieve content")
```

### `get_content_from_file(file_path)`

This function reads HTML content from a local file.

#### Parameters
- `file_path` (str): Path to the HTML file to read

#### Returns
- `tuple`: A tuple containing:
  - The HTML content as a string, or None if an error occurs
  - The file path (used as a base URL for resolving relative paths), or None if an error occurs

#### Error Handling
- Uses a try-except block to catch any exceptions that might occur during file reading
- Prints an error message if an exception occurs
- Returns (None, None) if an error occurs

#### Example Usage
```python
content, file_path = get_content_from_file("example.html")
if content:
    print(f"Read {len(content)} bytes from {file_path}")
else:
    print("Failed to read file")
```

### `get_content_from_url(url)`

This function fetches HTML content from a URL.

#### Parameters
- `url` (str): URL of the webpage to fetch

#### Returns
- `tuple`: A tuple containing:
  - The HTML content as a string, or None if an error occurs
  - The URL (used as a base URL for resolving relative paths), or None if an error occurs

#### Error Handling
- Uses a try-except block to catch any exceptions that might occur during URL fetching
- Prints an error message if an exception occurs
- Returns (None, None) if an error occurs

#### Example Usage
```python
content, url = get_content_from_url("https://example.com")
if content:
    print(f"Fetched {len(content)} bytes from {url}")
else:
    print("Failed to fetch URL")
```

### `output_formatted_content(content, args)`

This function formats and outputs the content based on user preferences.

#### Parameters
- `content` (dict): The structured content to format
- `args` (argparse.Namespace): The parsed command-line arguments

#### Behavior
- Formats the content using `format_content()`
- If `args.output` is provided, writes the formatted content to a file using `write_to_file()`
- Otherwise, prints the formatted content to the console

#### Example Usage
```python
output_formatted_content(extracted_content, args)
```

### `format_content(content, format_type)`

This function formats content as either JSON or LLM-friendly text.

#### Parameters
- `content` (dict): The structured content to format
- `format_type` (str): The format type, either 'json' or 'text'

#### Returns
- `str`: The formatted content as a string

#### Behavior
- If `format_type` is 'json', serializes the content to a JSON string with indentation
- Otherwise, formats the content using `format_for_llm()`

#### Example Usage
```python
json_content = format_content(extracted_content, 'json')
text_content = format_content(extracted_content, 'text')
```

### `write_to_file(content, file_path)`

This function writes content to a file.

#### Parameters
- `content` (str): The content to write
- `file_path` (str): The path of the file to write to

#### Error Handling
- Uses a try-except block to catch any exceptions that might occur during file writing
- Prints an error message if an exception occurs

#### Example Usage
```python
write_to_file("Hello, world!", "output.txt")
```

## Integration with Other Modules

The `htb_scraper_utils.py` module integrates with other modules in the following ways:

1. It imports `format_for_llm_structured` from `src.format_for_llm_structured` to format content for language models
2. It imports `fetch_html_from_url` from `src.fetch_html_from_url` to fetch HTML content from URLs
3. It's imported by the main script (`htb_scraper.py`) to handle command-line arguments and I/O operations

## Error Handling

The module uses try-except blocks to handle errors that might occur during file I/O operations or URL fetching. When an error occurs, it:

1. Prints an error message to the console
2. Returns appropriate values (usually None) to indicate that an error occurred
3. Allows the calling code to handle the error gracefully

## Best Practices

The module follows several best practices:

1. **Separation of Concerns**: Each function has a single, well-defined responsibility
2. **Error Handling**: Uses try-except blocks to catch and handle errors
3. **Documentation**: Includes docstrings for all functions
4. **Modularity**: Breaks down functionality into small, reusable functions
5. **Clear Naming**: Uses descriptive function and variable names

## Example Workflow

Here's an example of how the functions in this module might be used together:

```python
# Parse command-line arguments
args = parse_arguments()

# Get HTML content
content, base_url = get_html_content(args)
if not content:
    print("Failed to retrieve content")
    exit(1)

# Process the content (using other modules)
processed_content = process_content(content, base_url)

# Output the formatted content
output_formatted_content(processed_content, args)
```

This workflow demonstrates how the module provides a complete pipeline from command-line arguments to formatted output.
