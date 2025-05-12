# Complete Implementation Example

In this wiki, we'll provide a complete implementation example that ties together all the components we've created. This will give you a clear picture of how everything works together.

## Project Structure

After implementing all the authentication features, your project structure should look like this:

```
htb-scrape/
├── htb_scraper.py
├── src/
│   ├── __init__.py
│   ├── auth_handler.py
│   ├── htb_auth.py
│   ├── fetch_html_from_url.py
│   ├── htb_scraper_utils.py
│   ├── BaseHTMLExtractor.py
│   ├── LLMStructuredExtractor.py
│   ├── format_for_llm_structured.py
│   └── image_handler.py
├── tests/
│   └── ...
└── docs/
    ├── authentication_design.md
    └── wikis/
        ├── 01_authentication_introduction.md
        ├── 02_creating_auth_handler.md
        ├── ...
        └── 09_complete_implementation.md
```

## Complete Implementation

Let's go through a complete example of how to use the authentication features:

### 1. Running the Script with Authentication

```bash
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --username your.email@example.com
```

### 2. What Happens Behind the Scenes

When you run this command, the following happens:

1. **Argument Parsing**: The script parses the command-line arguments and recognizes that authentication is enabled.

2. **Getting Credentials**: The script gets the username from the command-line argument and prompts for the password.

3. **Authentication**: The script authenticates with HackTheBox Academy using the provided credentials.

4. **Fetching Content**: The script fetches the content from the URL using the authenticated session.

5. **Processing Content**: The script processes the content as usual, extracting the structured data.

6. **Output**: The script outputs the extracted content in the specified format.

### 3. Code Flow

Let's trace the code flow for this example:

```python
# htb_scraper.py
def main():
    # Parse arguments
    args = su.parse_arguments()
    
    # Print authentication info
    if args.auth and args.url:
        print("Authentication enabled")
        if args.username:
            print(f"Using username: {args.username}")
        if args.no_keyring:
            print("Keyring disabled - credentials will not be saved")
    
    # Get HTML content
    html_content, base_url = su.get_html_content(args)
    if html_content is None:
        return
    
    # Process content
    # ...
```

```python
# src/htb_scraper_utils.py
def get_html_content(args):
    if args.file:
        return get_content_from_file(args.file)
    else:  # args.url
        return get_content_from_url(
            args.url,
            auth=args.auth,
            username=args.username,
            use_keyring=not args.no_keyring
        )

def get_content_from_url(url, auth=False, username=None, use_keyring=True):
    try:
        print(f"Fetching content from URL: {url}")
        
        # Use authentication if requested
        if auth:
            print("Using authentication")
            content = fetch_html_from_url(
                url,
                auth=True,
                username=username,
                use_keyring=use_keyring
            )
        else:
            content = fetch_html_from_url(url)
            
        print(f"Successfully fetched content ({len(content)} bytes)")
        return content, url
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None
```

```python
# src/fetch_html_from_url.py
def fetch_html_from_url(url, auth=False, username=None, password=None, use_keyring=True):
    validate_url(url)
    headers = get_browser_headers()
    
    if auth:
        return fetch_with_auth(url, username, password, use_keyring)
    else:
        return make_http_request(url, headers)

def fetch_with_auth(url, username=None, password=None, use_keyring=True):
    # Determine which authentication handler to use
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
    
    # Make the request
    try:
        headers = get_browser_headers()
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching content: {str(e)}")
```

```python
# src/htb_auth.py
class HTBAuthHandler(AuthHandler):
    # ...
    
    def authenticate(self, username=None, password=None):
        # Get domain for keyring
        domain = self.get_domain_from_url(self.HTB_BASE_URL)
        
        # Get credentials
        username, password = self.get_credentials(username, password, domain)
        
        # Get CSRF token
        csrf_token = self._get_csrf_token()
        if not csrf_token:
            print("Failed to get CSRF token")
            return False
        
        # Perform login
        login_success = self._perform_login(username, password, csrf_token)
        if login_success:
            print(f"Successfully logged in as {username}")
            self.is_authenticated = True
            return True
        else:
            print("Login failed. Please check your credentials.")
            return False
```

## Complete Usage Examples

Here are some complete usage examples for different scenarios:

### Basic Authentication

```bash
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth
```

This will:
- Prompt for both username and password
- Save credentials to keyring
- Fetch and process the content

### Authentication with Username

```bash
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --username your.email@example.com
```

This will:
- Use the provided username
- Prompt for password
- Save credentials to keyring
- Fetch and process the content

### Authentication without Keyring

```bash
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --username your.email@example.com --no-keyring
```

This will:
- Use the provided username
- Prompt for password
- Not save credentials to keyring
- Fetch and process the content

### Authentication with Output File

```bash
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --username your.email@example.com --output module_123.json
```

This will:
- Use the provided username
- Prompt for password
- Save credentials to keyring
- Fetch and process the content
- Save the output to module_123.json

### Authentication with Text Format

```bash
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --username your.email@example.com --format text
```

This will:
- Use the provided username
- Prompt for password
- Save credentials to keyring
- Fetch and process the content
- Output in text format instead of JSON

## Conclusion

This complete implementation example shows how all the components work together to provide authentication capabilities for HTB-Scraper. By following the wikis in this series, you should now have a good understanding of how to implement authentication in a Python application.

Remember that this is just the beginning - you can extend and improve the authentication system as needed for your specific requirements. The modular design makes it easy to add support for other websites or authentication methods in the future.
