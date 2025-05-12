# Google Sign-In Authentication

In this wiki, we'll implement Google Sign-In authentication for HTB-Scraper. This will allow users to authenticate with HackTheBox Academy using their Google accounts.

## Understanding Google Sign-In

Many websites, including HackTheBox Academy, offer Google Sign-In as an authentication option. This is implemented using OAuth 2.0, which is a standard protocol for authorization. The process involves:

1. Redirecting the user to Google's authentication page
2. The user grants permission to the application
3. Google redirects back to the website with an authorization code
4. The website exchanges this code for access tokens
5. The website uses these tokens to authenticate the user

## Challenges with Automated Google Sign-In

Automating Google Sign-In is challenging because:

1. Google has security measures to prevent automated logins
2. The process requires user interaction in a browser
3. Google may require CAPTCHA or two-factor authentication

To work around these challenges, we'll use a browser automation approach with Selenium.

## Step 1: Install Required Dependencies

First, let's install the necessary dependencies:

```bash
pip install selenium webdriver-manager
```

You'll also need a compatible browser (Chrome or Firefox) installed on your system.

## Step 2: Create the Google Auth Handler

Let's create a new file called `google_auth.py` in the `src` directory:

```python
"""
Google Sign-In authentication handler for HTB-Scraper.
Uses Selenium to automate the Google Sign-In process.
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from .auth_handler import AuthHandler

class GoogleAuthHandler(AuthHandler):
    """
    Handles authentication via Google Sign-In.
    Uses Selenium to automate the browser interaction.
    """
    
    # HackTheBox URLs
    HTB_BASE_URL = "https://academy.hackthebox.com"
    HTB_LOGIN_URL = "https://academy.hackthebox.com/login"
    HTB_DASHBOARD_URL = "https://academy.hackthebox.com/dashboard"
    
    def __init__(self, use_keyring=True, headless=False):
        """
        Initialize the Google authentication handler.
        
        Args:
            use_keyring (bool): Whether to use the system keyring for credential storage
            headless (bool): Whether to run the browser in headless mode
        """
        super().__init__(use_keyring)
        self.is_authenticated = False
        self.headless = headless
        self.driver = None
        self.cookies = None
    
    def authenticate(self, username=None, password=None):
        """
        Authenticate with HackTheBox Academy using Google Sign-In.
        
        Args:
            username (str, optional): Google email address
            password (str, optional): Google password
            
        Returns:
            bool: True if authentication was successful, False otherwise
        """
        # Get domain for keyring
        domain = self.get_domain_from_url(self.HTB_BASE_URL)
        
        # Get credentials
        username, password = self.get_credentials(username, password, domain)
        
        try:
            # Initialize the browser
            self._initialize_browser()
            
            # Navigate to HackTheBox login page
            self.driver.get(self.HTB_LOGIN_URL)
            
            # Click on the Google Sign-In button
            self._click_google_signin_button()
            
            # Handle Google login
            login_success = self._perform_google_login(username, password)
            
            if not login_success:
                print("Google login failed. Please check your credentials.")
                self._cleanup_browser()
                return False
            
            # Check if we're redirected to the dashboard
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.url_contains(self.HTB_DASHBOARD_URL)
                )
                print(f"Successfully logged in as {username}")
                
                # Save cookies for future requests
                self._save_cookies()
                
                self.is_authenticated = True
                self._cleanup_browser()
                return True
            except TimeoutException:
                print("Login failed. Not redirected to dashboard.")
                self._cleanup_browser()
                return False
                
        except Exception as e:
            print(f"Error during Google authentication: {str(e)}")
            self._cleanup_browser()
            return False
    
    def _initialize_browser(self):
        """Initialize the Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.implicitly_wait(10)
    
    def _cleanup_browser(self):
        """Clean up the browser resources."""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def _click_google_signin_button(self):
        """Click on the Google Sign-In button on the HackTheBox login page."""
        try:
            # Wait for the Google Sign-In button to be clickable
            google_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.google-btn"))
            )
            google_button.click()
            return True
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error finding Google Sign-In button: {str(e)}")
            return False
    
    def _perform_google_login(self, username, password):
        """
        Perform the Google login process.
        
        Args:
            username (str): Google email address
            password (str): Google password
            
        Returns:
            bool: True if login was successful, False otherwise
        """
        try:
            # Wait for the email input field
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.send_keys(username)
            
            # Click the Next button
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            
            # Wait for the password input field
            password_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "password"))
            )
            password_input.send_keys(password)
            
            # Click the Next button
            password_next = self.driver.find_element(By.ID, "passwordNext")
            password_next.click()
            
            # Wait for the Google login to complete
            time.sleep(5)
            
            # Check if we're still on a Google page (which might indicate an error)
            if "google.com" in self.driver.current_url:
                # Check for common error messages
                if "Wrong password" in self.driver.page_source:
                    print("Google login failed: Wrong password")
                    return False
                elif "couldn't find your Google Account" in self.driver.page_source:
                    print("Google login failed: Account not found")
                    return False
                elif "unusual activity" in self.driver.page_source:
                    print("Google login failed: Unusual activity detected")
                    return False
                else:
                    print("Google login failed: Unknown error")
                    return False
            
            return True
        except Exception as e:
            print(f"Error during Google login: {str(e)}")
            return False
    
    def _save_cookies(self):
        """Save cookies from the browser session."""
        if self.driver:
            self.cookies = self.driver.get_cookies()
            
            # Apply cookies to our requests session
            for cookie in self.cookies:
                self.session.cookies.set(
                    cookie['name'],
                    cookie['value'],
                    domain=cookie['domain']
                )
    
    def get_authenticated_session(self):
        """
        Get the authenticated session.
        
        Returns:
            requests.Session: The authenticated session
        """
        if not self.is_authenticated:
            print("Warning: Session is not authenticated")
        return self.session
```

