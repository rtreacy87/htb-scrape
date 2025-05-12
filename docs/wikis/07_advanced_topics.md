# Advanced Topics and Future Improvements

In this wiki, we'll cover some advanced topics and future improvements for the authentication system in HTB-Scraper.

## Error Handling and Debugging

### Adding Better Error Messages

To make the tool more user-friendly, we can add more detailed error messages:

```python
def fetch_with_auth(url, username=None, password=None, use_keyring=True):
    """Fetch HTML content using authentication."""
    try:
        # Existing code...
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Connection error: Could not connect to {url}. Check your internet connection.")
    except requests.exceptions.Timeout:
        raise RuntimeError(f"Timeout error: The request to {url} timed out. Try again later.")
    except requests.exceptions.TooManyRedirects:
        raise RuntimeError(f"Redirect error: Too many redirects for {url}. The URL may be incorrect.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching content: {str(e)}")
```

### Adding Debug Mode

We can add a debug mode to help troubleshoot issues:

```python
def fetch_html_from_url(url, auth=False, username=None, password=None, use_keyring=True, debug=False):
    """Fetch HTML content from a URL, with optional authentication."""
    if debug:
        print(f"Debug: Fetching URL {url}")
        print(f"Debug: Authentication enabled: {auth}")
        if auth:
            print(f"Debug: Username provided: {username is not None}")
            print(f"Debug: Using keyring: {use_keyring}")
    
    # Existing code...
```

## Supporting Multiple Authentication Methods

### Adding OAuth Support

For websites that use OAuth authentication:

```python
class OAuthHandler(AuthHandler):
    """Handles OAuth authentication."""
    
    def __init__(self, client_id, client_secret, redirect_uri, use_keyring=True):
        super().__init__(use_keyring)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.refresh_token = None
    
    def authenticate(self):
        """Authenticate using OAuth."""
        # Implementation details...
```

### Adding Two-Factor Authentication Support

For websites that require two-factor authentication:

```python
class TwoFactorAuthHandler(AuthHandler):
    """Handles two-factor authentication."""
    
    def authenticate(self, username=None, password=None):
        """Authenticate with two-factor authentication."""
        # Get credentials
        username, password = self.get_credentials(username, password)
        
        # Perform initial login
        login_success = self._perform_login(username, password)
        if not login_success:
            return False
        
        # Get two-factor code
        code = input("Enter two-factor authentication code: ")
        
        # Submit two-factor code
        return self._submit_two_factor_code(code)
```

## Improving Security

### Using Environment Variables

Instead of command-line arguments, we can use environment variables for credentials:

```python
def get_credentials_from_env():
    """Get credentials from environment variables."""
    import os
    username = os.environ.get('HTB_USERNAME')
    password = os.environ.get('HTB_PASSWORD')
    return username, password
```

### Implementing Token Rotation

For long-running processes, we can implement token rotation:

```python
def refresh_token_if_needed(self):
    """Refresh the authentication token if it's about to expire."""
    if self.token_expiry and time.time() > self.token_expiry - 300:  # 5 minutes before expiry
        self.refresh_token()
```

## Performance Improvements

### Session Caching

We can cache sessions to avoid re-authenticating unnecessarily:

```python
class SessionCache:
    """Cache for authenticated sessions."""
    
    def __init__(self, max_age=3600):  # Default: 1 hour
        self.sessions = {}
        self.max_age = max_age
    
    def get_session(self, domain, username):
        """Get a cached session if available and not expired."""
        key = f"{domain}:{username}"
        if key in self.sessions:
            session_data = self.sessions[key]
            if time.time() - session_data['timestamp'] < self.max_age:
                return session_data['session']
        return None
    
    def store_session(self, domain, username, session):
        """Store a session in the cache."""
        key = f"{domain}:{username}"
        self.sessions[key] = {
            'session': session,
            'timestamp': time.time()
        }
```

### Parallel Processing

