import pytest
from src.format_for_llm import format_questions, format_alert, format_table, format_image, format_list, format_code_block, format_paragraph, format_heading

def test_format_questions_basic_SCP_FMT005():
    # Test with basic questions list
    questions = [
        "What is the capital of France?",
        "How many continents are there?"
    ]
    
    result = format_questions(questions)
    
    assert result == [
        "## Questions",
        "",
        "Question 1: What is the capital of France?",
        "",
        "Question 2: How many continents are there?",
        ""
    ]

def test_format_questions_empty_SCP_FMT010():
    # Test with empty questions list
    questions = []
    
    result = format_questions(questions)
    
    assert result == [
        "## Questions",
        ""
    ]

def test_format_questions_single_SCP_FMT015():
    # Test with single question
    questions = ["Single test question?"]
    
    result = format_questions(questions)
    
    assert result == [
        "## Questions",
        "",
        "Question 1: Single test question?",
        ""
    ]

def test_format_questions_with_special_chars_SCP_FMT020():
    # Test with questions containing special characters and formatting
    questions = [
        "Question with *asterisks* and _underscores_?",
        "Question with [brackets] and {braces}!"
    ]
    
    result = format_questions(questions)
    
    assert result == [
        "## Questions",
        "",
        "Question 1: Question with *asterisks* and _underscores_?",
        "",
        "Question 2: Question with [brackets] and {braces}!",
        ""
    ]

def test_format_alert_basic_SCP_FMT025():
    # Test formatting of a basic alert item
    alert_item = {
        "type": "alert",
        "text": "This is an important alert message"
    }
    
    result = format_alert(alert_item)
    
    assert result == [
        "---",
        "Note:",
        "This is an important alert message",
        "---",
        ""
    ]

def test_format_table_SCP_FMT030():
    # Test cases for table formatting
    test_cases = [
        # Case 1: Empty/summary table
        (
            {"type": "table"},
            ["[Empty table]", "No headers or rows provided"]
        ),
        
        # Case 2: Table with headers only
        (
            {
                "type": "table",
                "headers": ["Name", "Age", "City"]
            },
            [
                "| Name | Age | City |",
                "| --- | --- | --- |",
                ""
            ]
        ),
        
        # Case 3: Complete table with headers and rows
        (
            {
                "type": "table",
                "headers": ["Name", "Age", "City"],
                "rows": [
                    ["John", "25", "New York"],
                    ["Alice", "30", "London"]
                ]
            },
            [
                "| Name | Age | City |",
                "| --- | --- | --- |",
                "| John | 25 | New York |",
                "| Alice | 30 | London |",
                ""
            ]
        )
    ]
    
    for input_data, expected_output in test_cases:
        result = format_table(input_data)
        assert result == expected_output

def test_format_image_basic_SCP_FMT035():
    # Test basic image formatting
    image_item = {
        "type": "image",
        "alt": "Test image",
        "src": "test.jpg"
    }
    
    result = format_image(image_item)
    
    assert result == ["[Image: Test image (test.jpg)]", ""]

def test_format_image_empty_alt_SCP_FMT040():
    # Test image with empty alt text
    image_item = {
        "type": "image",
        "alt": "",
        "src": "images/photo.png"
    }
    
    result = format_image(image_item)
    
    assert result == ["[Image:  (photo.png)]", ""]

def test_format_image_special_chars_SCP_FMT045():
    # Test image with special characters in alt text
    image_item = {
        "type": "image",
        "alt": "Test image with *asterisks* and [brackets]",
        "src": "path/to/complex-image_name.jpg"
    }
    
    result = format_image(image_item)
    
    assert result == ["[Image: Test image with *asterisks* and [brackets] (complex-image_name.jpg)]", ""]

def test_format_image_no_path_SCP_FMT050():
    # Test image with just filename in src
    image_item = {
        "type": "image",
        "alt": "Simple image",
        "src": "image.png"
    }
    
    result = format_image(image_item)
    
    assert result == ["[Image: Simple image (image.png)]", ""]