## Step 3: Update the URL Fetcher

Now, let's update the `fetch_html_from_url.py` file to support Google Sign-In:

```python
# Add this import at the top
from .google_auth import GoogleAuthHandler

# Update the fetch_with_auth function
def fetch_with_auth(url, username=None, password=None, use_keyring=True, auth_method='password'):
    """
    Fetch HTML content using authentication.
    
    Args:
        url (str): The URL to fetch
        username (str, optional): Username for authentication
        password (str, optional): Password for authentication
        use_keyring (bool): Whether to use the system keyring for credential storage
        auth_method (str): Authentication method ('password' or 'google')
        
    Returns:
        str: The HTML content
        
    Raises:
        RuntimeError: If authentication or the request fails
    """
    # Determine which authentication handler to use based on the URL
    domain = urlparse(url).netloc
    
    # For now, we only support HackTheBox Academy
    if "hackthebox.com" in domain or "hackthebox.eu" in domain:
        if auth_method == 'google':
            auth_handler = GoogleAuthHandler(use_keyring=use_keyring)
        else:
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

## Step 4: Update the Command-Line Interface

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
    parser.add_argument('--auth-method', choices=['password', 'google'], default='password',
                        help='Authentication method (default: password)')
    parser.add_argument('--headless', action='store_true',
                        help='Run browser in headless mode for Google authentication')
    
    return parser.parse_args()
```

Also update the `get_content_from_url` function:

```python
def get_content_from_url(url, auth=False, username=None, use_keyring=True, auth_method='password', headless=False):
    """
    Fetch HTML content from a URL, with optional authentication.
    
    Args:
        url (str): The URL to fetch
        auth (bool): Whether to use authentication
        username (str, optional): Username for authentication
        use_keyring (bool): Whether to use the system keyring for credential storage
        auth_method (str): Authentication method ('password' or 'google')
        headless (bool): Whether to run browser in headless mode for Google authentication
        
    Returns:
        tuple: (HTML content, base URL) or (None, None) if an error occurs
    """
    try:
        print(f"Fetching content from URL: {url}")
        
        # Use authentication if requested
        if auth:
            print(f"Using authentication method: {auth_method}")
            content = fetch_html_from_url(
                url,
                auth=True,
                username=username,
                use_keyring=use_keyring,
                auth_method=auth_method,
                headless=headless
            )
        else:
            content = fetch_html_from_url(url)
            
        print(f"Successfully fetched content ({len(content)} bytes)")
        return content, url
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None
```

And update the `get_html_content` function:

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
            use_keyring=not args.no_keyring,
            auth_method=args.auth_method,
            headless=args.headless if hasattr(args, 'headless') else False
        )
```

## Step 5: Usage Examples

Here are some examples of how to use Google Sign-In authentication:

```bash
# Basic Google Sign-In authentication
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --auth-method google

# Google Sign-In with username
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --auth-method google --username your.email@gmail.com

# Google Sign-In in headless mode
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --auth-method google --headless
```

## Troubleshooting Google Sign-In

### Browser Automation Issues

If you encounter issues with browser automation:

1. Make sure you have Chrome installed
2. Try disabling headless mode to see what's happening
3. Check if Google is requiring additional verification

### CAPTCHA and Security Challenges

Google may present CAPTCHA or security challenges if it detects unusual activity:

1. Try logging in manually first
2. Use the same machine and IP address that you normally use
3. Consider using cookies from a manual login session

### Two-Factor Authentication

If your Google account has two-factor authentication enabled:

1. You may need to create an app password in your Google account settings
2. Use this app password instead of your regular password

## Conclusion

Adding Google Sign-In authentication to HTB-Scraper provides users with an alternative authentication method. This is especially useful for users who prefer to use their Google accounts for authentication.

Remember that browser automation can be fragile and may break if Google changes their login page. Regular maintenance may be required to keep this feature working.
