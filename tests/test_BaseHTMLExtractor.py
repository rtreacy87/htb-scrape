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

def test_process_code_block_with_language_SCP_HTB005():
    # Test code block with language specified
    test_html = '<pre class="language-python">def test(): pass</pre>'
    element = BeautifulSoup(test_html, 'html.parser').find('pre')
    
    result = TestHTMLExtractor.process_code_block(element)
    
    assert result["type"] == "code"
    assert result["language"] == "python"
    assert result["text"] == "def test(): pass"

def test_process_code_block_without_language_SCP_HTB010():
    # Test code block without language
    test_html = '<pre>print("hello")</pre>'
    element = BeautifulSoup(test_html, 'html.parser').find('pre')
    
    result = TestHTMLExtractor.process_code_block(element)
    
    assert result["type"] == "code"
    assert result["language"] == ""
    assert result["text"] == 'print("hello")'

def test_process_code_block_multiple_classes_SCP_HTB015():
    # Test code block with multiple classes
    test_html = '<pre class="highlight language-javascript code-block">const x = 1;</pre>'
    element = BeautifulSoup(test_html, 'html.parser').find('pre')
   
    result = TestHTMLExtractor.process_code_block(element)
    
    assert result["type"] == "code"
    assert result["language"] == "javascript"
    assert result["text"] == "const x = 1;"

def test_process_code_block_empty_SCP_HTB020():
    # Test empty code block
    test_html = '<pre class="language-ruby">    </pre>'
    element = BeautifulSoup(test_html, 'html.parser').find('pre')
    
    result = TestHTMLExtractor.process_code_block(element)
    
    assert result["type"] == "code"
    assert result["language"] == "ruby"
    assert result["text"] == ""

def test_process_paragraph_with_text_SCP_HTB025():
    # Test paragraph with regular text
    test_html = '<p>This is a test paragraph.</p>'
    element = BeautifulSoup(test_html, 'html.parser').find('p')
    
    result = BaseHTMLExtractor.process_paragraph(element)
    
    assert result["type"] == "paragraph"
    assert result["text"] == "This is a test paragraph."

def test_process_paragraph_empty_SCP_HTB030():
    # Test empty paragraph
    test_html = '<p>    </p>'
    element = BeautifulSoup(test_html, 'html.parser').find('p')
    
    result = BaseHTMLExtractor.process_paragraph(element)
    
    assert result is None

def test_process_paragraph_with_nested_elements_SCP_HTB035():
    # Test paragraph with nested elements
    test_html = '<p>Text with <strong>bold</strong> and <em>italic</em> content.</p>'
    element = BeautifulSoup(test_html, 'html.parser').find('p')
    
    result = BaseHTMLExtractor.process_paragraph(element)
    
    assert result["type"] == "paragraph"
    assert result["text"] == "Text with bold and italic content."

def test_process_paragraph_with_newlines_SCP_HTB040():
    # Test paragraph with newlines and extra spaces
    test_html = '<p>\n    Multiple\n    lines with    spaces\n</p>'
    element = BeautifulSoup(test_html, 'html.parser').find('p')
    
    result = BaseHTMLExtractor.process_paragraph(element)
    
    assert result["type"] == "paragraph"
    assert result["text"] == "Multiple lines with spaces"

def test_process_image_with_src_and_alt_SCP_HTB045():
    # Test image with both src and alt attributes
    test_html = '<img src="test.jpg" alt="Test Image">'
    element = BeautifulSoup(test_html, 'html.parser').find('img')
    
    result = BaseHTMLExtractor.process_image(element)
    
    assert result["type"] == "image"
    assert result["src"] == "test.jpg"
    assert result["alt"] == "Test Image"

def test_process_image_without_alt_SCP_HTB050():
    # Test image without alt attribute
    test_html = '<img src="test.jpg">'
    element = BeautifulSoup(test_html, 'html.parser').find('img')
    
    result = BaseHTMLExtractor.process_image(element)
    
    assert result["type"] == "image"
    assert result["src"] == "test.jpg"
    assert result["alt"] == "Image"  # Should default to "Image"

def test_process_image_empty_attributes_SCP_HTB055():
    # Test image with empty attributes
    test_html = '<img src="" alt="">'
    element = BeautifulSoup(test_html, 'html.parser').find('img')
    
    result = BaseHTMLExtractor.process_image(element)
    
    assert result["type"] == "image"
    assert result["src"] == ""
    assert result["alt"] == "Image"  # Should default to "Image" when alt is empty

def test_process_alert_with_text_SCP_HTB060():
    # Test alert with regular text
    test_html = '<div class="card">This is an alert message</div>'
    element = BeautifulSoup(test_html, 'html.parser').find('div')
    
    result = BaseHTMLExtractor.process_alert(element)
    
    assert result["type"] == "alert"
    assert result["text"] == "This is an alert message"

def test_process_alert_with_nested_elements_SCP_HTB065():
    # Test alert with nested elements
    test_html = '<div class="card"><strong>Warning:</strong> Important alert <em>message</em></div>'
    element = BeautifulSoup(test_html, 'html.parser').find('div')
    
    result = BaseHTMLExtractor.process_alert(element)
    
    assert result["type"] == "alert"
    assert result["text"] == "Warning: Important alert message"

def test_process_alert_empty_SCP_HTB070():
    # Test empty alert
    test_html = '<div class="card">    </div>'
    element = BeautifulSoup(test_html, 'html.parser').find('div')
    
    result = BaseHTMLExtractor.process_alert(element)

    assert result is None
    

def test_process_alert_with_newlines_SCP_HTB075():
    # Test alert with newlines and extra spaces
    test_html = '<div class="card">\n    Multiple\n    lines with    spaces\n</div>'
    element = BeautifulSoup(test_html, 'html.parser').find('div')
    
    result = BaseHTMLExtractor.process_alert(element)
    
    assert result["type"] == "alert"
    assert result["text"] == "Multiple lines with spaces"

def test_process_table_basic_SCP_HTB080():
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

def test_process_list_ordered_SCP_HTB085():
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

def test_process_list_unordered_SCP_HTB090():
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

def test_process_list_with_nested_elements_SCP_HTB095():
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

def test_process_list_empty_SCP_HTB100():
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

def test_process_heading_basic_SCP_HTB105():
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

def test_process_heading_with_nested_elements_SCP_HTB110():
    # Test heading with nested HTML elements
    test_html = '<h2>Title with <strong>bold</strong> and <em>italic</em> text</h2>'
    element = BeautifulSoup(test_html, 'html.parser').find('h2')
    
    result = BaseHTMLExtractor.process_heading(element)
    
    assert result["type"] == "heading"
    assert result["level"] == 2
    assert result["text"] == "Title with bold and italic text"

def test_process_heading_with_whitespace_SCP_HTB115():
    # Test heading with extra whitespace
    test_html = '<h1>\n    Heading with    extra\n    spaces    \n</h1>'
    element = BeautifulSoup(test_html, 'html.parser').find('h1')
    
    result = BaseHTMLExtractor.process_heading(element)
    
    assert result["type"] == "heading"
    assert result["level"] == 1
    assert result["text"] == "Heading with extra spaces"

def test_process_content_elements_mixed_content_SCP_HTB120():
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
    assert len(result) == 5
    
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

def test_process_single_element_SCP_HTB125():
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

def test_is_valid_element_SCP_HTB130():
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

def test_get_element_processor_map_SCP_HTB135():
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

def test_extract_title_SCP_HTB140():
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

