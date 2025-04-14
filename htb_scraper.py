from src.HTBHTMLExtractor import extract_content_from_html
import src.main_functions as mf

def main():
    """Main function to coordinate the content extraction process"""
    args = mf.parse_arguments()
    html_content = mf.get_html_content(args)
    if html_content is None:
        return  
    content = extract_content_from_html(html_content)
    mf.output_formatted_content(content, args)

if __name__ == '__main__':
    main()