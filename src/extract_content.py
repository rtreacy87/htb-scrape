from bs4 import BeautifulSoup
import re

def extract_content(html_content):
    """Extract content from HTML and return structured data"""
    soup = BeautifulSoup(html_content, 'html.parser')
    content_container = find_main_content_container(soup)
    if not content_container:
        return {"title": "Error", "content": [{"type": "paragraph", "text": "Could not extract content"}]}
    title = extract_title(soup)
    content_items = process_content_elements(content_container)
    questions = extract_questions(soup)
    result = {"title": title, "content": content_items}
    if questions:
        result["questions"] = questions
    return result

def find_main_content_container(soup):
    """Find the main content container in the HTML"""
    training_module = soup.find('div', class_='training-module')
    if training_module:
        return training_module
    print("Warning: Could not find main 'training-module' div. Looking for alternative content...")
    for selector in [
        ('div', 'page-content'),
        ('article', None),
        ('body', None)
    ]:
        element_type, class_name = selector
        if class_name:
            container = soup.find(element_type, class_=class_name)
        else:
            container = soup.find(element_type)
            
        if container:
            return container
    return None

def extract_title(soup):
    """Extract the page title from various possible elements"""
    title_elements = [
        soup.find('h4', class_='page-title'),
        soup.find('h1', class_='page-title'),
        soup.find('h1'),
        soup.find('title')
    ]
    for element in title_elements:
        if element and element.text.strip():
            return element.text.strip()
    return "Unknown Title"

def process_content_elements(container):
    """Process all content elements in the container"""
    element_processors = {
        'h1': process_heading,
        'h2': process_heading,
        'h3': process_heading,
        'h4': process_heading,
        'h5': process_heading,
        'h6': process_heading,
        'p': process_paragraph,
        'pre': process_code_block,
        'ol': process_list,
        'ul': process_list,
        'img': process_image,
        'table': process_table
    }
    content_items = []
    for element in container.children:
        if not hasattr(element, 'name') or not element.name:
            continue
        processor = element_processors.get(element.name)
        if element.name == 'div' and 'card' in element.get('class', []):
            item = process_alert(element)
            item = processor(element)
        else:
            continue
        if item:
            content_items.append(item)
    return content_items

def process_heading(element):
    """Process a heading element"""
    return {
        "type": "heading",
        "level": int(element.name[1]),
        "text": element.text.strip()
    }
    
def process_list(element):
    """Process a list element"""
    list_items = []
    for li in element.find_all('li', recursive=False):
        list_items.append(li.text.strip())
        
    return {
        "type": "list",
        "list_type": "ordered" if element.name == "ol" else "unordered",
        "items": list_items
    }

def process_table(element):
    """Process a table element"""
    return {
        "type": "table",
        "text": "Table content (summarized for brevity)"
    }

def process_alert(element):
    """Process an alert element"""
    card_text = element.text.strip()
    return {
        "type": "alert",
        "text": card_text
    }

def process_image(element):
    """Process an image element"""
    src = element.get('src', '')
    alt = element.get('alt', '')
    return {
        "type": "image",
        "src": src,
        "alt": alt if alt else "Image"
    }

def process_paragraph(element):
    """Process a paragraph element"""
    text = element.text.strip()
    if not text:  # Skip empty paragraphs
        return None
    return {
        "type": "paragraph",
        "text": text
    }

def process_code_block(element):
    """Process a code block element"""
    code = element.text.strip()
    language = ""
    class_attr = element.get('class', [])
    
    if class_attr:
        language_match = re.search(r'language-(\w+)', ' '.join(class_attr))
        if language_match:
            language = language_match.group(1)
    
    return {
        "type": "code",
        "language": language,
        "text": code
    }

def extract_questions(soup):
    """Extract questions from the page
    
    Args:
        soup (BeautifulSoup): BeautifulSoup object containing the parsed HTML
        
    Returns:
        list: A list of question strings extracted from the page. Returns empty list if no questions found.
        
    Details:
        - Looks for questions inside a div with id='questionsDiv'
        - Extracts text from labels with class='module-question'
        - Removes cube indicators (e.g. "+ 2 🟦") from question text using regex
        - Strips whitespace from questions
    """
    questions_div = soup.find('div', id='questionsDiv')
    if not questions_div:
        return []
    questions = []
    for question_label in questions_div.find_all('label', class_='module-question'):
        question_text = question_label.text.strip()
        # Extract just the question part, removing cube indicators
        question_text = re.sub(r'^\s*\+\s*\d+\s*[^\w]*\s*', '', question_text).strip()
        questions.append(question_text)
    
    return questions
