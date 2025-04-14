from bs4 import BeautifulSoup
import re
import os
from src.BaseHTMLExtractor import BaseHTMLExtractor
from src.image_handler import process_image_element

class LLMStructuredExtractor(BaseHTMLExtractor):
    """HTML extractor that creates a more structured output for LLM consumption."""

    def extract_content(self):
        """Extract content from HTML and return structured data.
        Returns:
            dict: A dictionary containing:
                - title (str): The page title
                - content (list): List of processed content items with a hierarchical structure
                - questions (list, optional): List of questions if any are found
        """
        content_container = self.find_main_content_container()
        if not content_container:
            return {"title": "Error", "content": [{"type": "paragraph", "text": "Could not extract content"}]}
        title = self.extract_title()
        content_items = self.process_content_elements(content_container)
        questions = self.extract_questions()
        result = {"title": title, "content": content_items}
        if questions:
            result["questions"] = questions
        return result

    def find_main_content_container(self):
        """Find the main content container in HTML.
        Returns:
            BeautifulSoup element or None: The main content container element if found, None otherwise.
        """
        # Try to find common content containers
        for selector in [
            ('div', 'training-module'),
            ('div', 'page-content'),
            ('div', 'content'),
            ('article', None),
            ('main', None),
            ('body', None)
        ]:
            element_type, class_name = selector
            if class_name:
                container = self.soup.find(element_type, class_=class_name)
            else:
                container = self.soup.find(element_type)
            if container:
                return container
        return None

    def extract_questions(self):
        """Extract questions from the page.
        Returns:
            list: A list of question strings extracted from the page. Returns empty list if no questions found.
        """
        questions_div = self.soup.find('div', id='questionsDiv')
        if not questions_div:
            return []
        questions = []
        for question_label in questions_div.find_all('label', class_='module-question'):
            question_text = question_label.text.strip()
            # Extract just the question part, removing cube indicators
            question_text = re.sub(r'^\s*\+\s*\d*\s*[^\w\s]*\s*', '', question_text).strip()
            questions.append(question_text)
        return questions

    def process_content_elements(self, container):
        """Process all content elements in the container with a more structured approach.

        This method creates a hierarchical structure where images are embedded within
        their parent elements (lists, table cells, etc.) rather than as separate items.

        Args:
            container: BeautifulSoup element containing the content to process

        Returns:
            list: List of processed content items with a hierarchical structure
        """
        content_items = []

        # Process all elements in order by traversing the DOM tree
        self._process_elements_in_order(container, content_items)

        return content_items

    def _process_elements_in_order(self, container, content_items, depth=0):
        """Recursively process elements in order with a more structured approach.

        Args:
            container: BeautifulSoup element to process
            content_items: List to append processed items to
            depth: Current recursion depth
        """
        if depth > self.max_depth:
            return

        # Special handling for lists (ul/ol)
        if container.name in ['ul', 'ol']:
            list_type = "ordered" if container.name == "ol" else "unordered"
            list_items = []

            # Process each list item with its embedded images
            for li in container.find_all('li', recursive=False):
                item_content = []

                # Get the text content
                text = li.get_text().strip()
                if text:
                    item_content.append({
                        "type": "text",
                        "content": text
                    })

                # Get any images in the list item
                for img in li.find_all('img', recursive=True):
                    processed_img = self.process_image(img)
                    if processed_img:
                        item_content.append(processed_img)

                # Add the item with its content
                if item_content:
                    list_items.append(item_content)

            # Add the list to content items
            if list_items:
                content_items.append({
                    "type": "list",
                    "list_type": list_type,
                    "items": list_items
                })

            return

        # Special handling for tables
        if container.name == 'table':
            rows = []

            # Process each row
            for tr in container.find_all('tr', recursive=False):
                cells = []

                # Process each cell
                for td in tr.find_all(['td', 'th'], recursive=False):
                    cell_content = []

                    # Get the text content
                    text = td.get_text().strip()
                    if text:
                        cell_content.append({
                            "type": "text",
                            "content": text
                        })

                    # Get any images in the cell
                    for img in td.find_all('img', recursive=True):
                        processed_img = self.process_image(img)
                        if processed_img:
                            cell_content.append(processed_img)

                    # Add the cell with its content
                    cells.append(cell_content)

                # Add the row with its cells
                if cells:
                    rows.append(cells)

            # Add the table to content items
            if rows:
                content_items.append({
                    "type": "table",
                    "rows": rows
                })

            return

        # Process direct children in order
        for element in container.children:
            if not hasattr(element, 'name') or not element.name:
                continue

            # Skip elements that are handled specially
            if element.name in ['ul', 'ol', 'table']:
                self._process_elements_in_order(element, content_items, depth + 1)
                continue

            # Process this element
            if element.name == 'img':
                processed_item = self.process_image(element)
                if processed_item:
                    content_items.append(processed_item)
            else:
                processed_item = self.process_single_element(element, self.element_processors)
                if processed_item:
                    content_items.append(processed_item)

                # If this is a container element that might contain nested elements, process its children
                if element.name in ['div', 'article', 'section', 'figure', 'p']:
                    self._process_elements_in_order(element, content_items, depth + 1)


def extract_structured_content_from_html(html_content, base_url=None, download_images=True, image_output_dir='images'):
    """Helper function to extract structured content from HTML for LLM consumption.

    Args:
        html_content (str): HTML content to parse
        base_url (str, optional): Base URL for resolving relative image URLs
        download_images (bool): Whether to download images
        image_output_dir (str): Directory to save downloaded images

    Returns:
        dict: Extracted content with a hierarchical structure
    """
    extractor = LLMStructuredExtractor(html_content, base_url, download_images, image_output_dir)
    return extractor.extract_content()
