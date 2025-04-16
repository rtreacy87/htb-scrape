# format_for_llm_structured Module

This document provides a detailed explanation of the `format_for_llm_structured.py` module, which contains functions for formatting structured content into LLM-friendly text.

## Overview

The `format_for_llm_structured.py` module transforms the structured content extracted by `LLMStructuredExtractor` into a format that's easy for language models (LLMs) to consume. It converts the hierarchical JSON structure into a plain text format with appropriate formatting for headings, paragraphs, lists, code blocks, images, and tables.

## Function Details

### `format_for_llm_structured(content)`

This is the main function in the module, responsible for formatting structured content into LLM-friendly text.

#### Parameters
- `content` (dict): The structured content to format, typically from `LLMStructuredExtractor`

#### Returns
- `str`: The formatted content as a string

#### Behavior
1. Formats the title
2. Formats the content items
3. Formats the questions (if any)
4. Joins everything into a single string
5. Returns the formatted string

#### Example Usage
```python
from src.format_for_llm_structured import format_for_llm_structured

formatted_content = format_for_llm_structured(structured_content)
print(formatted_content)
```

### Helper Functions

The module includes several helper functions for formatting specific types of content:

#### `format_title(content)`

Formats the title of the content.

#### Parameters
- `content` (dict): The structured content

#### Returns
- `list`: A list of strings representing the formatted title

#### `format_content_items(content_items)`

Formats a list of content items.

#### Parameters
- `content_items` (list): The list of content items to format

#### Returns
- `list`: A list of strings representing the formatted content items

#### `get_formatter_for_type(item_type)`

Gets the appropriate formatter function for a given item type.

#### Parameters
- `item_type` (str): The type of the item to format

#### Returns
- `function`: The formatter function for the specified item type

### Item Formatters

The module includes formatter functions for each type of content item:

- `format_heading(item)`: Formats a heading item
- `format_paragraph(item)`: Formats a paragraph item
- `format_code_block(item)`: Formats a code block item
- `format_structured_list(item)`: Formats a list item
- `format_image(item)`: Formats an image item
- `format_structured_table(item)`: Formats a table item
- `format_alert(item)`: Formats an alert/note item

Each formatter takes an item dictionary and returns a list of strings representing the formatted item.

### Table Formatting Functions

The module includes specialized functions for formatting tables:

- `format_table_header()`: Formats the table header
- `format_table_row(row)`: Formats a table row
- `format_table_cell(cell)`: Formats a table cell
- `format_cell_image(element)`: Formats an image within a table cell

### Question Formatting

The module includes a function for formatting questions:

- `format_questions(questions)`: Formats a list of questions

## Output Format

The module produces plain text output with the following formatting:

1. **Title**: Formatted as a level 1 heading with `#`
2. **Headings**: Formatted with `#` characters corresponding to the heading level
3. **Paragraphs**: Formatted as plain text with blank lines before and after
4. **Lists**: Formatted with `-` for unordered lists and numbers for ordered lists
5. **Code Blocks**: Formatted with triple backticks and language identifier
6. **Images**: Formatted as Markdown image links or text descriptions
7. **Tables**: Formatted as Markdown tables with pipe characters
8. **Questions**: Formatted as a numbered list under a "Questions" heading

## Integration with Other Modules

The `format_for_llm_structured.py` module integrates with other modules in the following ways:

1. It's imported by `htb_scraper_utils.py` to format content for output
2. It processes the output of `LLMStructuredExtractor.py`
3. It's used indirectly by the main script (`htb_scraper.py`) through `htb_scraper_utils.py`

## Example Output

Here's an example of the output produced by the module:

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

## Best Practices

When using the `format_for_llm_structured.py` module:

1. **Validate Input**: Ensure that the input content has the expected structure
2. **Handle Missing Fields**: Be prepared for cases where fields might be missing
3. **Customize Formatting**: Extend the module with custom formatters if needed
4. **Consider Output Length**: Be mindful of the length of the formatted output, especially for large documents

## Related Files

- [LLMStructuredExtractor.py](LLMStructuredExtractor.md): Produces the structured content that this module formats
- [htb_scraper_utils.py](htb_scraper_utils.md): Uses this module to format content for output
