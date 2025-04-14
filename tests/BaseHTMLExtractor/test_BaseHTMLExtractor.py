import pytest
from bs4 import BeautifulSoup, Comment
from src.BaseHTMLExtractor import BaseHTMLExtractor

class TestHTMLExtractor:
    """Test class for BaseHTMLExtractor static methods"""
    @staticmethod
    def process_code_block(element):
        return BaseHTMLExtractor.process_code_block(element)

    @staticmethod
    def process_paragraph(element):
        return BaseHTMLExtractor.process_paragraph(element)

def test_process_code_block_with_language_SCP_BHTML005():
    # Test code block with language specified
    test_html = '<pre class="language-python">def test(): pass</pre>'
    element = BeautifulSoup(test_html, 'html.parser').find('pre')

    result = TestHTMLExtractor.process_code_block(element)

    assert result["type"] == "code"
    assert result["language"] == "python"
    assert result["text"] == "def test(): pass"

def test_process_code_block_without_language_SCP_BHTML010():
    # Test code block without language
    test_html = '<pre>print("hello")</pre>'
    element = BeautifulSoup(test_html, 'html.parser').find('pre')

    result = TestHTMLExtractor.process_code_block(element)

    assert result["type"] == "code"
    assert result["language"] == ""
    assert result["text"] == 'print("hello")'

def test_process_code_block_multiple_classes_SCP_BHTML015():
    # Test code block with multiple classes
    test_html = '<pre class="highlight language-javascript code-block">const x = 1;</pre>'
    element = BeautifulSoup(test_html, 'html.parser').find('pre')

    result = TestHTMLExtractor.process_code_block(element)

    assert result["type"] == "code"
    assert result["language"] == "javascript"
    assert result["text"] == "const x = 1;"

def test_process_code_block_empty_SCP_BHTML020():
    # Test empty code block
    test_html = '<pre class="language-ruby">    </pre>'
    element = BeautifulSoup(test_html, 'html.parser').find('pre')

    result = TestHTMLExtractor.process_code_block(element)

    assert result["type"] == "code"
    assert result["language"] == "ruby"
    assert result["text"] == ""

def test_process_paragraph_with_text_SCP_BHTML025():
    # Test paragraph with regular text
    test_html = '<p>This is a test paragraph.</p>'
    element = BeautifulSoup(test_html, 'html.parser').find('p')

    result = BaseHTMLExtractor.process_paragraph(element)

    assert result["type"] == "paragraph"
    assert result["text"] == "This is a test paragraph."

def test_process_paragraph_empty_SCP_BHTML030():
    # Test empty paragraph
    test_html = '<p>    </p>'
    element = BeautifulSoup(test_html, 'html.parser').find('p')

    result = BaseHTMLExtractor.process_paragraph(element)

    assert result is None

def test_process_paragraph_with_nested_elements_SCP_BHTML035():
    # Test paragraph with nested elements
    test_html = '<p>Text with <strong>bold</strong> and <em>italic</em> content.</p>'
    element = BeautifulSoup(test_html, 'html.parser').find('p')

    result = BaseHTMLExtractor.process_paragraph(element)

    assert result["type"] == "paragraph"
    assert result["text"] == "Text with bold and italic content."

def test_process_paragraph_with_newlines_SCP_BHTML040():
    # Test paragraph with newlines and extra spaces
    test_html = '<p>\n    Multiple\n    lines with    spaces\n</p>'
    element = BeautifulSoup(test_html, 'html.parser').find('p')

    result = BaseHTMLExtractor.process_paragraph(element)

    assert result["type"] == "paragraph"
    assert result["text"] == "Multiple lines with spaces"

def test_process_image_with_src_and_alt_SCP_BHTML045():
    # Test image with both src and alt attributes
    test_html = '<img src="test.jpg" alt="Test Image">'
    element = BeautifulSoup(test_html, 'html.parser').find('img')

    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    extractor = TestExtractor("<html></html>")
    result = extractor.process_image(element)

    assert result["type"] == "image"
    assert result["src"] == "test.jpg"
    assert result["alt"] == "Test Image"

