import requests
from bs4 import BeautifulSoup
from image_audit import audit_images


def analyze_website(website_url):

    # Download the webpage HTML
    response = requests.get(website_url, timeout=10)

    # Convert HTML into searchable Python object
    soup = BeautifulSoup(response.text, "html.parser")

    # Run image audit and get image statistics
    image_results = audit_images(soup)

    # Get page title
    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else "Missing Title"
    )

    # Find meta description tag
    meta_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    # Extract description content
    meta_description = (
        meta_tag.get("content", "")
        if meta_tag
        else "Missing Meta Description"
    )

    # Find first H1 tag
    h1_tag = soup.find("h1")

    # Extract H1 text
    h1 = (
        h1_tag.get_text(strip=True)
        if h1_tag
        else "Missing H1"
    )

    # -------------------------
    # SEO SCORE CALCULATION
    # -------------------------

    # Start from 100 points
    score = 100

    # Missing title = major SEO issue
    if title == "Missing Title":
        score -= 25

    # Missing meta description
    if meta_description == "Missing Meta Description":
        score -= 25

    # Missing H1 heading
    if h1 == "Missing H1":
        score -= 20

    # Penalize images without ALT text
    if image_results["total_images"] > 0:

        missing_alt_count = len(
            image_results["missing_alt_images"]
        )

        # 5 points deduction per image
        # Maximum deduction = 30
        alt_penalty = min(
            missing_alt_count * 5,
            30
        )

        score -= alt_penalty

    # Never allow negative score
    score = max(score, 0)

    return {
        "title": title,
        "meta_description": meta_description,
        "h1": h1,
        "total_images": image_results["total_images"],
        "missing_alt": len(
            image_results["missing_alt_images"]
        ),

        # Send SEO score to HTML page
        "seo_score": score
    }