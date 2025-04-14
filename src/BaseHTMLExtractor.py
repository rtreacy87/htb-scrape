from bs4 import BeautifulSoup
import re
import os
from abc import ABC, abstractmethod
from src.image_handler import process_image_element

class BaseHTMLExtractor(ABC):

    def __init__(self, html_content, base_url=None, download_images=True, image_output_dir='images', max_depth=5):
        """Initialize with HTML content to parse.
        Args:
            html_content (str): HTML content as string
            base_url (str, optional): Base URL for resolving relative image URLs
            download_images (bool): Whether to download images
            image_output_dir (str): Directory to save downloaded images
            max_depth (int): Maximum recursion depth for processing nested elements
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.base_url = base_url
        self.download_images = download_images
        self.image_output_dir = image_output_dir
        self.max_depth = max_depth
        self.element_processors = self.get_element_processor_map()

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
        Iterates through elements in the container and processes them in order.
        Args:
            container: BeautifulSoup element containing the content to process
        Returns:
            list: List of processed content items, where each item is a dictionary
                 containing the structured data for that element. Invalid or
                 unprocessable elements are filtered out.
        """
        content_items = []
        # Process all elements in order by traversing the DOM tree
        self._process_elements_in_order(container, content_items)
        return content_items

    def _process_elements_in_order(self, container, content_items, depth=0):
        """Recursively process elements in order.
        Args:
            container: BeautifulSoup element to process
            content_items: List to append processed items to
            depth: Current recursion depth
        """
        if self._should_stop_recursion(depth):
            return
        # Process direct children in order
        for element in container.children:
            if not hasattr(element, 'name') or not element.name:
                continue
            # Process this element based on its type
            if element.name == 'img':
                self._process_image_element(element, content_items)
            elif element.name == 'li':
                self._process_list_item(element, content_items)
            elif element.name == 'td' or element.name == 'th':
                self._process_table_cell(element, content_items)
            else:
                self._process_standard_element(element, content_items)
            self._process_container_children(element, content_items, depth)

    def _should_stop_recursion(self, depth):
        """Check if recursion should stop based on depth.
        Args:
            depth: Current recursion depth
        Returns:
            bool: True if recursion should stop, False otherwise
        """
        return depth > self.max_depth

    def _process_image_element(self, element, content_items):
        """Process an image element and add it to content items.
        Args:
            element: BeautifulSoup image element
            content_items: List to append processed item to
        """
        processed_item = self.process_image(element)
        if processed_item:
            content_items.append(processed_item)
            print(f"Processed image: {processed_item.get('src', 'unknown')}")

    def _process_list_item(self, element, content_items):
        """Process a list item element and its contained images.
        Args:
            element: BeautifulSoup list item element
            content_items: List to append processed items to
        """
        # First process the list item itself
        processed_item = self.process_single_element(element, self.element_processors)
        if processed_item:
            content_items.append(processed_item)
        # Then look for images inside the list item
        for img in element.find_all('img', recursive=True):
            processed_img = self.process_image(img)
            if processed_img:
                content_items.append(processed_img)
                print(f"Processed image in list item: {processed_img.get('src', 'unknown')}")

    def _process_table_cell(self, element, content_items):
        """Process a table cell element and its contained images.
        Args:
            element: BeautifulSoup table cell element (td or th)
            content_items: List to append processed items to
        """
        # Process text content
        text = element.get_text().strip()
        if text:
            content_items.append({
                "type": "paragraph",
                "text": text
            })

        # Process images in the cell
        for img in element.find_all('img', recursive=True):
            processed_img = self.process_image(img)
            if processed_img:
                content_items.append(processed_img)
                print(f"Processed image in table cell: {processed_img.get('src', 'unknown')}")

    def _process_standard_element(self, element, content_items):
        """Process a standard element using the appropriate processor.
        Args:
            element: BeautifulSoup element
            content_items: List to append processed item to
        """
        processed_item = self.process_single_element(element, self.element_processors)
        if processed_item:
            content_items.append(processed_item)

    def _process_container_children(self, element, content_items, depth):
        """Process children of container elements recursively.
        Args:
            element: BeautifulSoup element to check if it's a container
            content_items: List to append processed items to
            depth: Current recursion depth
        """
        # If this is a container element that might contain images, process its children
        # Expanded list of container elements
        if element.name in ['div', 'article', 'section', 'figure', 'p', 'table', 'tr', 'ul', 'ol']:
            self._process_elements_in_order(element, content_items, depth + 1)

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

    def process_image(self, element):
        """Process an image element.
        Uses the image_handler module to process and optionally download the image.
        """
        return process_image_element(
            element,
            base_url=self.base_url,
            download=self.download_images,
            output_dir=self.image_output_dir
        )

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