def test_process_image_without_alt_SCP_BHTML050():
    # Test image without alt attribute
    test_html = '<img src="test.jpg">'
    element = BeautifulSoup(test_html, 'html.parser').find('img')

    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    extractor = TestExtractor("<html></html>")
    result = extractor.process_image(element)

    assert result["type"] == "image"
    assert result["src"] == "test.jpg"
    assert result["alt"] == "Image"  # Should default to "Image"

def test_process_image_empty_attributes_SCP_BHTML055():
    # Test image with empty attributes
    test_html = '<img src="" alt="">'
    element = BeautifulSoup(test_html, 'html.parser').find('img')

    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    extractor = TestExtractor("<html></html>")
    result = extractor.process_image(element)

    assert result["type"] == "image"
    assert result["src"] == ""
    assert result["alt"] == "Image"  # Should default to "Image" when alt is empty

def test_process_alert_with_text_SCP_BHTML060():
    # Test alert with regular text
    test_html = '<div class="card">This is an alert message</div>'
    element = BeautifulSoup(test_html, 'html.parser').find('div')

    result = BaseHTMLExtractor.process_alert(element)

    assert result["type"] == "alert"
    assert result["text"] == "This is an alert message"

def test_process_alert_with_nested_elements_SCP_BHTML065():
    # Test alert with nested elements
    test_html = '<div class="card"><strong>Warning:</strong> Important alert <em>message</em></div>'
    element = BeautifulSoup(test_html, 'html.parser').find('div')

    result = BaseHTMLExtractor.process_alert(element)

    assert result["type"] == "alert"
    assert result["text"] == "Warning: Important alert message"

def test_process_alert_empty_SCP_BHTML070():
    # Test empty alert
    test_html = '<div class="card">    </div>'
    element = BeautifulSoup(test_html, 'html.parser').find('div')

    result = BaseHTMLExtractor.process_alert(element)

    assert result is None


def test_process_alert_with_newlines_SCP_BHTML075():
    # Test alert with newlines and extra spaces
    test_html = '<div class="card">\n    Multiple\n    lines with    spaces\n</div>'
    element = BeautifulSoup(test_html, 'html.parser').find('div')

    result = BaseHTMLExtractor.process_alert(element)

    assert result["type"] == "alert"
    assert result["text"] == "Multiple lines with spaces"

def test_process_table_basic_SCP_BHTML080():
    # Test basic table processing
    test_html = '''
        <table>
            <tr>
                <th>Header 1</th>
                <th>Header 2</th>
            </tr>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
            </tr>
        </table>
    '''
    element = BeautifulSoup(test_html, 'html.parser').find('table')

    result = BaseHTMLExtractor.process_table(element)

    assert result["type"] == "table"
    assert result["text"] == "Table content (summarized for brevity)"

def test_process_list_ordered_SCP_BHTML085():
    # Test ordered list processing
    test_html = '''
        <ol>
            <li>First item</li>
            <li>Second item</li>
            <li>Third item</li>
        </ol>
    '''
    element = BeautifulSoup(test_html, 'html.parser').find('ol')

    result = BaseHTMLExtractor.process_list(element)

    assert result["type"] == "list"
    assert result["list_type"] == "ordered"
    assert result["items"] == ["First item", "Second item", "Third item"]

def test_process_list_unordered_SCP_BHTML090():
    # Test unordered list processing
    test_html = '''
        <ul>
            <li>Apple</li>
            <li>Banana</li>
            <li>Orange</li>
        </ul>
    '''
    element = BeautifulSoup(test_html, 'html.parser').find('ul')

    result = BaseHTMLExtractor.process_list(element)

    assert result["type"] == "list"
    assert result["list_type"] == "unordered"
    assert result["items"] == ["Apple", "Banana", "Orange"]

def test_process_list_with_nested_elements_SCP_BHTML095():
    # Test list with nested HTML elements
    test_html = '''
        <ul>
            <li>Plain text</li>
            <li>Text with <strong>bold</strong> content</li>
            <li>Text with <em>italic</em> and <code>code</code></li>
        </ul>
    '''
    element = BeautifulSoup(test_html, 'html.parser').find('ul')

    result = BaseHTMLExtractor.process_list(element)

    assert result["type"] == "list"
    assert result["list_type"] == "unordered"
    assert result["items"] == [
        "Plain text",
        "Text with bold content",
        "Text with italic and code"
    ]

