import pytest
from bs4 import BeautifulSoup
from src.HTBHTMLExtractor import HTBHTMLExtractor

def test_extract_questions_SCP_HTB005():
    # Test HTML with various question formats
    test_html = """
    <div id="questionsDiv">
        <label class="module-question">+ 2 🟦 What is the first question?</label>
        <label class="module-question">+ 1 🟦  Second question here</label>
        <label class="module-question">+3🟦Third question without spaces</label>
        <label class="module-question">Regular question without cube indicator</label>
    </div>
    """
    
    extractor = HTBHTMLExtractor(test_html)
    questions = extractor.extract_questions()
    
    assert len(questions) == 4
    assert questions[0] == "What is the first question?"
    assert questions[1] == "Second question here"
    assert questions[2] == "Third question without spaces"
    assert questions[3] == "Regular question without cube indicator"

def test_extract_questions_empty_SCP_HTB010():
    # Test HTML without questions div
    test_html = "<div>Some other content</div>"
    extractor = HTBHTMLExtractor(test_html)
    questions = extractor.extract_questions()
    
    assert len(questions) == 0
    assert questions == []

def test_extract_questions_empty_div_SCP_HTB015():
    # Test HTML with empty questions div
    test_html = '<div id="questionsDiv"></div>'
    extractor = HTBHTMLExtractor(test_html)
    questions = extractor.extract_questions()
    
    assert len(questions) == 0
    assert questions == []

def test_extract_questions_malformed_SCP_HTB020():
    # Test HTML with malformed question labels
    test_html = """
    <div id="questionsDiv">
        <label class="module-question">+ ⬛ Malformed cube</label>
        <label class="module-question">+</label>
        <label class="module-question">    </label>
    </div>
    """
    extractor = HTBHTMLExtractor(test_html)
    questions = extractor.extract_questions()
    
    assert len(questions) == 3
    assert questions[0] == "Malformed cube"
    assert questions[1] == ""
    assert questions[2] == ""

def test_find_main_content_container_training_module_SCP_HTB025():
    # Test HTML with training-module div
    test_html = """
    <html>
        <body>
            <div class="training-module">
                <p>Main content here</p>
            </div>
        </body>
    </html>
    """
    extractor = HTBHTMLExtractor(test_html)
    container = extractor.find_main_content_container()
    
    assert container is not None
    assert container.name == 'div'
    assert 'training-module' in container['class']

def test_find_main_content_container_fallbacks_SCP_HTB030():
    # Test HTML with fallback containers
    test_html = """
    <html>
        <body>
            <div class="page-content">
                <p>Alternative content here</p>
            </div>
        </body>
    </html>
    """
    extractor = HTBHTMLExtractor(test_html)
    container = extractor.find_main_content_container()
    
    assert container is not None
    assert container.name == 'div'
    assert 'page-content' in container['class']

def test_find_main_content_container_no_containers_SCP_HTB035():
    # Test HTML without any valid containers except body
    test_html = """
    <html>
        <body>
            <div class="other-content">
                <p>Some content</p>
            </div>
        </body>
    </html>
    """
    extractor = HTBHTMLExtractor(test_html)
    container = extractor.find_main_content_container()
    
    assert container is not None
    assert container.name == 'body'  

def test_find_main_content_container_completely_empty_SCP_HTB040():
    # Test HTML without any containers at all
    test_html = "<html></html>"
    extractor = HTBHTMLExtractor(test_html)
    container = extractor.find_main_content_container()
    
    assert container is None  

def test_extract_content_SCP_HTB045():
    # Test HTML with various content types
    test_html = """
    <html>
        <body>
            <div class="training-module">
                <h1>Test Module</h1>
                <p>Main paragraph content</p>
                <pre class="language-python">def test(): pass</pre>
                <div id="questionsDiv">
                    <label class="module-question">+ 1 🟦 Test question?</label>
                </div>
            </div>
        </body>
    </html>
    """
    
    extractor = HTBHTMLExtractor(test_html)
    content = extractor.extract_content()
    
    assert content["title"] == "Test Module"
    assert len(content["content"]) == 3  # h1, p, and pre elements
    assert content["questions"] == ["Test question?"]
    
    # Verify content structure
    assert content["content"][0] == {"type": "heading", "level": 1, "text": "Test Module"}
    assert content["content"][1] == {"type": "paragraph", "text": "Main paragraph content"}
    assert content["content"][2] == {"type": "code", "language": "python", "text": "def test(): pass"}

def test_extract_content_empty_SCP_HTB050():
    # Test HTML without main container
    test_html = "<html><body></body></html>"
    
    extractor = HTBHTMLExtractor(test_html)
    content = extractor.extract_content()
    
    assert content["title"] == "Unknown Title"
    assert len(content["content"]) == 0  # Content list is empty when no content is found
    assert "content" in content  # Verify the content key exists

def test_extract_content_fallback_container_SCP_HTB055():
    # Test HTML with fallback container
    test_html = """
    <html>
        <body>
            <div class="page-content">
                <h1>Fallback Title</h1>
                <p>Content in fallback container</p>
            </div>
        </body>
    </html>
    """
    
    extractor = HTBHTMLExtractor(test_html)
    content = extractor.extract_content()
    
    assert content["title"] == "Fallback Title"
    assert len(content["content"]) == 2
    assert content["content"][0] == {"type": "heading", "level": 1, "text": "Fallback Title"}
    assert content["content"][1] == {"type": "paragraph", "text": "Content in fallback container"}