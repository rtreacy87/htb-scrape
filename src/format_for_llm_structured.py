def format_for_llm_structured(extracted_content):
    """
    Convert the structured content into a plain text format that's easy for LLMs to process

    This formatter handles the hierarchical structure created by LLMStructuredExtractor
    """
    output_lines = []
    output_lines.extend(format_title(extracted_content))
    output_lines.extend(format_content_items(extracted_content["content"]))
    if "questions" in extracted_content:
        output_lines.extend(format_questions(extracted_content["questions"]))
    return "\n".join(output_lines)

def format_title(content):
    """Format the title section"""
    if 'title' in content:
        return [f"# {content['title']}", ""]
    return []

def format_content_items(content_items):
    """Format all content items"""
    output_lines = []
    for item in content_items:
        formatter = get_formatter_for_type(item["type"])
        if formatter:
            output_lines.extend(formatter(item))
    return output_lines

def get_formatter_for_type(item_type):
    """Return the appropriate formatter function for the given item type"""
    formatters = {
        "heading": format_heading,
        "paragraph": format_paragraph,
        "code": format_code_block,
        "list": format_structured_list,
        "image": format_image,
        "table": format_structured_table,
        "alert": format_alert
    }
    return formatters.get(item_type)

def format_heading(item):
    """Format a heading item"""
    prefix = "#" * item["level"]
    return [f"{prefix} {item['text']}", ""]

def format_paragraph(item):
    """Format a paragraph item"""
    return [item["text"], ""]

def format_code_block(item):
    """Format a code block item"""
    language = item["language"] if item["language"] else ""
    return [f"```{language}", item["text"], "```", ""]

def format_structured_list(item):
    """Format a structured list item with embedded images"""
    result = []
    list_type = item["list_type"]
    for i, list_item in enumerate(item["items"]):
        # Each list item is an array of content elements
        prefix = f"{i+1}." if list_type == "ordered" else "-"
        # Process the first element (usually text)
        if list_item and list_item[0]["type"] == "text":
            result.append(f"{prefix} {list_item[0]['content']}")
        else:
            result.append(f"{prefix} ")
        # Process any additional elements (usually images)
        for j in range(1, len(list_item)):
            sub_item = list_item[j]
            if sub_item["type"] == "image":
                # Format the image with indentation
                image_lines = format_image(sub_item)
                for line in image_lines:
                    if line:  # Skip empty lines
                        result.append(f"  {line}")
    result.append("")
    return result

def format_image(item):
    """Format an image item"""
    # Get the filename from either the source URL or local path
    if 'local_path' in item and item['local_path']:
        # Use the local path if available
        image_ref = item['local_path']
        return [f"![{item['alt']}]({image_ref})", ""]
    else:
        # Fall back to just showing the filename from the source URL
        filename = item['src'].split('/')[-1]
        return [f"[Image: {item['alt']} ({filename})]", ""]

def format_structured_table(item):
    """Format a structured table item with embedded images"""
    result = [""]
    result.extend(format_table_header())

    for row in item["rows"]:
        result.append(format_table_row(row))

    result.append("")
    return result

def format_table_header():
    """Format the table header"""
    return ["| Table Content |", "| ------------- |"]

def format_table_row(row):
    """Format a table row
    Args:
        row: List of cells in the row
    Returns:
        str: Formatted table row
    """
    row_content = []
    for cell in row:
        row_content.append(format_table_cell(cell))

    return f"| {' | '.join(row_content)} |"

def format_table_cell(cell):
    """Format a table cell with its content
    Args:
        cell: List of elements in the cell
    Returns:
        str: Formatted cell content
    """
    cell_text = []
    for element in cell:
        if element["type"] == "text":
            cell_text.append(element["content"])
        elif element["type"] == "image":
            cell_text.append(format_cell_image(element))

    return " ".join(cell_text)

def format_cell_image(element):
    """Format an image within a table cell
    Args:
        element: Image element
    Returns:
        str: Formatted image reference
    """
    if 'local_path' in element and element['local_path']:
        return f"![{element['alt']}]({element['local_path']})"
    else:
        filename = element['src'].split('/')[-1]
        return f"[Image: {element['alt']} ({filename})]"

def format_alert(item):
    """Format an alert/note item"""
    return ["---", "Note:", item["text"], "---", ""]

def format_questions(questions):
    """Format the questions section"""
    result = ["## Questions", ""]
    for i, question in enumerate(questions):
        result.append(f"Question {i+1}: {question}")
        result.append("")
    return result
