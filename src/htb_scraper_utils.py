import json
import argparse
from src.format_for_llm_structured import format_for_llm_structured as format_for_llm
from src.fetch_html_from_url import fetch_html_from_url

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Extract content from HackTheBox Academy HTML')
    # Input source group (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file', '-f', help='Path to a local HTML file')
    input_group.add_argument('--url', '-u', help='URL of the webpage to scrape')
    # Output options
    parser.add_argument('--output', '-o', help='Output file (default: output.txt)')
    parser.add_argument('--format', '-m', choices=['text', 'json'], default='json',
                        help='Output format (default: text)')
    # Image options
    parser.add_argument('--download-images', '-d', action='store_true', default=True,
                        help='Download images (default: True)')
    parser.add_argument('--image-dir', '-i', default='images',
                        help='Directory to save downloaded images (default: images)')
    return parser.parse_args()

def get_html_content(args):
    """Get HTML content from either a file or URL"""
    if args.file:
        return get_content_from_file(args.file)
    else:  # args.url
        return get_content_from_url(args.url)

def get_content_from_file(file_path):
    """Read HTML content from a local file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Read content from file: {file_path}")
        return content, file_path  # Use file path as base URL for resolving relative paths
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None, None

def get_content_from_url(url):
    """Fetch HTML content from a URL"""
    try:
        print(f"Fetching content from URL: {url}")
        content = fetch_html_from_url(url)
        print(f"Successfully fetched content ({len(content)} bytes)")
        return content, url
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

def output_formatted_content(content, args):
    """Format and output the content based on user preferences"""
    formatted_content = format_content(content, args.format)
    if args.output:
        write_to_file(formatted_content, args.output)
    else:
        print(formatted_content)

def format_content(content, format_type):
    """Format content as either JSON or LLM-friendly text"""
    if format_type == 'json':
        return json.dumps(content, indent=2)
    else:
        return format_for_llm(content)

def write_to_file(content, file_path):
    """Write content to a file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content saved to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {str(e)}")
