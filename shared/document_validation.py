import re

def extract_doc_id_from_url(url):
    match = re.search(r"/document/d/([a-zA-Z0-9-_]+)", url)
    if not match:
        raise ValueError("Invalid Google Docs URL")
    return match.group(1)

def extract_google_doc_url(msg):
    match = re.search(r'https://docs\.google\.com/document/d/[a-zA-Z0-9-_]+', msg)
    return match.group(0) if match else None

def extract_any_url(msg):
    match = re.search(r'https?://[^\s]+', msg)
    return match.group(0) if match else None

def is_valid_google_doc(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
