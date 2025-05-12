# Updating the Command-Line Interface

In this wiki, we'll update the command-line interface to support authentication options. This will allow users to enable authentication and provide credentials when running the tool.

## Understanding the Current Command-Line Interface

Currently, the command-line interface in `htb_scraper_utils.py` provides options for input sources, output formats, and image handling. We need to add options for:

1. Enabling authentication
2. Providing a username
3. Disabling keyring usage

## Step 1: Update the htb_scraper_utils.py file

Let's update the `parse_arguments` function in `htb_scraper_utils.py`:

```python
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
    
    # Authentication options
    parser.add_argument('--auth', '-a', action='store_true',
                        help='Enable authentication for password-protected sites')
    parser.add_argument('--username', help='Username for authentication')
    parser.add_argument('--no-keyring', action='store_true',
                        help='Disable keyring for credential storage')
    
    return parser.parse_args()
```

We also need to update the `get_content_from_url` function to support authentication:

```python
def get_content_from_url(url, auth=False, username=None, use_keyring=True):
    """
    Fetch HTML content from a URL, with optional authentication.
    
    Args:
        url (str): The URL to fetch
        auth (bool): Whether to use authentication
        username (str, optional): Username for authentication
        use_keyring (bool): Whether to use the system keyring for credential storage
        
    Returns:
        tuple: (HTML content, base URL) or (None, None) if an error occurs
    """
    try:
        print(f"Fetching content from URL: {url}")
        
        # Use authentication if requested
        if auth:
            print("Using authentication")
            content = fetch_html_from_url(
                url,
                auth=True,
                username=username,
                use_keyring=not use_keyring
            )
        else:
            content = fetch_html_from_url(url)
            
        print(f"Successfully fetched content ({len(content)} bytes)")
        return content, url
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None
```

Finally, we need to update the `get_html_content` function to pass authentication parameters:

```python
def get_html_content(args):
    """
    Get HTML content from either a file or URL.
    
    Args:
        args: Command-line arguments
        
    Returns:
        tuple: (HTML content, base URL) or (None, None) if an error occurs
    """
    if args.file:
        return get_content_from_file(args.file)
    else:  # args.url
        return get_content_from_url(
            args.url,
            auth=args.auth,
            username=args.username,
            use_keyring=not args.no_keyring
        )
```

## Step 2: Understanding the Updated Command-Line Interface

Let's break down the changes we made:

1. **New Arguments**: Added `--auth`, `--username`, and `--no-keyring` options
2. **Updated URL Fetcher**: Modified `get_content_from_url` to support authentication
3. **Parameter Passing**: Updated `get_html_content` to pass authentication parameters

## Step 3: Testing the Updated Command-Line Interface

To make sure our updated command-line interface works correctly, let's create a simple test script:

```python
# test_cli.py
import sys
from src.htb_scraper_utils import parse_arguments, get_html_content

def test_cli():
    # Simulate command-line arguments
    sys.argv = [
        'htb_scraper.py',
        '--url', 'https://academy.hackthebox.com/dashboard',
        '--auth',
        '--username', 'test@example.com',
        '--no-keyring'
    ]
    
    # Parse arguments
    args = parse_arguments()
    
    # Print parsed arguments
    print(f"URL: {args.url}")
    print(f"Auth: {args.auth}")
    print(f"Username: {args.username}")
    print(f"No Keyring: {args.no_keyring}")
    
    # Try to get content
    content, base_url = get_html_content(args)
    
    if content:
        print(f"Successfully fetched {len(content)} bytes from {base_url}")
    else:
        print("Failed to fetch content")

if __name__ == "__main__":
    test_cli()
```

You can run this test script to make sure the command-line interface works with authentication options.

## Next Steps

In the next wiki, we'll update the main script to integrate all our changes.