def test_format_list_SCP_FMT045():
    # Test cases for list formatting
    test_cases = [
        # Case 1: Ordered list
        (
            {
                "type": "list",
                "list_type": "ordered",
                "items": ["First item", "Second item", "Third item"]
            },
            [
                "1. First item",
                "2. Second item",
                "3. Third item",
                ""
            ]
        ),
        
        # Case 2: Unordered list
        (
            {
                "type": "list",
                "list_type": "unordered",
                "items": ["Apple", "Banana", "Orange"]
            },
            [
                "- Apple",
                "- Banana",
                "- Orange",
                ""
            ]
        ),
        
        # Case 3: Empty list
        (
            {
                "type": "list",
                "list_type": "ordered",
                "items": []
            },
            [""]
        ),
        
        # Case 4: Single item list
        (
            {
                "type": "list",
                "list_type": "unordered",
                "items": ["Solo item"]
            },
            [
                "- Solo item",
                ""
            ]
        )
    ]
    
    for input_data, expected_output in test_cases:
        result = format_list(input_data)
        assert result == expected_output

def test_format_code_block_SCP_FMT035():
    # Test cases for code block formatting
    test_cases = [
        # Case 1: Code block with language specified
        (
            {
                "type": "code",
                "language": "python",
                "text": "def hello():\n    print('Hello, World!')"
            },
            [
                "```python",
                "def hello():\n    print('Hello, World!')",
                "```",
                ""
            ]
        ),
        
        # Case 2: Code block without language
        (
            {
                "type": "code",
                "language": "",
                "text": "console.log('test');"
            },
            [
                "```",
                "console.log('test');",
                "```",
                ""
            ]
        ),
        
        # Case 3: Empty code block with language
        (
            {
                "type": "code",
                "language": "java",
                "text": ""
            },
            [
                "```java",
                "",
                "```",
                ""
            ]
        )
    ]
    
    for input_data, expected_output in test_cases:
        result = format_code_block(input_data)
        assert result == expected_output

def test_format_paragraph_SCP_FMT025():
    # Test cases for paragraph formatting
    test_cases = [
        # Case 1: Basic paragraph
        (
            {
                "type": "paragraph",
                "text": "This is a simple paragraph."
            },
            [
                "This is a simple paragraph.",
                ""
            ]
        ),
        
        # Case 2: Paragraph with special characters
        (
            {
                "type": "paragraph",
                "text": "Paragraph with *asterisks* and _underscores_!"
            },
            [
                "Paragraph with *asterisks* and _underscores_!",
                ""
            ]
        ),
        
        # Case 3: Empty paragraph
        (
            {
                "type": "paragraph",
                "text": ""
            },
            [
                "",
                ""
            ]
        ),
        
        # Case 4: Paragraph with multiple lines
        (
            {
                "type": "paragraph",
                "text": "First line\nSecond line\nThird line"
            },
            [
                "First line\nSecond line\nThird line",
                ""
            ]
        )
    ]
    
    for input_data, expected_output in test_cases:
        result = format_paragraph(input_data)
        assert result == expected_output

def test_format_heading_SCP_FMT050():
    # Test cases for heading formatting
    test_cases = [
        # Case 1: Level 1 heading
        (
            {
                "type": "heading",
                "level": 1,
                "text": "Main Title"
            },
            [
                "# Main Title",
                ""
            ]
        ),
        
        # Case 2: Level 3 heading
        (
            {
                "type": "heading",
                "level": 3,
                "text": "Subsection Title"
            },
            [
                "### Subsection Title",
                ""
            ]
        ),
        
        # Case 3: Level 6 heading with special characters
        (
            {
                "type": "heading",
                "level": 6,
                "text": "Special *Title* with _formatting_"
            },
            [
                "###### Special *Title* with _formatting_",
                ""
            ]
        ),
        
        # Case 4: Empty heading text
        (
            {
                "type": "heading",
                "level": 2,
                "text": ""
            },
            [
                "## ",
                ""
            ]
        )
    ]
    
    for input_data, expected_output in test_cases:
        result = format_heading(input_data)
        assert result == expected_output



