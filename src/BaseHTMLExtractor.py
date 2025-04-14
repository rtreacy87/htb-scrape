from bs4 import BeautifulSoup
import re
from abc import ABC, abstractmethod

class BaseHTMLExtractor(ABC):
    
    def __init__(self, html_content):
        """Initialize with HTML content to parse.
        Args:
            html_content (str): HTML content as string
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        
    @abstractmethod
    def extract_content(self):
        """Extract content from HTML and return structured data."""
        pass
    
    @abstractmethod
    def find_main_content_container(self):
        """Find the main content container in the HTML."""
        pass
    
    def extract_title(self):
        """Extract the page title from various possible elements.
        Searches for the title in the following order of precedence:
        1. <h4> tag with class 'page-title'
        2. <h1> tag with class 'page-title'
        3. First <h1> tag
        4. <title> tag
        Returns:
            str: The extracted title text, stripped of whitespace.
                Returns "Unknown Title" if no title element is found.
        """
        title_elements = [
            self.soup.find('h4', class_='page-title'),
            self.soup.find('h1', class_='page-title'),
            self.soup.find('h1'),
            self.soup.find('title')
        ]
        for element in title_elements:
            if element and element.text.strip():
                return element.text.strip()
        return "Unknown Title"
    
    def get_element_processor_map(self):
        """Return a mapping of HTML elements to their processor methods."""
        return {
            'h1': self.process_heading,
            'h2': self.process_heading,
            'h3': self.process_heading,
            'h4': self.process_heading,
            'h5': self.process_heading,
            'h6': self.process_heading,
            'p': self.process_paragraph,
            'pre': self.process_code_block,
            'ol': self.process_list,
            'ul': self.process_list,
            'img': self.process_image,
            'table': self.process_table
        }
        
    def is_valid_element(self, element):
        """Check if element is valid for processing.
        
        Args:
            element: BeautifulSoup element to validate
        
        Returns:
            bool: True if element is a valid HTML element, False otherwise
        """
        return hasattr(element, 'name') and element.name is not None
    
    def process_single_element(self, element, element_processors):
        """Process a single HTML element and return the processed item if successful.
        Args:
            element: BeautifulSoup element to process
            element_processors (dict): Mapping of HTML tag names to their processor methods
        Returns:
            dict: Processed element data if processing succeeds
            None: If element is invalid or no suitable processor is found
        Processing steps:
        1. Validates the element using is_valid_element()
        2. Looks up and applies standard processor based on element tag name
        3. Special handling for div elements with 'card' class as alerts
        """
        if not self.is_valid_element(element):
            return None
        processor = element_processors.get(element.name)
        if processor:
            return processor(element)
        if element.name == 'div' and 'card' in element.get('class', []):
            return self.process_alert(element)    
        return None
    
    def process_content_elements(self, container):
        """Process all content elements in the container.
        Iterates through all direct children of the container and processes each element
        using the appropriate processor from the element_processors map.
        Args:
            container: BeautifulSoup element containing the content to process
        Returns:
            list: List of processed content items, where each item is a dictionary 
                 containing the structured data for that element. Invalid or 
                 unprocessable elements are filtered out.
        """
        element_processors = self.get_element_processor_map()
        content_items = [] 
        for element in container.children:
            processed_item = self.process_single_element(element, element_processors)
            if processed_item:
                content_items.append(processed_item)       
        return content_items

    @staticmethod
    def process_heading(element):
        """Process a heading element."""
        # Normalize whitespace: replace newlines and multiple spaces with single spaces
        text = re.sub(r'\s+', ' ', element.text.strip())
        return {
            "type": "heading",
            "level": int(element.name[1]),
            "text": text
        }

    @staticmethod
    def process_list(element):
        """Process a list element."""
        list_items = []
        for li in element.find_all('li', recursive=False):
            list_items.append(li.text.strip())
        return {
            "type": "list",
            "list_type": "ordered" if element.name == "ol" else "unordered",
            "items": list_items
        }

    @staticmethod
    def process_table(element):
        """Process a table element."""
        return {
            "type": "table",
            "text": "Table content (summarized for brevity)"
        }

    @staticmethod
    def process_alert(element):
        """Process an alert element."""
        card_text = element.text.strip()
        if not card_text:  
            return None
        # Normalize whitespace: replace newlines and multiple spaces with single spaces
        normalized_text = re.sub(r'\s+', ' ', card_text)
        return {
            "type": "alert",
            "text": normalized_text
        }

    @staticmethod
    def process_image(element):
        """Process an image element."""
        src = element.get('src', '')
        alt = element.get('alt', '')
        return {
            "type": "image",
            "src": src,
            "alt": alt if alt else "Image"
        }

    @staticmethod
    def process_paragraph(element):
        """Process a paragraph element.
        Args:
            element: BeautifulSoup element representing a paragraph tag (<p>)
        Returns:
            dict: A dictionary containing the paragraph type and text content
                Format: {"type": "paragraph", "text": "paragraph content"}
            None: If the paragraph contains no text after stripping whitespace
        """
        text = element.text.strip()
        if not text:  
            return None
        # Normalize whitespace: replace newlines and multiple spaces with single spaces
        normalized_text = re.sub(r'\s+', ' ', text)
        return {
            "type": "paragraph",
            "text": normalized_text
        }

    @staticmethod
    def process_code_block(element):
        """Process a code block element."""
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