def test_process_list_empty_SCP_BHTML100():
    # Test empty list
    test_html = '''
        <ol>
            <li>    </li>
            <li></li>
        </ol>
    '''
    element = BeautifulSoup(test_html, 'html.parser').find('ol')

    result = BaseHTMLExtractor.process_list(element)

    assert result["type"] == "list"
    assert result["list_type"] == "ordered"
    assert result["items"] == ["", ""]

def test_process_heading_basic_SCP_BHTML105():
    # Test basic heading processing for different levels
    test_cases = [
        ('<h1>Main Title</h1>', 1, "Main Title"),
        ('<h2>Subtitle</h2>', 2, "Subtitle"),
        ('<h3>Section Header</h3>', 3, "Section Header"),
        ('<h4>Subsection</h4>', 4, "Subsection"),
        ('<h5>Minor Header</h5>', 5, "Minor Header"),
        ('<h6>Smallest Header</h6>', 6, "Smallest Header")
    ]

    for html, expected_level, expected_text in test_cases:
        element = BeautifulSoup(html, 'html.parser').find(f'h{expected_level}')
        result = BaseHTMLExtractor.process_heading(element)

        assert result["type"] == "heading"
        assert result["level"] == expected_level
        assert result["text"] == expected_text

def test_process_heading_with_nested_elements_SCP_BHTML110():
    # Test heading with nested HTML elements
    test_html = '<h2>Title with <strong>bold</strong> and <em>italic</em> text</h2>'
    element = BeautifulSoup(test_html, 'html.parser').find('h2')

    result = BaseHTMLExtractor.process_heading(element)

    assert result["type"] == "heading"
    assert result["level"] == 2
    assert result["text"] == "Title with bold and italic text"

def test_process_heading_with_whitespace_SCP_BHTML115():
    # Test heading with extra whitespace
    test_html = '<h1>\n    Heading with    extra\n    spaces    \n</h1>'
    element = BeautifulSoup(test_html, 'html.parser').find('h1')

    result = BaseHTMLExtractor.process_heading(element)

    assert result["type"] == "heading"
    assert result["level"] == 1
    assert result["text"] == "Heading with extra spaces"

def test_process_content_elements_mixed_content_SCP_BHTML120():
    # Test processing of mixed content elements
    test_html = """
        <div>
            <h1>Main Title</h1>
            <p>First paragraph</p>
            <pre class="language-python">def test(): pass</pre>
            <div class="card">Alert message</div>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
            <!-- This comment should be ignored -->
            <span>This span should be ignored</span>
            <p>    </p>
        </div>
    """

    # Create a BaseHTMLExtractor instance with a concrete implementation
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    extractor = TestExtractor(test_html)
    container = BeautifulSoup(test_html, 'html.parser').find('div')
    result = extractor.process_content_elements(container)

    # Verify the number of processed items (empty paragraph and ignored elements should be filtered out)
    # We now expect 7 items because list items are processed as paragraphs
    assert len(result) == 7

    # Verify each processed item
    assert result[0] == {
        "type": "heading",
        "level": 1,
        "text": "Main Title"
    }

    assert result[1] == {
        "type": "paragraph",
        "text": "First paragraph"
    }

    assert result[2] == {
        "type": "code",
        "language": "python",
        "text": "def test(): pass"
    }

    assert result[3] == {
        "type": "alert",
        "text": "Alert message"
    }

    assert result[4] == {
        "type": "list",
        "list_type": "unordered",
        "items": ["Item 1", "Item 2"]
    }

