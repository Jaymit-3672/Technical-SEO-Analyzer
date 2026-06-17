import requests
from bs4 import BeautifulSoup
from image_audit import audit_images


def analyze_website(website_url):

    response = requests.get(website_url, timeout=10) #downloads the webpage.

    soup = BeautifulSoup(response.text, "html.parser") #BeautifulSoup parses the HTML so we can search inside it.

    image_results = audit_images(soup)

    title = soup.title.get_text(strip=True) if soup.title else "Missing Title" #soup.title gets the page title.

    meta_tag = soup.find("meta", attrs={"name": "description"}) #finds the meta description tag.

    meta_description = (
        meta_tag.get("content", "")
        if meta_tag
        else "Missing Meta Description"
    )

    h1_tag = soup.find("h1") # finds the first H1 heading

    h1 = h1_tag.get_text(strip=True) if h1_tag else "Missing H1"

    return {
        "title": title,
        "meta_description": meta_description,
        "h1": h1,
        "total_images": image_results["total_images"],
        "missing_alt": len(image_results["missing_alt_images"])
    }
    #The function returns a dictionary because Flask can easily send it to the template.
