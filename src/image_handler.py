import os
import requests
import urllib.parse
from urllib.parse import urlparse
import re
import shutil

def download_image(image_url, base_url=None, output_dir='images'):
    """
    Download an image from a URL and save it to the specified directory.
    Args:
        image_url (str): URL of the image to download
        base_url (str, optional): Base URL to resolve relative URLs
        output_dir (str): Directory to save images to
    Returns:
        str: Path to the saved image file, or None if download failed
    """
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Try to handle as a local file first
        local_path = handle_local_file(image_url, base_url, output_dir)
        if local_path:
            return local_path

        # Handle as a remote URL
        resolved_url = resolve_url(image_url, base_url)
        filename = generate_filename(resolved_url)
        save_path = os.path.join(output_dir, filename)

        return download_from_url(resolved_url, save_path, filename)

    except Exception as e:
        print(f"Error handling image {image_url}: {str(e)}")
        return None

def handle_local_file(image_url, base_url, output_dir):
    """
    Handle local file paths and copy the file to the output directory.
    Args:
        image_url (str): URL or path of the image
        base_url (str, optional): Base URL or path of the HTML file
        output_dir (str): Directory to save images to
    Returns:
        str: Path to the saved image file, or None if not found
    """
    # Check if this looks like a local file path
    if not (image_url.startswith('./') or image_url.startswith('../') or '/' in image_url or '\\' in image_url):
        return None

    # Get the filename from the path
    filename = os.path.basename(image_url)
    save_path = os.path.join(output_dir, filename)

    # Try several possible locations
    possible_paths = generate_possible_paths(image_url, base_url)

    # Try each possible path
    for path in possible_paths:
        print(f"Trying path: {path}")
        if os.path.exists(path) and os.path.isfile(path):
            shutil.copy2(path, save_path)
            print(f"Copied local image: {filename} from {path}")
            return save_path

    # If we get here, we couldn't find the file
    print(f"Local image not found in any of the tried paths: {image_url}")
    return None

def generate_possible_paths(image_url, base_url):
    """
    Generate a list of possible file paths to try.
    Args:
        image_url (str): URL or path of the image
        base_url (str, optional): Base URL or path of the HTML file
    Returns:
        list: List of possible file paths
    """
    possible_paths = [
        image_url,  # Direct path
        os.path.join(os.getcwd(), image_url),  # Relative to current directory
        os.path.join(os.path.dirname(os.getcwd()), image_url),  # Relative to parent directory
    ]

    # If we have a file path for the HTML file, try relative to that
    if base_url and os.path.isfile(base_url):
        html_dir = os.path.dirname(os.path.abspath(base_url))
        possible_paths.append(os.path.join(html_dir, image_url))

    return possible_paths

def resolve_url(image_url, base_url):
    """
    Resolve a relative URL against a base URL.
    Args:
        image_url (str): URL of the image
        base_url (str, optional): Base URL to resolve against
    Returns:
        str: Resolved URL
    """
    # Handle relative URLs
    if base_url and not urlparse(image_url).netloc:
        return urllib.parse.urljoin(base_url, image_url)
    return image_url

def generate_filename(url):
    """
    Generate a filename from a URL.
    Args:
        url (str): URL of the image
    Returns:
        str: Generated filename
    """
    # Get the filename from the URL
    filename = os.path.basename(urlparse(url).path)

    # Clean the filename (remove query parameters, etc.)
    filename = re.sub(r'\?.*$', '', filename)

    # If filename is empty or invalid, generate a random one
    if not filename or len(filename) < 3:
        import uuid
        extension = guess_extension(url)
        filename = f"image_{uuid.uuid4().hex[:8]}{extension}"

    return filename

def download_from_url(url, save_path, filename):
    """
    Download an image from a URL and save it to the specified path.
    Args:
        url (str): URL of the image
        save_path (str): Path to save the image to
        filename (str): Filename for logging purposes
    Returns:
        str: Path to the saved image file, or None if download failed
    """
    try:
        # Download the image
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        # Save the image to disk
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded image: {filename}")
        return save_path

    except Exception as e:
        print(f"Error downloading image {url}: {str(e)}")
        return None

def guess_extension(url):
    """
    Guess the file extension from the URL or content type
    """
    # Try to get extension from URL
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]
    if ext:
        return ext

    # Default to .jpg if we can't determine the extension
    return '.jpg'

def process_image_element(element, base_url=None, download=True, output_dir='images'):
    """
    Process an image element from HTML.
    Args:
        element: BeautifulSoup image element
        base_url (str, optional): Base URL to resolve relative URLs
        download (bool): Whether to download the image
        output_dir (str): Directory to save images to
    Returns:
        dict: Processed image data
    """
    src = element.get('src', '')
    alt = element.get('alt', '')

    print(f"Processing image: src='{src}', alt='{alt}'")

    local_path = None
    if download and src:
        print(f"Attempting to download/copy image: {src}")
        local_path = download_image(src, base_url, output_dir)
        if local_path:
            print(f"Successfully saved image to: {local_path}")
        else:
            print(f"Failed to save image: {src}")

    return {
        "type": "image",
        "src": src,
        "alt": alt if alt else "Image",
        "local_path": local_path
    }
