# LLMStructuredExtractor Module

This document provides a detailed explanation of the `LLMStructuredExtractor.py` module, which extends the `BaseHTMLExtractor` class to create a hierarchical structure optimized for language model consumption.

## Overview

The `LLMStructuredExtractor` class is a concrete implementation of the `BaseHTMLExtractor` abstract base class. It extracts content from HTML and organizes it into a hierarchical structure that's particularly well-suited for language models (LLMs).

## Class Structure

The `LLMStructuredExtractor` class extends `BaseHTMLExtractor` with the following components:

1. **Implementation of Abstract Methods**: Provides concrete implementations of the abstract methods defined in `BaseHTMLExtractor`
2. **Specialized Processing Methods**: Adds methods for processing elements in a way that creates a hierarchical structure
3. **Helper Functions**: Includes utility functions for finding content containers and extracting questions

## Detailed Method Documentation

### Constructor

The constructor inherits from `BaseHTMLExtractor` and doesn't add any additional parameters.

```python
def __init__(self, html_content, base_url=None, download_images=True, image_output_dir='images'):
    super().__init__(html_content, base_url, download_images, image_output_dir)
```

### Implemented Abstract Methods

#### `extract_content()`

Extracts content from HTML and returns structured data.

```python
def extract_content(self):
```

#### Returns
- `dict`: A dictionary containing:
  - `title` (str): The page title
  - `content` (list): List of processed content items with a hierarchical structure
  - `questions` (list, optional): List of questions if any are found

#### Behavior
1. Finds the main content container
2. Extracts the title
3. Processes the content elements
4. Extracts questions
5. Returns a structured dictionary

### Core Processing Methods

#### `find_main_content_container()`

Finds the main content container in the HTML document.

#### Returns
- BeautifulSoup element: The main content container, or None if not found

#### `extract_questions()`

Extracts questions from the HTML document.

#### Returns
- `list`: List of question strings, or an empty list if none are found

#### `process_content_elements(container)`

Processes all content elements in the container.

#### Parameters
- `container`: BeautifulSoup element containing the content to process

#### Returns
- `list`: List of processed content items

#### `_process_elements_in_order(container, content_items, depth=0)`

Recursively processes elements in order with a more structured approach.

#### Parameters
- `container`: BeautifulSoup element to process
- `content_items`: List to append processed items to
- `depth`: Current recursion depth

### Specialized Processing Methods

The class includes several specialized methods for processing different types of elements:

- `_process_list(container, content_items)`: Processes a list element
- `_process_list_item_content(list_item)`: Processes the content of a list item
- `_process_table(container, content_items)`: Processes a table element
- `_process_table_row(row)`: Processes a table row
- `_process_table_cell(cell)`: Processes a table cell
- `_process_special_element(element, content_items, depth)`: Processes special elements like lists and tables
- `_process_image_element(element, content_items)`: Processes an image element
- `_process_standard_element(element, content_items)`: Processes a standard element
- `_process_container_children(element, content_items, depth)`: Processes children of container elements

### Module-Level Function

#### `extract_structured_content_from_html(html_content, base_url=None, download_images=True, image_output_dir='images')`

A convenience function that creates an instance of `LLMStructuredExtractor` and extracts content.

#### Parameters
- `html_content` (str): The HTML content to extract from
- `base_url` (str, optional): Base URL for resolving relative URLs
- `download_images` (bool): Whether to download images
- `image_output_dir` (str): Directory to save downloaded images

#### Returns
- `dict`: The extracted content in a structured format

## Output Structure

The `LLMStructuredExtractor` produces a hierarchical structure with the following format:

```json
{
  "title": "Page Title",
  "content": [
    {
      "type": "heading",
      "level": 1,
      "text": "Heading Text"
    },
    {
      "type": "paragraph",
      "text": "Paragraph text..."
    },
    {
      "type": "list",
      "list_type": "unordered",
      "items": [
        [
          {
            "type": "text",
            "content": "List item text"
          },
          {
            "type": "image",
            "src": "image.jpg",
            "alt": "Image description",
            "local_path": "images/image.jpg"
          }
        ]
      ]
    },
    {
      "type": "table",
      "rows": [
        [
          [
            {
              "type": "text",
              "content": "Cell text"
            }
          ]
        ]
      ]
    }
  ],
  "questions": [
    "Question 1?",
    "Question 2?"
  ]
}
```

## Integration with Other Modules

The `LLMStructuredExtractor` class integrates with other modules in the following ways:

1. It extends `BaseHTMLExtractor` to inherit core functionality
2. It's used by the main script (`htb_scraper.py`) to extract content from HTML
3. Its output is formatted by `format_for_llm_structured.py` for LLM consumption

## Example Usage

Here's an example of how to use the `LLMStructuredExtractor` class:

```python
from src.LLMStructuredExtractor import extract_structured_content_from_html

# Get HTML content
html_content = "<html>...</html>"

# Extract structured content
structured_content = extract_structured_content_from_html(
    html_content,
    base_url="https://example.com",
    download_images=True,
    image_output_dir="images"
)

# Use the structured content
print(f"Title: {structured_content['title']}")
print(f"Content items: {len(structured_content['content'])}")
if 'questions' in structured_content:
    print(f"Questions: {len(structured_content['questions'])}")
```

## Best Practices

When working with the `LLMStructuredExtractor` class:

1. **Use the Convenience Function**: For most cases, use `extract_structured_content_from_html()` instead of creating an instance directly
2. **Handle Missing Elements**: Be prepared for cases where elements might not be found
3. **Process the Output**: The structured output is designed to be further processed by `format_for_llm_structured.py`
4. **Consider Image Handling**: Be mindful of image downloading, especially for large pages

## Related Files

- [BaseHTMLExtractor.py](BaseHTMLExtractor.md): The abstract base class that `LLMStructuredExtractor` extends
- [format_for_llm_structured.py](format_for_llm_structured.md): Formats the output of `LLMStructuredExtractor` for LLM consumption
- [image_handler.py](image_handler.md): Provides image processing functionality used by `LLMStructuredExtractor`
