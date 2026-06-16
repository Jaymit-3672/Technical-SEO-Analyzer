import requests
from bs4 import BeautifulSoup
from image_audit import audit_images


def analyze_website(website_url):

    response = requests.get(website_url, timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")

    image_results = audit_images(soup)

    title = soup.title.get_text(strip=True) if soup.title else "Missing Title"

    meta_tag = soup.find("meta", attrs={"name": "description"})

    meta_description = (
        meta_tag.get("content", "")
        if meta_tag
        else "Missing Meta Description"
    )

    h1_tag = soup.find("h1")

    h1 = h1_tag.get_text(strip=True) if h1_tag else "Missing H1"

    return {
        "title": title,
        "meta_description": meta_description,
        "h1": h1,
        "total_images": image_results["total_images"],
        "missing_alt": len(image_results["missing_alt_images"])
    }