For scraping multiple pages, we can use parallel processing:

```python
def fetch_multiple_urls(urls, auth=False, username=None, password=None, use_keyring=True):
    """Fetch multiple URLs in parallel."""
    import concurrent.futures
    
    # Authenticate once
    if auth:
        auth_handler = HTBAuthHandler(use_keyring=use_keyring)
        auth_success = auth_handler.authenticate(username, password)
        if not auth_success:
            raise RuntimeError("Authentication failed")
        session = auth_handler.get_authenticated_session()
    else:
        session = requests.Session()
    
    # Fetch URLs in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {
            executor.submit(fetch_url_with_session, url, session): url
            for url in urls
        }
        results = {}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                results[url] = future.result()
            except Exception as e:
                results[url] = str(e)
    
    return results
```

## User Experience Improvements

### Interactive Mode

We can add an interactive mode for easier use:

```python
def interactive_mode():
    """Run the scraper in interactive mode."""
    print("HTB-Scraper Interactive Mode")
    print("----------------------------")
    
    # Get URL
    url = input("Enter URL to scrape: ")
    
    # Ask about authentication
    auth = input("Use authentication? (y/n): ").lower() == 'y'
    
    if auth:
        # Get username
        username = input("Username: ")
        
        # Ask about keyring
        use_keyring = input("Save credentials to keyring? (y/n): ").lower() == 'y'
        
        # Run with authentication
        content = fetch_html_from_url(url, auth=True, username=username, use_keyring=use_keyring)
    else:
        # Run without authentication
        content = fetch_html_from_url(url)
    
    # Process content...
```

### Configuration File

We can add support for a configuration file:

```python
def load_config():
    """Load configuration from a config file."""
    import os
    import configparser
    
    config = configparser.ConfigParser()
    
    # Look for config file in standard locations
    config_paths = [
        './htb-scraper.ini',
        os.path.expanduser('~/.htb-scraper.ini'),
        '/etc/htb-scraper.ini'
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            config.read(path)
            return config
    
    # Return empty config if no file found
    return config
```

## Testing and Documentation

### Unit Tests

We should add unit tests for the authentication system:

```python
# test_auth_handler.py
import unittest
from unittest.mock import patch, MagicMock
from src.auth_handler import AuthHandler

class TestAuthHandler(unittest.TestCase):
    
    def test_get_domain_from_url(self):
        auth = AuthHandler()
        domain = auth.get_domain_from_url("https://academy.hackthebox.com/module/123")
        self.assertEqual(domain, "academy.hackthebox.com")
    
    @patch('getpass.getpass')
    def test_prompt_for_password(self, mock_getpass):
        mock_getpass.return_value = "test_password"
        auth = AuthHandler()
        password = auth.prompt_for_password()
        self.assertEqual(password, "test_password")
        mock_getpass.assert_called_once_with("Password: ")
    
    # More tests...
```

### Documentation

We should add comprehensive documentation:

```python
def authenticate(self, username=None, password=None):
    """
    Authenticate with HackTheBox Academy.
    
    This method handles the authentication process for HackTheBox Academy.
    It will:
    1. Get credentials from arguments, keyring, or user input
    2. Get the CSRF token from the login page
    3. Submit the login form with credentials and token
    4. Check if login was successful
    
    Args:
        username (str, optional): Username provided via arguments
        password (str, optional): Password provided via arguments
        
    Returns:
        bool: True if authentication was successful, False otherwise
        
    Examples:
        >>> auth = HTBAuthHandler()
        >>> success = auth.authenticate("user@example.com", "password123")
        >>> if success:
        ...     session = auth.get_authenticated_session()
    """
    # Implementation...
```

## Conclusion

These advanced topics and future improvements will make the authentication system more robust, secure, and user-friendly. As you continue to develop the HTB-Scraper tool, consider implementing these features based on user feedback and needs.

Remember that security should always be a top priority when handling authentication, so regularly review and update the security measures in the code.
