import requests
import os
from urllib.parse import urlparse
import hashlib

def fetch_image(url, fetched_dir="Fetched_Images"):
    """
    Fetches an image from the given URL and saves it in fetched_dir.
    Applies error handling, filename generation, duplicate prevention,
    and safety checks for content type.
    """
    try:
        # Ensure directory exists
        os.makedirs(fetched_dir, exist_ok=True)

        # Send request with headers for safer communication
        headers = {"User-Agent": "UbuntuImageFetcher/1.0"}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()

        # Check for appropriate content type
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipping {url} (not an image, got {content_type})")
            return

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        if not filename:  # Fallback if URL ends with /
            filename = "downloaded_image.jpg"

        # Prevent duplicate downloads using file hash
        file_hash = hashlib.md5(response.content).hexdigest()
        filename = f"{file_hash}_{filename}"
        filepath = os.path.join(fetched_dir, filename)

        if os.path.exists(filepath):
            print(f"⚠ Duplicate detected. Skipping {filename}")
            return

        # Save file in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Saved to: {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ Unexpected error for {url}: {e}")


def main():
    print("🌍 Welcome to the Ubuntu Image Fetcher")
    print("I am because we are — Collecting and Sharing Images with Care\n")

    # Accept multiple URLs (comma-separated)
    urls = input("Enter one or more image URLs (comma separated): ").split(",")

    for url in urls:
        url = url.strip()
        if url:
            fetch_image(url)

    print("\n🤝 Connection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
