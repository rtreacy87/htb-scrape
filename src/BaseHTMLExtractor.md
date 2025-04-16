# BaseHTMLExtractor Module

This document provides a detailed explanation of the `BaseHTMLExtractor.py` module, which serves as the abstract base class for HTML extraction in the HTB-Scrape tool.

## Overview

The `BaseHTMLExtractor` class is an abstract base class that provides core functionality for extracting content from HTML. It defines the interface and common methods that all HTML extractors in the system should implement.

## Class Structure

The `BaseHTMLExtractor` class is designed with the following components:

1. **Initialization**: Sets up the extractor with HTML content and configuration options
2. **Abstract Methods**: Define the interface that concrete extractors must implement
3. **Utility Methods**: Provide common functionality for HTML processing
4. **Element Processors**: Methods for processing specific types of HTML elements

## Detailed Method Documentation

### Constructor

```python
def __init__(self, html_content, base_url=None, download_images=True, image_output_dir='images', max_depth=10):
```

#### Parameters
- `html_content` (str): The HTML content to extract from
- `base_url` (str, optional): Base URL for resolving relative URLs
- `download_images` (bool): Whether to download images
- `image_output_dir` (str): Directory to save downloaded images
- `max_depth` (int): Maximum recursion depth for processing nested elements

#### Behavior
- Initializes the BeautifulSoup parser with the HTML content
- Sets up configuration options for image handling and recursion depth
- Initializes the element processor map

### Abstract Methods

#### `extract_content()`

This abstract method must be implemented by concrete extractors to extract content from HTML.

```python
def extract_content(self):
    """Extract content from HTML and return structured data."""
    raise NotImplementedError("Subclasses must implement extract_content()")
```

#### Returns
- `dict`: A dictionary containing the extracted content

### Core Processing Methods

#### `process_content_elements(container)`

Processes all content elements in the container.

#### Parameters
- `container`: BeautifulSoup element containing the content to process

#### Returns
- `list`: List of processed content items

#### `_process_elements_in_order(container, content_items, depth=0)`

Recursively processes elements in order.

#### Parameters
- `container`: BeautifulSoup element to process
- `content_items`: List to append processed items to
- `depth`: Current recursion depth

### Element Processors

The class includes methods for processing various types of HTML elements:

- `process_code_block(element)`: Processes a code block element
- `process_paragraph(element)`: Processes a paragraph element
- `process_image(element)`: Processes an image element
- `process_alert(element)`: Processes an alert/note element
- `process_list(element)`: Processes a list element
- `process_heading(element)`: Processes a heading element
- `process_table(element)`: Processes a table element

Each processor extracts relevant information from the element and returns a structured representation.

### Utility Methods

#### `extract_title()`

Extracts the title from the HTML document.

#### Returns
- `str`: The extracted title

#### `is_valid_element(element)`

Checks if an element is valid for processing.

#### Parameters
- `element`: BeautifulSoup element to check

#### Returns
- `bool`: True if the element is valid, False otherwise

#### `get_element_processor_map()`

Gets a mapping of HTML elements to their processor methods.

#### Returns
- `dict`: A dictionary mapping element names to processor methods

## Integration with Other Modules

The `BaseHTMLExtractor` class integrates with other modules in the following ways:

1. It's extended by `LLMStructuredExtractor` to provide specialized extraction for LLM consumption
2. It uses `image_handler.process_image_element` for processing image elements

## Example Usage

Here's an example of how to extend and use the `BaseHTMLExtractor` class:

```python
class MyHTMLExtractor(BaseHTMLExtractor):
    def extract_content(self):
        content_container = self.find_main_content_container()
        if not content_container:
            return {"title": "Error", "content": []}
        
        title = self.extract_title()
        content_items = self.process_content_elements(content_container)
        
        return {
            "title": title,
            "content": content_items
        }
    
    def find_main_content_container(self):
        # Custom logic to find the main content container
        return self.soup.find('div', class_='content')

# Usage
extractor = MyHTMLExtractor(html_content)
extracted_content = extractor.extract_content()
```

## Best Practices

When working with the `BaseHTMLExtractor` class:

1. **Extend, Don't Modify**: Create a subclass instead of modifying the base class
2. **Implement Required Methods**: Make sure to implement all abstract methods
3. **Respect the Interface**: Follow the established patterns for processing elements
4. **Handle Edge Cases**: Be prepared for malformed HTML and missing elements
5. **Limit Recursion**: Be mindful of the recursion depth to avoid stack overflow

## Related Files

- [LLMStructuredExtractor.py](LLMStructuredExtractor.md): A concrete implementation of `BaseHTMLExtractor`
- [image_handler.py](image_handler.md): Provides image processing functionality used by `BaseHTMLExtractor`
