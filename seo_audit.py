import requests
from bs4 import BeautifulSoup
from image_audit import audit_images


def analyze_website(website_url):

    # Download webpage
    response = requests.get(
        website_url,
        timeout=10
    )

    # Parse HTML
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Run image audit
    image_results = audit_images(soup)

    # ==========================================
    # SITEMAP CHECKER
    # ==========================================

    sitemap_url = (
        website_url.rstrip("/")
        + "/sitemap.xml"
    )

    try:

        sitemap_response = requests.get(
            sitemap_url,
            timeout=5
        )

        sitemap_found = (
            sitemap_response.status_code == 200
        )

    except:

        sitemap_found = False

    # ==========================================
    # ROBOTS.TXT CHECKER
    # ==========================================

    robots_url = (
        website_url.rstrip("/")
        + "/robots.txt"
    )

    try:

        robots_response = requests.get(
            robots_url,
            timeout=5
        )

        robots_found = (
            robots_response.status_code == 200
        )

    except:

        robots_found = False

    # ==========================================
    # TITLE CHECK
    # ==========================================

    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else "Missing Title"
    )

    # ==========================================
    # META DESCRIPTION CHECK
    # ==========================================

    meta_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    meta_description = (
        meta_tag.get("content", "")
        if meta_tag
        else "Missing Meta Description"
    )

    # ==========================================
    # H1 CHECK
    # ==========================================

    h1_tag = soup.find("h1")

    h1 = (
        h1_tag.get_text(strip=True)
        if h1_tag
        else "Missing H1"
    )

    # ==========================================
    # SEO SCORE
    # ==========================================

    score = 100

    # Missing title
    if title == "Missing Title":
        score -= 25

    # Missing meta description
    if meta_description == "Missing Meta Description":
        score -= 25

    # Missing H1
    if h1 == "Missing H1":
        score -= 20

    # Missing ALT text
    if image_results["total_images"] > 0:

        missing_alt_count = len(
            image_results["missing_alt_images"]
        )

        alt_penalty = min(
            missing_alt_count * 5,
            30
        )

        score -= alt_penalty

    # Bonus deductions

    if not sitemap_found:
        score -= 10

    if not robots_found:
        score -= 10

    # Prevent negative score

    score = max(score, 0)

    # Send results to HTML

    return {

        "title": title,

        "meta_description": meta_description,

        "h1": h1,

        "total_images":
            image_results["total_images"],

        "missing_alt":
            len(
                image_results[
                    "missing_alt_images"
                ]
            ),

        "seo_score": score,

        "sitemap_found": sitemap_found,

        "robots_found": robots_found
    }