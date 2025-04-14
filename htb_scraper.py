from src.HTBHTMLExtractor import extract_content_from_html
import src.main_functions as mf

def main():
    """Main function to coordinate the content extraction process"""
    args = mf.parse_arguments()
    html_content, base_url = mf.get_html_content(args)
    if html_content is None:
        return

    # Create image directory if it doesn't exist
    if args.download_images and args.image_dir:
        import os
        os.makedirs(args.image_dir, exist_ok=True)

    # Extract content with image handling
    content = extract_content_from_html(
        html_content,
        base_url=base_url,
        download_images=args.download_images,
        image_output_dir=args.image_dir
    )

    mf.output_formatted_content(content, args)

if __name__ == '__main__':
    main()