def test_process_single_element_SCP_BHTML125():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test cases with different HTML elements
    test_cases = [
        # Standard paragraph
        ('<p>Test paragraph</p>',
         {"type": "paragraph", "text": "Test paragraph"}),

        # Code block with language
        ('<pre class="language-python">def test(): pass</pre>',
         {"type": "code", "language": "python", "text": "def test(): pass"}),

        # Alert div
        ('<div class="card">Alert message</div>',
         {"type": "alert", "text": "Alert message"}),

        # Invalid element (plain text node)
        ('Plain text', None),

        # Regular div (should be ignored)
        ('<div>Regular div</div>', None),

        # Empty paragraph
        ('<p>    </p>', None)
    ]

    extractor = TestExtractor("<html></html>")  # Dummy HTML content
    element_processors = extractor.get_element_processor_map()

    for html, expected_result in test_cases:
        # Parse HTML string to create BeautifulSoup element
        element = BeautifulSoup(html, 'html.parser').children.__next__()

        # Process the element
        result = extractor.process_single_element(element, element_processors)

        # Verify result matches expected output
        assert result == expected_result

def test_is_valid_element_SCP_BHTML130():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test cases with different types of elements
    test_html = """
        <div>
            <p>Test paragraph</p>
            <!-- Comment -->
            Plain text node
        </div>
    """

    soup = BeautifulSoup(test_html, 'html.parser')
    extractor = TestExtractor("<html></html>")  # Dummy HTML content

    # Test valid HTML element (div)
    div_element = soup.find('div')
    assert extractor.is_valid_element(div_element) == True

    # Test valid HTML element (p)
    p_element = soup.find('p')
    assert extractor.is_valid_element(p_element) == True

    # Test comment node
    comment = soup.find(string=lambda text: isinstance(text, Comment))
    assert extractor.is_valid_element(comment) == False

    # Test plain text node
    text_node = soup.find(string="Plain text node")
    assert extractor.is_valid_element(text_node) == False

    # Test None value
    assert extractor.is_valid_element(None) == False

def test_get_element_processor_map_SCP_BHTML135():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    extractor = TestExtractor("<html></html>")  # Dummy HTML content
    processor_map = extractor.get_element_processor_map()

    # Verify all expected HTML elements are mapped
    expected_elements = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre',
                        'ol', 'ul', 'img', 'table']
    assert set(processor_map.keys()) == set(expected_elements)

    # Verify each processor maps to the correct method
    assert processor_map['h1'] == extractor.process_heading
    assert processor_map['h2'] == extractor.process_heading
    assert processor_map['h3'] == extractor.process_heading
    assert processor_map['h4'] == extractor.process_heading
    assert processor_map['h5'] == extractor.process_heading
    assert processor_map['h6'] == extractor.process_heading
    assert processor_map['p'] == extractor.process_paragraph
    assert processor_map['pre'] == extractor.process_code_block
    assert processor_map['ol'] == extractor.process_list
    assert processor_map['ul'] == extractor.process_list
    assert processor_map['img'] == extractor.process_image
    assert processor_map['table'] == extractor.process_table

def test_extract_title_SCP_BHTML140():
    # Create a concrete implementation for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test cases for different title scenarios
    test_cases = [
        # Case 1: h4 with page-title class (highest precedence)
        ("""
        <html>
            <title>Document Title</title>
            <h1 class="page-title">H1 Page Title</h1>
            <h1>Regular H1</h1>
            <h4 class="page-title">H4 Page Title</h4>
        </html>
        """, "H4 Page Title"),

        # Case 2: h1 with page-title class (second precedence)
        ("""
        <html>
            <title>Document Title</title>
            <h1 class="page-title">H1 Page Title</h1>
            <h1>Regular H1</h1>
        </html>
        """, "H1 Page Title"),

        # Case 3: first h1 tag (third precedence)
        ("""
        <html>
            <title>Document Title</title>
            <h1>Regular H1</h1>
        </html>
        """, "Regular H1"),

        # Case 4: title tag (fourth precedence)
        ("""
        <html>
            <title>Document Title</title>
        </html>
        """, "Document Title"),

        # Case 5: no title elements (fallback)
        ("""
        <html>
            <body>
                <p>Some content</p>
            </body>
        </html>
        """, "Unknown Title"),

        # Case 6: empty title elements
        ("""
        <html>
            <title>    </title>
            <h1>    </h1>
            <h4 class="page-title">    </h4>
        </html>
        """, "Unknown Title")
    ]

    # Run all test cases
    for html, expected_title in test_cases:
        extractor = TestExtractor(html)
        assert extractor.extract_title() == expected_title

