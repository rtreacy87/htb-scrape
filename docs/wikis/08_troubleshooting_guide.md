# Troubleshooting Guide

In this wiki, we'll provide solutions to common issues you might encounter when implementing or using the authentication features in HTB-Scraper.

## Installation Issues

### Missing Dependencies

**Problem**: You get an error about missing modules when running the script.

**Solution**: Make sure you've installed all required dependencies:

```bash
pip install requests beautifulsoup4 keyring getpass
```

### Keyring Issues

**Problem**: You get errors related to the keyring module.

**Solution**: Some systems might need additional setup for keyring:

- **Windows**: No additional setup needed
- **macOS**: No additional setup needed
- **Linux**: You might need to install a backend:

```bash
# For GNOME/Ubuntu
sudo apt-get install python3-keyring gnome-keyring

# For KDE
sudo apt-get install python3-keyring kwalletmanager
```

If you continue to have issues, you can disable keyring with the `--no-keyring` option.

## Authentication Issues

### Login Failures

**Problem**: The script says "Login failed" even with correct credentials.

**Solution**:

1. Double-check your username and password
2. Try logging in manually in your browser to confirm your credentials work
3. Check if the website has changed its login page structure
4. Look for CAPTCHA or other anti-bot measures

If the website has changed, you might need to update the `_get_csrf_token` and `_perform_login` methods in `htb_auth.py`.

### CSRF Token Not Found

**Problem**: The script says "Failed to get CSRF token".

**Solution**:

1. Check if the website has changed its login page structure
2. Try updating the CSRF token extraction logic:

```python
def _get_csrf_token(self):
    """Get the CSRF token from the login page."""
    try:
        # Visit the login page
        response = self.session.get(self.HTB_LOGIN_URL)
        response.raise_for_status()
        
        # Save the HTML for debugging
        with open("login_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        # Try different methods to find the token
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Method 1: Look for input with name="_token"
        csrf_input = soup.find('input', {'name': '_token'})
        if csrf_input and 'value' in csrf_input.attrs:
            return csrf_input['value']
        
        # Method 2: Look for meta tag with name="csrf-token"
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        if csrf_meta and 'content' in csrf_meta.attrs:
            return csrf_meta['content']
        
        # Method 3: Try to find it using regex
        match = re.search(r'name="_token"\s+value="([^"]+)"', response.text)
        if match:
            return match.group(1)
        
        # Method 4: Look for it in a script tag
        match = re.search(r'csrfToken["\']?\s*:\s*["\']([^"\']+)["\']', response.text)
        if match:
            return match.group(1)
        
        print("Could not find CSRF token. Check login_page.html for debugging.")
        return None
    except Exception as e:
        print(f"Error getting CSRF token: {str(e)}")
        return None
```

### Session Not Maintained

**Problem**: The script authenticates successfully but then loses the session.

**Solution**:

1. Make sure you're using the same session object for all requests
2. Check if the website uses cookies for session management
3. Try adding code to print and check cookies:

```python
def _perform_login(self, username, password, csrf_token):
    """Perform the login request."""
    # Existing code...
    
    # Print cookies after login
    print("Cookies after login:")
    for cookie in self.session.cookies:
        print(f"  {cookie.name}: {cookie.value}")
    
    # Existing code...
```

## URL Fetching Issues

### Connection Errors

**Problem**: You get connection errors when trying to fetch URLs.

**Solution**:

1. Check your internet connection
2. Make sure the URL is correct
3. Check if the website is blocking automated requests
4. Try adding a delay between requests:

```python
def fetch_with_auth(url, username=None, password=None, use_keyring=True):
    """Fetch HTML content using authentication."""
    # Existing code...
    
    # Add a delay before making the request
    import time
    time.sleep(2)  # 2-second delay
    
    # Make the request
    # Existing code...
```

### Content Not Found

**Problem**: The script fetches the page but doesn't find the expected content.

**Solution**:

1. Check if you're logged in correctly
2. Save the fetched HTML for inspection:

```python
def fetch_with_auth(url, username=None, password=None, use_keyring=True):
    """Fetch HTML content using authentication."""
    # Existing code...
    
    try:
        headers = get_browser_headers()
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Save the HTML for inspection
        with open("fetched_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching content: {str(e)}")
```

## Command-Line Issues

### Arguments Not Recognized

**Problem**: Command-line arguments are not being recognized.

**Solution**:

1. Make sure you're using the correct argument format
2. Check for typos in argument names
3. Try using the long-form arguments (e.g., `--auth` instead of `-a`)
4. Print the parsed arguments for debugging:

```python
def main():
    """Main function to coordinate the content extraction process."""
    args = su.parse_arguments()
    
    # Print all arguments for debugging
    print("Parsed arguments:")
    for arg, value in vars(args).items():
        print(f"  {arg}: {value}")
    
    # Existing code...
```

### Password Prompt Issues

**Problem**: The password prompt doesn't work correctly.

**Solution**:

1. Make sure you're running the script in an interactive terminal
2. If you're running the script in a non-interactive environment, provide the username and password through environment variables:

```python
def get_credentials(self, username=None, password=None, domain=None):
    """Get credentials from user input, arguments, or keyring."""
    # Try to get credentials from environment variables
    import os
    env_username = os.environ.get('HTB_USERNAME')
    env_password = os.environ.get('HTB_PASSWORD')
    
    if env_username and env_password:
        return env_username, env_password
    
    # Existing code...
```

## Keyring Issues

### Keyring Not Saving Credentials

**Problem**: Credentials are not being saved to the keyring.

**Solution**:

1. Make sure you're not using the `--no-keyring` option
2. Check if your system's keyring service is running
3. Try a simpler keyring implementation:

```python
def save_to_keyring(self, username, password, domain):
    """Save credentials to the system keyring."""
    keyring_id = f"{self.KEYRING_SERVICE}:{domain}"
    try:
        keyring.set_password(keyring_id, username, password)
        print(f"Credentials saved to keyring for {domain}")
    except Exception as e:
        print(f"Failed to save credentials to keyring: {str(e)}")
        
        # Try a simpler approach
        try:
            keyring.set_password(domain, username, password)
            print(f"Credentials saved to keyring using simpler approach")
        except Exception as e2:
            print(f"Still failed to save credentials: {str(e2)}")
```

### Keyring Not Retrieving Credentials

**Problem**: Credentials are not being retrieved from the keyring.

**Solution**:

1. Make sure you've saved credentials previously
2. Try manually checking if credentials exist:

```python
def get_password_from_keyring(self, username, domain):
    """Retrieve password from the system keyring."""
    keyring_id = f"{self.KEYRING_SERVICE}:{domain}"
    try:
        password = keyring.get_password(keyring_id, username)
        if password:
            print(f"Found credentials in keyring for {username} at {domain}")
        else:
            print(f"No credentials found in keyring for {username} at {domain}")
        return password
    except Exception as e:
        print(f"Error retrieving from keyring: {str(e)}")
        return None
```

## Conclusion

This troubleshooting guide covers the most common issues you might encounter when implementing or using the authentication features in HTB-Scraper. If you encounter an issue not covered here, try:

1. Adding print statements to debug the problem
2. Checking the website's structure to see if it has changed
3. Looking for error messages in the console output
4. Saving intermediate HTML files for inspection

Remember that websites can change their structure and authentication methods over time, so you might need to update the code periodically to keep it working.
