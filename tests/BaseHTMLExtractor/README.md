# BaseHTMLExtractor Tests

This directory contains tests for the `BaseHTMLExtractor` class, which is responsible for extracting and processing HTML content.

## Test Categories

The tests are organized by the method they are testing, with each test having a unique identifier (SCP_BHTML###).

### Code Block Processing Tests

#### **test_process_code_block_with_language_SCP_BHTML005**:
Tests processing of code blocks with a specified language class. It takes the following input:
```html
<pre class="language-python">def test(): pass</pre>
```
it should return a dictionary with the type as "code", language as "python", and text as "def test(): pass". This tests the method's ability to correctly identify and extract the language from the class attribute as well as the code text.

#### **test_process_code_block_without_language_SCP_BHTML010**:
Tests processing of code blocks without a language class. It takes the following input:
```html
<pre>print("hello")</pre>
```
it should return a dictionary with the type as "code", language as an empty string, and text as 'print("hello")'. This tests the method's behavior when no language is specified.

#### **test_process_code_block_multiple_classes_SCP_BHTML015**:
Tests processing of code blocks with multiple classes including a language class. It takes the following input:
```html
<pre class="highlight language-javascript code-block">const x = 1;</pre>
```
it should return a dictionary with the type as "code", language as "javascript", and text as "const x = 1;". This tests the method's ability to extract the language from a class attribute with multiple classes.

#### **test_process_code_block_empty_SCP_BHTML020**:
Tests processing of empty code blocks. It takes the following input:
```html
<pre class="language-ruby">    </pre>
```
it should return a dictionary with the type as "code", language as "ruby", and text as an empty string. This tests the method's handling of code blocks with only whitespace.

### Paragraph Processing Tests

#### **test_process_paragraph_with_text_SCP_BHTML025**:
Tests processing of paragraphs with regular text. It takes the following input:
```html
<p>This is a test paragraph.</p>
```
it should return a dictionary with the type as "paragraph" and text as "This is a test paragraph.". This tests the basic paragraph processing functionality.

#### **test_process_paragraph_empty_SCP_BHTML030**:
Tests processing of empty paragraphs. It takes the following input:
```html
<p>    </p>
```
it should return None. This tests the method's handling of paragraphs with only whitespace.

#### **test_process_paragraph_with_nested_elements_SCP_BHTML035**:
Tests processing of paragraphs with nested HTML elements. It takes the following input:
```html
<p>Text with <strong>bold</strong> and <em>italic</em> content.</p>
```
it should return a dictionary with the type as "paragraph" and text as "Text with bold and italic content.". This tests the method's ability to extract text from paragraphs with nested HTML elements.

#### **test_process_paragraph_with_newlines_SCP_BHTML040**:
Tests processing of paragraphs with newlines and extra spaces. It takes the following input:
```html
<p>
    Multiple
    lines with    spaces
</p>
```
it should return a dictionary with the type as "paragraph" and text as "Multiple lines with spaces". This tests the method's ability to normalize whitespace in paragraphs.

### Image Processing Tests

#### **test_process_image_with_src_and_alt_SCP_BHTML045**:
Tests processing of images with both src and alt attributes. It takes the following input:
```html
<img src="test.jpg" alt="Test Image">
```
it should return a dictionary with the type as "image", src as "test.jpg", and alt as "Test Image". This tests the basic image processing functionality.

#### **test_process_image_without_alt_SCP_BHTML050**:
Tests processing of images without an alt attribute. It takes the following input:
```html
<img src="test.jpg">
```
it should return a dictionary with the type as "image", src as "test.jpg", and alt as "Image" (default value). This tests the method's handling of images without alt text.

#### **test_process_image_empty_attributes_SCP_BHTML055**:
Tests processing of images with empty attributes. It takes the following input:
```html
<img src="" alt="">
```
it should return a dictionary with the type as "image", src as an empty string, and alt as "Image" (default value). This tests the method's handling of images with empty attributes.

### Alert Processing Tests

#### **test_process_alert_with_text_SCP_BHTML060**:
Tests processing of alerts with regular text. It takes the following input:
```html
<div class="card">This is an alert message</div>
```
it should return a dictionary with the type as "alert" and text as "This is an alert message". This tests the basic alert processing functionality.

#### **test_process_alert_with_nested_elements_SCP_BHTML065**:
Tests processing of alerts with nested HTML elements. It takes the following input:
```html
<div class="card"><strong>Warning:</strong> Important alert <em>message</em></div>
```
it should return a dictionary with the type as "alert" and text as "Warning: Important alert message". This tests the method's ability to extract text from alerts with nested HTML elements.

#### **test_process_alert_empty_SCP_BHTML070**:
Tests processing of empty alerts. It takes the following input:
```html
<div class="card">    </div>
```
it should return None. This tests the method's handling of alerts with only whitespace.

#### **test_process_alert_with_newlines_SCP_BHTML075**:
Tests processing of alerts with newlines and extra spaces. It takes the following input:
```html
<div class="card">
    Multiple
    lines with    spaces
</div>
```
it should return a dictionary with the type as "alert" and text as "Multiple lines with spaces". This tests the method's ability to normalize whitespace in alerts.

### Table Processing Tests

#### **test_process_table_basic_SCP_BHTML080**:
Tests basic table processing. It takes the following input:
```html
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
```
it should return a dictionary with the type as "table" and text as "Table content (summarized for brevity)". This tests the basic table processing functionality.

#### **test_process_table_cell_SCP_BHTML150**:
Tests processing of table cells with text and images. It tests various table cell scenarios including:
- Cell with text only
- Cell with image only
- Cell with both text and image
- Empty cell
- Cell with multiple images

This tests the method's ability to process different types of content within table cells.

### List Processing Tests

#### **test_process_list_ordered_SCP_BHTML085**:
Tests processing of ordered lists. It takes the following input:
```html
<ol>
    <li>First item</li>
    <li>Second item</li>
    <li>Third item</li>
</ol>
```
it should return a dictionary with the type as "list", list_type as "ordered", and items as ["First item", "Second item", "Third item"]. This tests the method's ability to process ordered lists.

#### **test_process_list_unordered_SCP_BHTML090**:
Tests processing of unordered lists. It takes the following input:
```html
<ul>
    <li>Apple</li>
    <li>Banana</li>
    <li>Orange</li>
</ul>
```
it should return a dictionary with the type as "list", list_type as "unordered", and items as ["Apple", "Banana", "Orange"]. This tests the method's ability to process unordered lists.

#### **test_process_list_with_nested_elements_SCP_BHTML095**:
Tests processing of lists with nested HTML elements. It takes the following input:
```html
<ul>
    <li>Plain text</li>
    <li>Text with <strong>bold</strong> content</li>
    <li>Text with <em>italic</em> and <code>code</code></li>
</ul>
```
it should return a dictionary with the type as "list", list_type as "unordered", and items containing the text with formatting removed. This tests the method's ability to extract text from list items with nested HTML elements.

#### **test_process_list_empty_SCP_BHTML100**:
Tests processing of empty lists. It takes the following input:
```html
<ol>
    <li>    </li>
    <li></li>
</ol>
```
it should return a dictionary with the type as "list", list_type as "ordered", and items as ["", ""]. This tests the method's handling of lists with empty items.

#### **test_process_list_item_SCP_BHTML155**:
Tests processing of list items with text and images. It tests various list item scenarios including:
- List item with text only
- List item with image only
- List item with both text and image
- Empty list item

This tests the method's ability to process different types of content within list items.

### Heading Processing Tests

#### **test_process_heading_basic_SCP_BHTML105**:
Tests basic heading processing for different levels (h1-h6). It tests various heading elements (h1 through h6) and verifies that the correct level and text are extracted. This tests the method's ability to process headings of different levels.

#### **test_process_heading_with_nested_elements_SCP_BHTML110**:
Tests processing of headings with nested HTML elements. It takes the following input:
```html
<h2>Title with <strong>bold</strong> and <em>italic</em> text</h2>
```
it should return a dictionary with the type as "heading", level as 2, and text as "Title with bold and italic text". This tests the method's ability to extract text from headings with nested HTML elements.

#### **test_process_heading_with_whitespace_SCP_BHTML115**:
Tests processing of headings with extra whitespace. It takes the following input:
```html
<h1>
    Heading with    extra
    spaces
</h1>
```
it should return a dictionary with the type as "heading", level as 1, and text as "Heading with extra spaces". This tests the method's ability to normalize whitespace in headings.

### Content Element Processing Tests

#### **test_process_content_elements_mixed_content_SCP_BHTML120**:
Tests processing of mixed content elements. It takes a complex HTML structure with various elements (headings, paragraphs, code blocks, alerts, lists) and verifies that all elements are processed correctly and in the right order. This tests the method's ability to process a mix of different HTML elements.

#### **test_process_content_elements_mixed_content_SCP_BHTML175**:
Tests processing of mixed content elements with a focus on list items. It takes a complex HTML structure with various elements including lists and verifies that list items are processed correctly. This tests the method's handling of list items within a mixed content context.

### Element Processing Tests

#### **test_process_single_element_SCP_BHTML125**:
Tests processing of single HTML elements. It tests various HTML elements (paragraphs, code blocks, alerts, etc.) and verifies that each is processed correctly. This tests the method's ability to process individual HTML elements.

#### **test_process_standard_element_SCP_BHTML145**:
Tests processing of standard HTML elements. It tests various standard HTML elements and verifies that each is processed correctly. This tests the method's ability to process standard HTML elements using the appropriate processor.

#### **test_process_image_element_SCP_BHTML160**:
Tests processing of image elements. It tests various image scenarios including:
- Valid image with src and alt
- Image with src only
- Invalid image without src

This tests the method's ability to process different types of image elements.

### Utility Method Tests

#### **test_is_valid_element_SCP_BHTML130**:
Tests validation of HTML elements. It tests various types of elements (valid HTML elements, comments, text nodes, etc.) and verifies that the method correctly identifies valid elements. This tests the method's ability to validate HTML elements.

#### **test_get_element_processor_map_SCP_BHTML135**:
Tests retrieval of element processor mapping. It verifies that the method returns a mapping of HTML elements to their processor methods and that all expected elements are mapped. This tests the method's ability to provide a mapping of element processors.

#### **test_extract_title_SCP_BHTML140**:
Tests extraction of page titles from various elements. It tests different title scenarios (h4 with page-title class, h1 with page-title class, regular h1, title tag, etc.) and verifies that the method extracts the title according to the specified precedence. This tests the method's ability to extract page titles.

#### **test_should_stop_recursion_SCP_BHTML165**:
Tests recursion depth limit checking. It verifies that the method correctly determines when to stop recursion based on the current depth and maximum depth. This tests the method's ability to prevent infinite recursion.

### Container Processing Tests

#### **test_process_container_children_SCP_BHTML140**:
Tests processing of container children elements. It takes a complex HTML structure with nested container elements and verifies that all nested elements are processed correctly. This tests the method's ability to process nested container elements.

#### **test_process_elements_in_order_SCP_BHTML170**:
Tests processing of elements in order with proper nesting. It takes a complex HTML structure with various elements in a specific order and verifies that all elements are processed in the correct order. This tests the method's ability to maintain the order of elements during processing.

## Running the Tests

To run all tests in this directory:

```powershell
# Activate the conda environment
conda activate scrape

# Run the tests
python -m pytest BaseHTMLExtractor\test_BaseHTMLExtractor.py
```

To run a specific test:

```powershell
python -m pytest BaseHTMLExtractor\test_BaseHTMLExtractor.py::test_process_code_block_with_language_SCP_BHTML005
```

## Test Structure

Each test follows a similar structure:

1. **Setup**: Create test data and initialize necessary objects
2. **Execute**: Call the method being tested
3. **Assert**: Verify the results match the expected output

Most tests use a concrete implementation of the abstract `BaseHTMLExtractor` class for testing purposes.