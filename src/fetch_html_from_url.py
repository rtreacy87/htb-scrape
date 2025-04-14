def fetch_html_from_url(url):
    """
    Fetch HTML content from a URL
    """
    validate_url(url)
    headers = get_browser_headers()
    return make_http_request(url, headers)

def validate_url(url):
    """
    Validate that the URL is properly formatted
    """
    result = urlparse(url)
    if not all([result.scheme, result.netloc]):
        raise ValueError("Invalid URL. Please include http:// or https://")

def get_browser_headers():
    """
    Return headers that mimic a regular browser
    """
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

def make_http_request(url, headers):
    """
    Make the HTTP request and handle potential errors
    """
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching content: {str(e)}")

