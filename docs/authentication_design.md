# Authentication Support for HTB-Scrape

## Introduction

This document outlines how we plan to add authentication capabilities to the HTB-Scrape tool. In simple terms, we want to enable the tool to log into password-protected websites (specifically HackTheBox Academy) to extract content directly, rather than requiring users to manually download HTML files first.

## What is Authentication?

Authentication is the process of verifying who you are when accessing a website. When you visit a site like HackTheBox Academy, you need to provide your username and password to access the content. Our tool currently can't do this automatically - we're going to fix that.

## Why Do We Need This?

Currently, if you want to extract content from a password-protected page on HackTheBox Academy, you need to:
1. Log in manually using your browser
2. Save the HTML page to your computer
3. Run HTB-Scrape on the saved file

This is cumbersome and time-consuming. With authentication support, you'll be able to:
1. Run HTB-Scrape with your credentials
2. The tool will log in for you and extract the content in one step

## How Will It Work?

### For Users (Non-Technical Explanation)

When you run the tool, you'll have new options:

```bash
# This will ask for your username and password
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth
```

The tool will:
1. Ask for your username and password (if not provided)
2. Securely log in to the website
3. Download the content
4. Process it just like it does now

Your password will be handled securely - it won't be shown on screen when you type it, and you can choose to save it securely on your computer so you don't have to type it every time.

### For Developers (Technical Details)

We'll create a new module called `auth_handler.py` that will:
1. Manage authentication credentials
2. Handle the login process for different websites
3. Maintain authenticated sessions
4. Securely store credentials using the system's keyring

The existing code will be updated to use this new authentication system when requested.

## Security Considerations

We take security seriously, especially when handling passwords:

1. **No Plain Text Passwords**: Passwords won't be stored in plain text
2. **Secure Input**: When typing your password, it won't be visible on screen
3. **Secure Storage**: We'll use your system's secure credential storage (keyring)
4. **No Command Line Passwords**: We discourage putting passwords directly in command line arguments (which could be seen in command history)

## Components We'll Build

### 1. Authentication Handler

This component will:
- Accept username and password
- Log in to websites (with special handling for HackTheBox)
- Remember your login session
- Securely store credentials if you choose to save them

### 2. Updated URL Fetcher

We'll update the existing code that downloads web pages to:
- Check if authentication is needed
- Use the Authentication Handler when needed
- Handle both authenticated and non-authenticated requests

### 3. Command Line Interface Updates

We'll add new options to the command line:
- `--auth` to enable authentication
- `--username` to specify your username
- `--password` (not recommended, but available)
- `--no-keyring` if you don't want to save credentials

### 4. Secure Credential Storage

We'll use a system called "keyring" that:
- Stores passwords securely in your operating system's password manager
- On Windows, this uses Windows Credential Manager
- On macOS, this uses Keychain
- On Linux, this uses services like Secret Service or KWallet

## How to Use It (Examples)

### Basic Usage

```bash
# This will prompt for username and password
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth
```

### Providing Username (Password Will Be Prompted)

```bash
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --username your.email@example.com
```

### Without Saving Credentials

```bash
python htb_scraper.py --url https://academy.hackthebox.com/module/details/123 --auth --no-keyring
```

## What Happens Behind the Scenes?

When you run the tool with authentication:

1. The tool checks if you've provided a username and password
2. If not, it asks you to type them in
3. It then creates a "session" (like a browser session)
4. For HackTheBox specifically, it:
   - Visits the login page
   - Finds the security token on the page (to prevent fake logins)
   - Submits your username and password with this token
   - Checks if login was successful
5. If login works, it keeps this session active
6. It then visits the page you requested
7. Downloads the content using your logged-in session
8. Processes the content as usual

## Technical Implementation Details

For those interested in the code, we'll create:

1. A new `AuthHandler` class that manages the authentication process
2. Updates to `fetch_html_from_url.py` to support authenticated sessions
3. Updates to the argument parser to accept authentication options
4. Integration with the system keyring for secure credential storage

## Future Improvements

After this initial implementation, we could add:

1. Support for other types of authentication (like OAuth)
2. Ability to import cookies from your browser
3. Support for two-factor authentication
4. Support for proxy servers

## Conclusion

This authentication feature will make HTB-Scrape much more convenient for users who want to extract content directly from HackTheBox Academy without manually downloading pages first. It will handle credentials securely and provide a smooth user experience.