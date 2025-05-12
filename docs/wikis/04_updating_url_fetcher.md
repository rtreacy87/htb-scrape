# Updating the URL Fetcher

In this wiki, we'll update the URL fetcher to support authenticated requests. This will allow the scraper to access password-protected content.

## Understanding the Current URL Fetcher

Currently, the URL fetcher in `fetch_html_from_url.py` makes simple HTTP requests without authentication. We need to modify it to:

1. Check if authentication is needed
2. Use the appropriate authentication handler
3. Make requests using an authenticated session

## Step 1: Update the fetch_html_from_url.py file

Let's update the `fetch_html_from_url.py` file to support authentication:

```python
"""
Module for fetching HTML content from URLs with optional authentication.
"""
import requests
from urllib.parse import urlparse
from .htb_auth import HTBAuthHandler

def fetch_html_from_url(url, auth=False, username=None, password=None, use_keyring=True):
    """
    Fetch HTML content from a URL, with optional authentication.
    
    Args:
        url (str): The URL to fetch
        auth (bool): Whether to use authentication
        username (str, optional): Username for authentication
        password (str, optional): Password for authentication
        use_keyring (bool): Whether to use the system keyring for credential storage
        
    Returns:
        str: The HTML content
    """
    validate_url(url)
    headers = get_browser_headers()
    
    if auth:
        return fetch_with_auth(url, username, password, use_keyring)
    else:
        return make_http_request(url, headers)

def validate_url(url):
    """
    Validate that the URL is properly formatted.
    
    Args:
        url (str): The URL to validate
        
    Raises:
        ValueError: If the URL is invalid
    """
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        raise ValueError("Invalid URL. Please include http:// or https://")

def get_browser_headers():
    """
    Return headers that mimic a regular browser.
    
    Returns:
        dict: Browser headers
    """
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

def make_http_request(url, headers):
    """
    Make a simple HTTP request without authentication.
    
    Args:
        url (str): The URL to fetch
        headers (dict): HTTP headers
        
    Returns:
        str: The HTML content
        
    Raises:
        RuntimeError: If the request fails
    """
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching content: {str(e)}")

def fetch_with_auth(url, username=None, password=None, use_keyring=True):
    """
    Fetch HTML content using authentication.
    
    Args:
        url (str): The URL to fetch
        username (str, optional): Username for authentication
        password (str, optional): Password for authentication
        use_keyring (bool): Whether to use the system keyring for credential storage
        
    Returns:
        str: The HTML content
        
    Raises:
        RuntimeError: If authentication or the request fails
    """
    # Determine which authentication handler to use based on the URL
    domain = urlparse(url).netloc
    
    # For now, we only support HackTheBox Academy
    if "hackthebox.com" in domain or "hackthebox.eu" in domain:
        auth_handler = HTBAuthHandler(use_keyring=use_keyring)
    else:
        raise RuntimeError(f"Authentication not supported for domain: {domain}")
    
    # Authenticate
    auth_success = auth_handler.authenticate(username, password)
    if not auth_success:
        raise RuntimeError("Authentication failed")
    
    # Get the authenticated session
    session = auth_handler.get_authenticated_session()
    
    # Make the request using the authenticated session
    try:
        headers = get_browser_headers()
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching content: {str(e)}")
```

## Step 2: Understanding the Updated URL Fetcher

Let's break down the changes we made:

1. **New Parameters**: Added `auth`, `username`, `password`, and `use_keyring` parameters
2. **Authentication Check**: Added logic to check if authentication is needed
3. **Domain Detection**: Added logic to determine which authentication handler to use
4. **Authenticated Requests**: Added a new function to fetch content with authentication

## Step 3: Testing the Updated URL Fetcher

To make sure our updated URL fetcher works correctly, let's create a simple test script:

```python
# test_url_fetcher.py
from src.fetch_html_from_url import fetch_html_from_url

def test_url_fetcher():
    # Test without authentication
    try:
        content = fetch_html_from_url("https://www.example.com")
        print(f"Fetched {len(content)} bytes without authentication")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test with authentication
    try:
        content = fetch_html_from_url(
            "https://academy.hackthebox.com/dashboard",
            auth=True,
            use_keyring=False
        )
        print(f"Fetched {len(content)} bytes with authentication")
        
        # Check if we got the dashboard
        if "Dashboard" in content and "Login" not in content:
            print("Authentication successful!")
        else:
            print("Authentication may have failed")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_url_fetcher()
```

You can run this test script to make sure the URL fetcher works with and without authentication.

## Next Steps

In the next wiki, we'll update the command-line interface to support authentication options.
