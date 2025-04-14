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

        # Get the filename from the path
        filename = os.path.basename(image_url)

        # Full path to save the image
        save_path = os.path.join(output_dir, filename)

        # Check if this is a local file path
        if image_url.startswith('./') or image_url.startswith('../') or '/' in image_url or '\\' in image_url:
            # This might be a local file path - try several possible locations
            possible_paths = [
                image_url,  # Direct path
                os.path.join(os.getcwd(), image_url),  # Relative to current directory
                os.path.join(os.path.dirname(os.getcwd()), image_url),  # Relative to parent directory
            ]

            # If we have a file path for the HTML file, try relative to that
            if base_url and os.path.isfile(base_url):
                html_dir = os.path.dirname(os.path.abspath(base_url))
                possible_paths.append(os.path.join(html_dir, image_url))

            # Try each possible path
            for path in possible_paths:
                print(f"Trying path: {path}")
                if os.path.exists(path) and os.path.isfile(path):
                    shutil.copy2(path, save_path)
                    print(f"Copied local image: {filename} from {path}")
                    return save_path

            # If we get here, we couldn't find the file
            print(f"Local image not found in any of the tried paths: {image_url}")

        # Handle relative URLs
        if base_url and not urlparse(image_url).netloc:
            image_url = urllib.parse.urljoin(base_url, image_url)

        # Get the filename from the URL
        filename = os.path.basename(urlparse(image_url).path)

        # Clean the filename (remove query parameters, etc.)
        filename = re.sub(r'\?.*$', '', filename)

        # If filename is empty or invalid, generate a random one
        if not filename or len(filename) < 3:
            import uuid
            extension = guess_extension(image_url)
            filename = f"image_{uuid.uuid4().hex[:8]}{extension}"

        # Full path to save the image
        save_path = os.path.join(output_dir, filename)

        # Download the image
        response = requests.get(image_url, stream=True, timeout=10)
        response.raise_for_status()

        # Save the image to disk
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded image: {filename}")
        return save_path

    except Exception as e:
        print(f"Error handling image {image_url}: {str(e)}")
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
