def extract_content(html_content):
    """
    Extract the main content from HTB Academy HTML and format it in a clean way
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main content div which contains the actual training material
    training_module = soup.find('div', class_='training-module')
    
    if not training_module:
        print("Warning: Could not find main 'training-module' div. Looking for alternative content...")
        # Try to find any substantial content div as a fallback
        main_content = soup.find('div', class_='page-content')
        if main_content:
            training_module = main_content
        else:
            # Try to find an article tag
            article = soup.find('article')
            if article:
                training_module = article
            else:
                # Last resort - just take the body
                training_module = soup.find('body')
                if not training_module:
                    return {"title": "Error", "content": [{"type": "paragraph", "text": "Could not extract content from the HTML"}]}
    
    # Extract the title (try multiple common title locations)
    title = "Unknown Title"
    title_elements = [
        soup.find('h4', class_='page-title'),
        soup.find('h1', class_='page-title'),
        soup.find('h1'),
        soup.find('title')
    ]
    
    for element in title_elements:
        if element and element.text.strip():
            title = element.text.strip()
            break
    
    # Process the content
    result = {
        "title": title,
        "content": []
    }
    
    # Process all elements in the training module
    for element in training_module.children:
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            # Format headings
            result["content"].append({
                "type": "heading",
                "level": int(element.name[1]),
                "text": element.text.strip()
            })
        
        elif element.name == 'p':
            # Process paragraphs
            text = element.text.strip()
            if text:  # Skip empty paragraphs
                result["content"].append({
                    "type": "paragraph",
                    "text": text
                })
        
        elif element.name == 'pre':
            # Process code blocks
            code = element.text.strip()
            language = ""
            class_attr = element.get('class', [])
            if class_attr:
                language_match = re.search(r'language-(\w+)', ' '.join(class_attr))
                if language_match:
                    language = language_match.group(1)
            
            result["content"].append({
                "type": "code",
                "language": language,
                "text": code
            })
        
        elif element.name == 'ol' or element.name == 'ul':
            # Process lists
            list_items = []
            for li in element.find_all('li', recursive=False):
                list_items.append(li.text.strip())
            
            result["content"].append({
                "type": "list",
                "list_type": "ordered" if element.name == "ol" else "unordered",
                "items": list_items
            })
        
        elif element.name == 'img':
            # Process images
            src = element.get('src', '')
            alt = element.get('alt', '')
            
            result["content"].append({
                "type": "image",
                "src": src,
                "alt": alt if alt else "Image"
            })
        
        elif element.name == 'table':
            # Process tables (simplified)
            result["content"].append({
                "type": "table",
                "text": "Table content (summarized for brevity)"
            })
        
        elif element.name == 'div' and 'card' in element.get('class', []):
            # Process card/alert boxes
            card_text = element.text.strip()
            result["content"].append({
                "type": "alert",
                "text": card_text
            })
    
    # Add questions section if present
    questions_div = soup.find('div', id='questionsDiv')
    if questions_div:
        questions = []
        for question_label in questions_div.find_all('label', class_='module-question'):
            question_text = question_label.text.strip()
            # Extract just the question part, removing cube indicators
            question_text = re.sub(r'\+\s*\d+\s*\S.*?\s', '', question_text).strip()
            questions.append(question_text)
        
        if questions:
            result["questions"] = questions
    
    return result


def format_for_llm(extracted_content):
    """
    Convert the structured content into a plain text format that's easy for LLMs to process
    """
    output = []
    
    # Add title
    if 'title' in extracted_content:
        output.append(f"# {extracted_content['title']}")
        output.append("")
    
    # Process content
    for item in extracted_content["content"]:
        if item["type"] == "heading":
            # Format headings based on level
            prefix = "#" * item["level"]
            output.append(f"{prefix} {item['text']}")
            output.append("")
        
        elif item["type"] == "paragraph":
            output.append(item["text"])
            output.append("")
        
        elif item["type"] == "code":
            language = item["language"] if item["language"] else ""
            output.append(f"```{language}")
            output.append(item["text"])
            output.append("```")
            output.append("")
        
        elif item["type"] == "list":
            for i, list_item in enumerate(item["items"]):
                prefix = f"{i+1}." if item["list_type"] == "ordered" else "-"
                output.append(f"{prefix} {list_item}")
            output.append("")
        
        elif item["type"] == "image":
            output.append(f"[Image: {item['alt']}]")
            output.append("")
        
        elif item["type"] == "table":
            output.append("[Table content summarized]")
            output.append("")
        
        elif item["type"] == "alert":
            output.append("---")
            output.append("Note:")
            output.append(item["text"])
            output.append("---")
            output.append("")
    
    # Add questions
    if "questions" in extracted_content:
        output.append("## Questions")
        output.append("")
        for i, question in enumerate(extracted_content["questions"]):
            output.append(f"Question {i+1}: {question}")
            output.append("")
    
    return "\n".join(output)


def fetch_html_from_url(url):
    """
    Fetch HTML content from a URL
    """
    try:
        # Validate URL
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValueError("Invalid URL. Please include http:// or https://")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching content: {str(e)}")
    
def main():
    parser = argparse.ArgumentParser(description='Extract content from HackTheBox Academy HTML')
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file', '-f', help='Path to a local HTML file')
    input_group.add_argument('--url', '-u', help='URL of the webpage to scrape')
    
    parser.add_argument('--output', '-o', help='Output file (default: output.txt)')
    parser.add_argument('--format', '-m', choices=['text', 'json'], default='text',
                        help='Output format (default: text)')
    
    args = parser.parse_args()
    
    # Get HTML content (either from file or URL)
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            print(f"Read content from file: {args.file}")
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return
    else:  # args.url
        try:
            print(f"Fetching content from URL: {args.url}")
            html_content = fetch_html_from_url(args.url)
            print(f"Successfully fetched content ({len(html_content)} bytes)")
        except Exception as e:
            print(f"Error: {str(e)}")
            return
    
    # Extract and process the content
    content = extract_content(html_content)
    
    # Format output based on selected format
    if args.format == 'json':
        output = json.dumps(content, indent=2)
    else:
        output = format_for_llm(content)
    
    # Write to output file or print to console
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Content saved to {args.output}")
    else:
        print(output)

    @abstractmethod
    def extract_questions(self):
        """Extract questions from the page."""
        pass


class ContentFormatter:
    def __init__(self):
        # Dictionary mapping content types to their formatter methods
        self.formatters = {
            "heading": self.format_heading,
            "paragraph": self.format_paragraph,
            "code": self.format_code_block,
            "list": self.format_list,
            "image": self.format_image,
            "table": self.format_table,
            "alert": self.format_alert
        }

    def format_for_llm(self, extracted_content):
        """
        Convert the structured content into a plain text format that's easy for LLMs to process
        """
        output_lines = []
        output_lines.extend(self.format_title(extracted_content))
        output_lines.extend(self.format_content_items(extracted_content["content"]))
        if "questions" in extracted_content:
            output_lines.extend(self.format_questions(extracted_content["questions"]))
        return "\n".join(output_lines)

    def format_title(self, content):
        """Format the title section"""
        if 'title' in content:
            return [f"# {content['title']}", ""]
        return []

    def format_content_items(self, content_items):
        """Format all content items"""
        output_lines = []
        for item in content_items:
            formatter = self.get_formatter_for_type(item["type"])
            if formatter:
                output_lines.extend(formatter(item))
        return output_lines

    def get_formatter_for_type(self, item_type):
        """Return the appropriate formatter method for the given item type"""
        return self.formatters.get(item_type)

    # Individual formatters for each content type
    def format_heading(self, item):
        """Format a heading item"""
        prefix = "#" * item["level"]
        return [f"{prefix} {item['text']}", ""]

    def format_paragraph(self, item):
        """Format a paragraph item"""
        return [item["text"], ""]

    def format_code_block(self, item):
        """Format a code block item"""
        language = item["language"] if item["language"] else ""
        return [f"```{language}", item["text"], "```", ""]

    def format_list(self, item):
        """Format a list item"""
        result = []
        for i, list_item in enumerate(item["items"]):
            prefix = f"{i+1}." if item["list_type"] == "ordered" else "-"
            result.append(f"{prefix} {list_item}")
        result.append("")
        return result

    def format_image(self, item):
        """Format an image item"""
        return [f"[Image: {item['alt']}]", ""]

    def format_table(self, item):
        """Format a table item"""
        return ["[Table content summarized]", ""]

    def format_alert(self, item):
        """Format an alert/note item"""
        return ["---", "Note:", item["text"], "---", ""]

    def format_questions(self, questions):
        """Format the questions section"""
        result = ["## Questions", ""]
        for i, question in enumerate(questions):
            result.append(f"Question {i+1}: {question}")
            result.append("")
        return result