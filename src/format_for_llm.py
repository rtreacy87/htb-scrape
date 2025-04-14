def format_for_llm(extracted_content):
    """
    Convert the structured content into a plain text format that's easy for LLMs to process
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
        "list": format_list,
        "image": format_image,
        "table": format_table,
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

def format_list(item):
    """Format a list item"""
    result = []
    for i, list_item in enumerate(item["items"]):
        prefix = f"{i+1}." if item["list_type"] == "ordered" else "-"
        result.append(f"{prefix} {list_item}")
    result.append("")
    return result

def format_image(item):
    """Format an image item"""
    filename = item['src'].split('/')[-1] 
    return [f"[Image: {item['alt']} ({filename})]", ""]
    
def fill_in_table(item):
    """Fill in table item"""
    result = []
    if item.get("headers"):
        result.append("| " + " | ".join(item["headers"]) + " |")
        result.append("| " + " | ".join(["---"] * len(item["headers"])) + " |")
    if item.get("rows"):
        for row in item["rows"]:
            result.append("| " + " | ".join(str(cell) for cell in row) + " |")
    result.append("")
    return result

def format_table(item):
    """Format a table item"""
    if not item.get("headers") and not item.get("rows"):
        return ["[Empty table]", "No headers or rows provided"]
    result = fill_in_table(item)
    return result

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