def test_process_container_children_SCP_BHTML140():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test HTML with nested container elements
    test_html = """
        <div>
            <p>Paragraph 1</p>
            <section>
                <img src="test1.jpg" alt="Test 1">
                <figure>
                    <img src="test2.jpg" alt="Test 2">
                </figure>
            </section>
            <article>
                <table>
                    <tr>
                        <td><img src="test3.jpg" alt="Test 3"></td>
                    </tr>
                </table>
                <ul>
                    <li>Item with <img src="test4.jpg" alt="Test 4"></li>
                </ul>
            </article>
        </div>
    """

    extractor = TestExtractor("<html></html>")  # Dummy HTML content
    container = BeautifulSoup(test_html, 'html.parser').find('div')
    content_items = []

    # Process the container children
    extractor._process_container_children(container, content_items, 0)

    # Verify that all nested images were processed
    image_sources = [item["src"] for item in content_items if item["type"] == "image"]
    expected_sources = ["test1.jpg", "test2.jpg", "test3.jpg", "test4.jpg"]

    assert len(image_sources) == 4
    assert set(image_sources) == set(expected_sources)

    # Test max depth limit
    content_items_depth = []
    extractor._process_container_children(container, content_items_depth, extractor.max_depth)
    assert len(content_items_depth) == 0  # Should not process anything at max depth

def test_process_standard_element_SCP_BHTML145():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test cases with different HTML elements
    test_cases = [
        # Regular paragraph
        ('<p>Test paragraph</p>',
         {"type": "paragraph", "text": "Test paragraph"}),

        # Heading
        ('<h2>Test heading</h2>',
         {"type": "heading", "level": 2, "text": "Test heading"}),

        # Code block
        ('<pre class="language-python">def test(): pass</pre>',
         {"type": "code", "language": "python", "text": "def test(): pass"}),

        # Empty paragraph (should not be added to content_items)
        ('<p>    </p>', None),

        # Alert div
        ('<div class="card">Alert message</div>',
         {"type": "alert", "text": "Alert message"})
    ]

    for html, expected_result in test_cases:
        # Setup
        extractor = TestExtractor("<html></html>")  # Dummy HTML content
        content_items = []
        element = BeautifulSoup(html, 'html.parser').children.__next__()

        # Execute
        extractor._process_standard_element(element, content_items)

        # Verify
        if expected_result is None:
            assert len(content_items) == 0
        else:
            assert len(content_items) == 1
            assert content_items[0] == expected_result

def test_process_table_cell_SCP_BHTML150():
    # Test cases for table cell processing
    test_cases = [
        # Case 1: Cell with text only
        ('<td>Sample text</td>',
         [{"type": "paragraph", "text": "Sample text"}]),

        # Case 2: Cell with image only
        ('<td><img src="test.jpg" alt="Test Image"></td>',
         [{"type": "image", "src": "test.jpg", "alt": "Test Image"}]),

        # Case 3: Cell with both text and image
        ('''<td>
                Sample text
                <img src="test.jpg" alt="Test Image">
            </td>''',
         [
             {"type": "paragraph", "text": "Sample text"},
             {"type": "image", "src": "test.jpg", "alt": "Test Image"}
         ]),

        # Case 4: Empty cell
        ('<td>    </td>', []),

        # Case 5: Cell with multiple images
        ('''<td>
                <img src="test1.jpg" alt="Test Image 1">
                <img src="test2.jpg" alt="Test Image 2">
            </td>''',
         [
             {"type": "image", "src": "test1.jpg", "alt": "Test Image 1"},
             {"type": "image", "src": "test2.jpg", "alt": "Test Image 2"}
         ])
    ]

    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    for html, expected_items in test_cases:
        # Setup
        extractor = TestExtractor("<html></html>")  # Dummy HTML content
        content_items = []
        element = BeautifulSoup(html, 'html.parser').find(['td', 'th'])

        # Execute
        extractor._process_table_cell(element, content_items)

        # Assert
        assert len(content_items) == len(expected_items)
        for actual, expected in zip(content_items, expected_items):
            # Check all expected keys are present with correct values
            for key, value in expected.items():
                assert key in actual
                assert actual[key] == value

