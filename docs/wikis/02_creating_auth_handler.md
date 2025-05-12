# Creating the Authentication Handler

In this wiki, we'll create the core authentication handler that will manage credentials and authenticated sessions.

## What is the Authentication Handler?

The Authentication Handler is a class that will:

1. Store and manage user credentials
2. Create and maintain authenticated sessions
3. Handle secure storage of credentials using the system's keyring
4. Provide a consistent interface for different authentication methods

## Step 1: Create the auth_handler.py file

First, let's create a new file called `auth_handler.py` in the `src` directory:

```python
"""
Authentication handler for HTB-Scraper.
Manages credentials and authenticated sessions.
"""
import keyring
import getpass
import requests
from urllib.parse import urlparse

class AuthHandler:
    """
    Handles authentication for various websites.
    Manages credentials and maintains authenticated sessions.
    """
    
    # Service name for keyring
    KEYRING_SERVICE = "htb-scraper"
    
    def __init__(self, use_keyring=True):
        """
        Initialize the authentication handler.
        
        Args:
            use_keyring (bool): Whether to use the system keyring for credential storage
        """
        self.session = requests.Session()
        self.use_keyring = use_keyring
        self.username = None
        self.password = None
        
    def get_credentials(self, username=None, password=None, domain=None):
        """
        Get credentials from user input, arguments, or keyring.
        
        Args:
            username (str, optional): Username provided via arguments
            password (str, optional): Password provided via arguments
            domain (str, optional): Domain for which to retrieve credentials
            
        Returns:
            tuple: (username, password)
        """
        # Use provided credentials if available
        if username and password:
            self.username = username
            self.password = password
            return username, password
            
        # Use provided username and get password
        if username:
            self.username = username
            
            # Try to get password from keyring if enabled
            if self.use_keyring and domain:
                keyring_password = self.get_password_from_keyring(username, domain)
                if keyring_password:
                    self.password = keyring_password
                    return username, keyring_password
            
            # Prompt for password if not found in keyring
            password = self.prompt_for_password()
            self.password = password
            
            # Save to keyring if enabled
            if self.use_keyring and domain:
                self.save_to_keyring(username, password, domain)
                
            return username, password
            
        # No username provided, prompt for both
        username = input("Username: ")
        password = self.prompt_for_password()
        
        self.username = username
        self.password = password
        
        # Save to keyring if enabled
        if self.use_keyring and domain:
            self.save_to_keyring(username, password, domain)
            
        return username, password
    
    def prompt_for_password(self):
        """
        Securely prompt the user for a password.
        
        Returns:
            str: The password entered by the user
        """
        return getpass.getpass("Password: ")
    
    def get_password_from_keyring(self, username, domain):
        """
        Retrieve password from the system keyring.
        
        Args:
            username (str): The username
            domain (str): The domain for which to retrieve the password
            
        Returns:
            str or None: The password if found, None otherwise
        """
        keyring_id = f"{self.KEYRING_SERVICE}:{domain}"
        try:
            return keyring.get_password(keyring_id, username)
        except Exception:
            return None
    
    def save_to_keyring(self, username, password, domain):
        """
        Save credentials to the system keyring.
        
        Args:
            username (str): The username to save
            password (str): The password to save
            domain (str): The domain for which to save the credentials
        """
        keyring_id = f"{self.KEYRING_SERVICE}:{domain}"
        try:
            keyring.set_password(keyring_id, username, password)
            print(f"Credentials saved to keyring for {domain}")
        except Exception as e:
            print(f"Failed to save credentials to keyring: {str(e)}")
    
    def get_domain_from_url(self, url):
        """
        Extract the domain from a URL.
        
        Args:
            url (str): The URL
            
        Returns:
            str: The domain name
        """
        parsed_url = urlparse(url)
        return parsed_url.netloc
    
    def get_authenticated_session(self):
        """
        Get the authenticated session.
        
        Returns:
            requests.Session: The authenticated session
        """
        return self.session
```

## Step 2: Understanding the AuthHandler Class

Let's break down what this class does:

1. **Initialization**: Creates a new session and sets up keyring usage
2. **Credential Management**: Gets credentials from arguments, keyring, or user input
3. **Secure Password Input**: Uses `getpass` to hide password when typing
4. **Keyring Integration**: Saves and retrieves passwords securely
5. **Session Management**: Maintains an authenticated session for requests

## Step 3: Testing the AuthHandler

To make sure our AuthHandler works correctly, let's create a simple test script:

```python
# test_auth_handler.py
from src.auth_handler import AuthHandler

def test_auth_handler():
    # Create an auth handler without keyring (for testing)
    auth = AuthHandler(use_keyring=False)
    
    # Test getting domain from URL
    domain = auth.get_domain_from_url("https://academy.hackthebox.com/module/details/123")
    print(f"Domain: {domain}")
    
    # Test getting credentials (this will prompt for input)
    username, password = auth.get_credentials(username="test_user")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    
    # Get the session
    session = auth.get_authenticated_session()
    print(f"Session: {session}")

if __name__ == "__main__":
    test_auth_handler()
```

You can run this test script to make sure the basic functionality works.

## Next Steps

In the next wiki, we'll create a specialized authentication handler for HackTheBox Academy.
