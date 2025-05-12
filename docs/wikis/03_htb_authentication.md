# HackTheBox-Specific Authentication

In this wiki, we'll create a specialized authentication handler for HackTheBox Academy. This will extend our base AuthHandler to handle the specific login process for HackTheBox.

## Understanding HackTheBox Authentication

HackTheBox Academy uses a form-based authentication system with CSRF (Cross-Site Request Forgery) protection. To log in, we need to:

1. Visit the login page
2. Extract the CSRF token from the page
3. Submit the login form with username, password, and CSRF token
4. Check if login was successful
5. Maintain the session cookies for subsequent requests

## Step 1: Create the htb_auth.py file

Let's create a new file called `htb_auth.py` in the `src` directory:

```python
"""
HackTheBox-specific authentication handler.
Extends the base AuthHandler to handle HackTheBox Academy login.
"""
import re
import requests
from bs4 import BeautifulSoup
from .auth_handler import AuthHandler

class HTBAuthHandler(AuthHandler):
    """
    Handles authentication for HackTheBox Academy.
    """
    
    # HackTheBox URLs
    HTB_BASE_URL = "https://academy.hackthebox.com"
    HTB_LOGIN_URL = "https://academy.hackthebox.com/login"
    HTB_DASHBOARD_URL = "https://academy.hackthebox.com/dashboard"
    
    def __init__(self, use_keyring=True):
        """
        Initialize the HackTheBox authentication handler.
        
        Args:
            use_keyring (bool): Whether to use the system keyring for credential storage
        """
        super().__init__(use_keyring)
        self.is_authenticated = False
    
    def authenticate(self, username=None, password=None):
        """
        Authenticate with HackTheBox Academy.
        
        Args:
            username (str, optional): Username provided via arguments
            password (str, optional): Password provided via arguments
            
        Returns:
            bool: True if authentication was successful, False otherwise
        """
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
    
    def _get_csrf_token(self):
        """
        Get the CSRF token from the login page.
        
        Returns:
            str or None: The CSRF token if found, None otherwise
        """
        try:
            # Visit the login page
            response = self.session.get(self.HTB_LOGIN_URL)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the CSRF token input field
            csrf_input = soup.find('input', {'name': '_token'})
            if csrf_input and 'value' in csrf_input.attrs:
                return csrf_input['value']
            
            # Alternative method: try to find it using regex
            match = re.search(r'name="_token"\s+value="([^"]+)"', response.text)
            if match:
                return match.group(1)
            
            return None
        except Exception as e:
            print(f"Error getting CSRF token: {str(e)}")
            return None
    
    def _perform_login(self, username, password, csrf_token):
        """
        Perform the login request.
        
        Args:
            username (str): The username
            password (str): The password
            csrf_token (str): The CSRF token
            
        Returns:
            bool: True if login was successful, False otherwise
        """
        try:
            # Prepare login data
            login_data = {
                '_token': csrf_token,
                'email': username,
                'password': password,
                'remember': 'on'  # Stay logged in
            }
            
            # Set headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': self.HTB_LOGIN_URL,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Submit the login form
            response = self.session.post(
                self.HTB_LOGIN_URL,
                data=login_data,
                headers=headers,
                allow_redirects=True
            )
            
            # Check if login was successful
            # Usually, a successful login redirects to the dashboard
            if response.url == self.HTB_DASHBOARD_URL:
                return True
            
            # Alternative check: look for specific elements on the page
            if "Invalid credentials" in response.text:
                return False
            
            # Check if we can access a protected page
            dashboard_response = self.session.get(self.HTB_DASHBOARD_URL)
            return dashboard_response.status_code == 200 and "Login" not in dashboard_response.text
            
        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False
    
    def is_authenticated_session(self):
        """
        Check if the session is authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        return self.is_authenticated
```

## Step 2: Understanding the HTBAuthHandler Class

Let's break down what this class does:

1. **Extends AuthHandler**: Inherits all the base functionality
2. **HackTheBox-Specific URLs**: Contains the URLs needed for authentication
3. **CSRF Token Extraction**: Gets the security token from the login page
4. **Login Process**: Submits the login form with credentials and token
5. **Authentication Check**: Verifies if login was successful

## Step 3: Testing the HTBAuthHandler

To make sure our HTBAuthHandler works correctly, let's create a simple test script:

```python
# test_htb_auth.py
from src.htb_auth import HTBAuthHandler

def test_htb_auth():
    # Create an HTB auth handler
    auth = HTBAuthHandler(use_keyring=False)
    
    # Authenticate (this will prompt for credentials)
    success = auth.authenticate()
    
    if success:
        print("Authentication successful!")
        
        # Get the authenticated session
        session = auth.get_authenticated_session()
        
        # Try to access a protected page
        response = session.get("https://academy.hackthebox.com/dashboard")
        print(f"Dashboard access: {response.status_code == 200}")
    else:
        print("Authentication failed.")

if __name__ == "__main__":
    test_htb_auth()
```

You can run this test script to make sure the HackTheBox authentication works.

## Next Steps

In the next wiki, we'll update the URL fetcher to use our authentication system.