def test_process_list_item_SCP_BHTML155():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test cases for list item processing
    test_cases = [
        # Case 1: List item with text only
        ('<li>Simple list item</li>',
         [{"type": "paragraph", "text": "Simple list item"}]),

        # Case 2: List item with image only
        ('<li><img src="test.jpg" alt="Test Image"></li>',
         [{"type": "image", "src": "test.jpg", "alt": "Test Image"}]),

        # Case 3: List item with both text and image
        ('''<li>
                List item with image
                <img src="test.jpg" alt="Test Image">
            </li>''',
         [
             {"type": "paragraph", "text": "List item with image"},
             {"type": "image", "src": "test.jpg", "alt": "Test Image"}
         ]),

        # Case 4: Empty list item
        ('<li>    </li>', [])
    ]

    for html, expected_items in test_cases:
        # Setup
        extractor = TestExtractor("<html></html>")  # Dummy HTML content
        content_items = []
        element = BeautifulSoup(html, 'html.parser').find('li')

        # Execute
        extractor._process_list_item(element, content_items)

        # Assert
        assert len(content_items) == len(expected_items)
        for actual, expected in zip(content_items, expected_items):
            # Check all expected keys are present with correct values
            for key, value in expected.items():
                assert key in actual
                assert actual[key] == value

def test_process_image_element_SCP_BHTML160():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test cases for image element processing
    test_cases = [
        # Case 1: Valid image with src and alt
        ('<img src="test.jpg" alt="Test Image">',
         {"type": "image", "src": "test.jpg", "alt": "Test Image"}),

        # Case 2: Image with src only
        ('<img src="photo.png">',
         {"type": "image", "src": "photo.png", "alt": "Image"}),

        # Case 3: Invalid image without src
        ('<img alt="No Source">', None)
    ]

    for html, expected_result in test_cases:
        # Setup
        extractor = TestExtractor("<html></html>")  # Dummy HTML content
        content_items = []
        element = BeautifulSoup(html, 'html.parser').find('img')

        # Execute
        extractor._process_image_element(element, content_items)

        # Assert
        if expected_result is None:
            assert len(content_items) == 0
        else:
            assert len(content_items) == 1
            # Check all expected keys are present with correct values
            for key, value in expected_result.items():
                assert key in content_items[0]
                assert content_items[0][key] == value

def test_should_stop_recursion_SCP_BHTML165():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test cases with different depth values
    test_cases = [
        (0, False),    # Depth 0 should not stop
        (3, False),    # Depth 3 should not stop (assuming default max_depth=5)
        (5, False),    # Depth 5 should not stop (at max_depth)
        (6, True),     # Depth 6 should stop (exceeds max_depth)
        (10, True)     # Depth 10 should definitely stop
    ]

    extractor = TestExtractor("<html></html>")  # Dummy HTML content

    for depth, should_stop in test_cases:
        result = extractor._should_stop_recursion(depth)
        assert result == should_stop, f"Failed at depth {depth}, expected {should_stop} but got {result}"

    # Test with custom max_depth
    extractor_custom = TestExtractor("<html></html>", max_depth=2)
    assert extractor_custom._should_stop_recursion(3) == True
    assert extractor_custom._should_stop_recursion(2) == False

