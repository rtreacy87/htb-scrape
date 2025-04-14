from src.LLMStructuredExtractor import extract_structured_content_from_html
from src.format_for_llm_structured import format_for_llm_structured
import src.main_functions as mf
import json

def main():
    """Main function to coordinate the content extraction process with LLM-friendly structure"""
    args = mf.parse_arguments()
    html_content, base_url = mf.get_html_content(args)
    if html_content is None:
        return

    # Create image directory if it doesn't exist
    if args.download_images and args.image_dir:
        import os
        os.makedirs(args.image_dir, exist_ok=True)

    # Extract content with image handling and LLM-friendly structure
    content = extract_structured_content_from_html(
        html_content,
        base_url=base_url,
        download_images=args.download_images,
        image_output_dir=args.image_dir
    )

    # Format output based on selected format
    if args.format == 'json':
        formatted_content = json.dumps(content, indent=2)
    else:
        formatted_content = format_for_llm_structured(content)

    # Write to output file or print to console
    if args.output:
        mf.write_to_file(formatted_content, args.output)
    else:
        print(formatted_content)

if __name__ == '__main__':
    main()
