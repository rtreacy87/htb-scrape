# Updating the Main Script

In this wiki, we'll update the main script to integrate all our authentication changes. This will tie everything together and make the authentication features available to users.

## Understanding the Current Main Script

Currently, the main script in `htb_scraper.py` coordinates the content extraction process. It:

1. Parses command-line arguments
2. Gets HTML content from a file or URL
3. Extracts content with image handling
4. Formats the output
5. Writes to a file or prints to the console

We don't need to make many changes to this file, as most of the authentication logic is handled in the modules we've already updated.

## Step 1: Update the htb_scraper.py file

Let's update the `htb_scraper.py` file to include some informational messages about authentication:

```python
from src.LLMStructuredExtractor import extract_structured_content_from_html
from src.format_for_llm_structured import format_for_llm_structured
import src.htb_scraper_utils as su
import json

def main():
    """Main function to coordinate the content extraction process with LLM-friendly structure"""
    args = su.parse_arguments()
    
    # Print authentication info if enabled
    if args.auth and args.url:
        print("Authentication enabled")
        if args.username:
            print(f"Using username: {args.username}")
        if args.no_keyring:
            print("Keyring disabled - credentials will not be saved")
    
    html_content, base_url = su.get_html_content(args)
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
        su.write_to_file(formatted_content, args.output)
    else:
        print(formatted_content)

if __name__ == '__main__':
    main()
```

## Step 2: Understanding the Updated Main Script

The changes we made are minimal:

1. **Authentication Info**: Added informational messages about authentication
2. **No Functional Changes**: The actual authentication is handled by the modules we updated earlier

This is because we designed our authentication system to be seamlessly integrated with the existing code. The `get_html_content` function now handles authentication internally, so the main script doesn't need to know the details.

## Step 3: Testing the Complete System

Now that we've updated all the necessary files, let's test the complete system:

```bash
# Test with authentication
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --username your.email@example.com

# Test with authentication and no keyring
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --username your.email@example.com --no-keyring

# Test without authentication (for public pages)
python htb_scraper.py --url https://www.example.com
```

## Next Steps

In the next wiki, we'll cover some advanced topics and future improvements.