def test_process_elements_in_order_SCP_BHTML170():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test HTML with mixed content types in specific order
    test_html = """
        <div>
            <h1>Main Title</h1>
            <p>First paragraph</p>
            <img src="test1.jpg" alt="Test 1">
            <ul>
                <li>List item with <img src="test2.jpg" alt="Test 2"> image</li>
            </ul>
            <table>
                <tr>
                    <td>Table cell with <img src="test3.jpg" alt="Test 3"> image</td>
                </tr>
            </table>
            <div class="nested">
                <p>Nested paragraph</p>
            </div>
        </div>
    """

    # Setup
    extractor = TestExtractor("<html></html>")  # Dummy HTML content
    container = BeautifulSoup(test_html, 'html.parser').find('div')
    content_items = []

    # Execute
    extractor._process_elements_in_order(container, content_items)


    # Assert
    # Should have 10 items: heading, paragraph, image1, list (unordered), list-item text, image2,
    # table cell text, image3, nested paragraph
    assert len(content_items) == 10

    # Verify order and content of processed items
    # Item 0: Heading
    assert content_items[0]["type"] == "heading"
    assert content_items[0]["level"] == 1
    assert content_items[0]["text"] == "Main Title"

    # Item 1: Paragraph
    assert content_items[1]["type"] == "paragraph"
    assert content_items[1]["text"] == "First paragraph"

    # Item 2: Image 1
    assert content_items[2]["type"] == "image"
    assert content_items[2]["src"] == "test1.jpg"
    assert content_items[2]["alt"] == "Test 1"

    # Item 3: List (unordered)
    assert content_items[3]["type"] == "list"
    assert content_items[3]["list_type"] == "unordered"

    # Item 4: List item text
    assert content_items[4]["type"] == "paragraph"
    assert "List item with" in content_items[4]["text"]

    # Item 5: Image 2
    assert content_items[5]["type"] == "image"
    assert content_items[5]["src"] == "test2.jpg"
    assert content_items[5]["alt"] == "Test 2"

    # Item 6: Table
    assert content_items[6]["type"] == "table"

    # Item 7: Table cell text
    assert content_items[7]["type"] == "paragraph"
    assert "Table cell with" in content_items[7]["text"]

    # Item 8: Image 3
    assert content_items[8]["type"] == "image"
    assert content_items[8]["src"] == "test3.jpg"
    assert content_items[8]["alt"] == "Test 3"

    # Item 9: Nested paragraph
    assert content_items[9]["type"] == "paragraph"
    assert content_items[9]["text"] == "Nested paragraph"

    # Test recursion depth limit
    extractor_limited = TestExtractor("<html></html>", max_depth=1)
    content_items_limited = []
    extractor_limited._process_elements_in_order(container, content_items_limited, depth=2)
    assert len(content_items_limited) == 0  # Should not process anything at depth 2

def test_process_content_elements_mixed_content_SCP_BHTML175():
    # Create a concrete implementation of BaseHTMLExtractor for testing
    class TestExtractor(BaseHTMLExtractor):
        def extract_content(self):
            pass
        def find_main_content_container(self):
            pass

    # Test HTML with mixed content types
    test_html = """
        <div>
            <h1>Test Title</h1>
            <p>First paragraph</p>
            <img src="test.jpg" alt="Test Image">
            <pre class="language-python">def test(): pass</pre>
            <div class="card">Alert message</div>
            <ul>
                <li>List item 1</li>
                <li>List item 2</li>
            </ul>
        </div>
    """

    # Setup
    extractor = TestExtractor("<html></html>")  # Dummy HTML content
    container = BeautifulSoup(test_html, 'html.parser').find('div')

    # Execute
    result = extractor.process_content_elements(container)


    # Assert
    # Expected number of items (1 heading + 1 paragraph + 1 image + 1 code + 1 alert + 1 list + 2 list items)
    assert len(result) == 8

    # Verify each item type and content
    # Item 0: Heading
    assert result[0]["type"] == "heading"
    assert result[0]["level"] == 1
    assert result[0]["text"] == "Test Title"

    # Item 1: Paragraph
    assert result[1]["type"] == "paragraph"
    assert result[1]["text"] == "First paragraph"

    # Item 2: Image
    assert result[2]["type"] == "image"
    assert result[2]["src"] == "test.jpg"
    assert result[2]["alt"] == "Test Image"

    # Item 3: Code
    assert result[3]["type"] == "code"
    assert result[3]["language"] == "python"
    assert result[3]["text"] == "def test(): pass"

    # Item 4: Alert
    assert result[4]["type"] == "alert"
    assert result[4]["text"] == "Alert message"

    # Item 5: List
    assert result[5]["type"] == "list"
    assert result[5]["list_type"] == "unordered"
    assert result[5]["items"] == ["List item 1", "List item 2"]

    # Item 6: List item 1
    assert result[6]["type"] == "paragraph"
    assert result[6]["text"] == "List item 1"

    # Item 7: List item 2
    assert result[7]["type"] == "paragraph"
    assert result[7]["text"] == "List item 2"

