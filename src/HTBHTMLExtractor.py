from src.BaseHTMLExtractor import BaseHTMLExtractor
import re

class HTBHTMLExtractor(BaseHTMLExtractor):
    """Specific HTML extractor for HackTheBox Academy content."""

    def extract_content(self):
        """Extract content from HTML and return structured data.
        Returns:
            dict: A dictionary containing:
                - title (str): The page title
                - content (list): List of processed content items
                - questions (list, optional): List of questions if any are found
        If content extraction fails, returns an error dictionary with:
            - title: "Error"
            - content: Single paragraph item with error message
        The method:
        1. Finds the main content container
        2. Extracts the page title
        3. Processes all content elements
        4. Extracts any questions
        5. Combines everything into a structured result
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
        """Find the main content container in HackTheBox Academy HTML.
        Returns:
            BeautifulSoup element or None: The main content container element if found, None otherwise.
        The method searches for content containers in the following order:
        1. <div> with class 'training-module'
        2. <div> with class 'page-content'
        3. <article> tag
        4. <body> tag
        If the primary container ('training-module') is not found, a warning is printed
        before attempting to find alternative containers.
        """
        training_module = self.soup.find('div', class_='training-module')
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
                container = self.soup.find(element_type, class_=class_name)
            else:
                container = self.soup.find(element_type)
            if container:
                return container
        return None

    def extract_questions(self):
        """Extract questions from HackTheBox Academy pages.
        Returns:
            list: A list of question strings extracted from the page. Returns empty list if no questions found.
        Details:
            - Looks for questions inside a div with id='questionsDiv'
            - Extracts text from labels with class='module-question'
            - Removes cube indicators (e.g. "+ 2 🟦") from question text using regex
            - Strips whitespace from questions
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


def extract_content_from_html(html_content, base_url=None, download_images=True, image_output_dir='images'):
    """Helper function to extract content from HTML.

    Args:
        html_content (str): HTML content to parse
        base_url (str, optional): Base URL for resolving relative image URLs
        download_images (bool): Whether to download images
        image_output_dir (str): Directory to save downloaded images

    Returns:
        dict: Extracted content
    """
    extractor = HTBHTMLExtractor(html_content, base_url, download_images, image_output_dir)
    return extractor.extract_content()