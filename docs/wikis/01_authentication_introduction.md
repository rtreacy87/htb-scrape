# Authentication in HTB-Scraper: Introduction

## What is this wiki series?

This series of wiki pages will guide you through implementing authentication features for the HTB-Scraper tool. By the end, you'll be able to add functionality that allows users to log into password-protected websites (specifically HackTheBox Academy) to extract content directly.

## Who is this for?

These guides are designed for developers with minimal experience. We'll explain each step clearly and provide code examples that you can follow along with.

## What will we build?

We'll be adding the following features to HTB-Scraper:

1. Command-line options for authentication
2. A secure way to handle usernames and passwords
3. A system to log into HackTheBox Academy
4. An updated URL fetcher that works with authenticated sessions
5. Secure credential storage using the system's keyring

## Why do we need authentication?

Currently, HTB-Scraper can only process HTML files that are already downloaded. If a user wants to extract content from a password-protected page, they need to:

1. Log in manually using their browser
2. Save the HTML page to their computer
3. Run HTB-Scraper on the saved file

With authentication support, users will be able to:

1. Run HTB-Scraper with their credentials
2. The tool will log in for them and extract the content in one step

## Prerequisites

Before starting this implementation, make sure you have:

1. Python 3.6 or higher installed
2. Basic understanding of Python programming
3. The HTB-Scraper codebase cloned to your local machine
4. The following Python packages installed:
   - `requests` (for making HTTP requests)
   - `keyring` (for secure credential storage)
   - `getpass` (for secure password input)

You can install these packages using pip:

```bash
pip install requests keyring getpass
```

## Overview of the implementation

We'll be creating the following new files:

1. `src/auth_handler.py` - The main authentication module
2. `src/htb_auth.py` - HackTheBox-specific authentication logic

And we'll be updating these existing files:

1. `htb_scraper.py` - To integrate authentication into the main flow
2. `src/htb_scraper_utils.py` - To add authentication-related command-line arguments
3. `src/fetch_html_from_url.py` - To support authenticated requests

## Next steps

Continue to the next wiki page to start implementing the authentication handler.
