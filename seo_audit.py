# ==========================================
# IMPORT LIBRARIES
# ==========================================

import requests
import time

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from image_audit import audit_images


# ==========================================
# MAIN SEO ANALYZER FUNCTION
# ==========================================

def analyze_website(website_url):

    # ==========================================
    # START TIMER
    # ==========================================

    start_time = time.time()

    # ==========================================
    # DOWNLOAD WEBSITE HTML
    # ==========================================

    response = requests.get(
        website_url,
        timeout=10
    )

    # Convert HTML into searchable object

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # ==========================================
    # IMAGE AUDIT
    # ==========================================

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
    # TITLE TAG CHECK
    # ==========================================

    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else "Missing Title"
    )

    title_length = (
        len(title)
        if title != "Missing Title"
        else 0
    )

    # ==========================================
    # META DESCRIPTION CHECK
    # ==========================================

    meta_tag = soup.find(
        "meta",
        attrs={
            "name": "description"
        }
    )

    meta_description = (
        meta_tag.get("content")
        if meta_tag
        else "Missing Meta Description"
    )

    meta_length = (
        len(meta_description)
        if meta_description != "Missing Meta Description"
        else 0
    )

    # ==========================================
    # CANONICAL TAG CHECK
    # ==========================================

    canonical_tag = soup.find(
        "link",
        rel="canonical"
    )

    canonical_found = (
        canonical_tag is not None
    )

    canonical_url = (
        canonical_tag.get("href")
        if canonical_tag
        else "Not Found"
    )

    # ==========================================
    # HEADING AUDIT
    # ==========================================

    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")
    h3_tags = soup.find_all("h3")
    h4_tags = soup.find_all("h4")
    h5_tags = soup.find_all("h5")
    h6_tags = soup.find_all("h6")

    h1_count = len(h1_tags)
    h2_count = len(h2_tags)
    h3_count = len(h3_tags)
    h4_count = len(h4_tags)
    h5_count = len(h5_tags)
    h6_count = len(h6_tags)

    total_headings = (
        h1_count +
        h2_count +
        h3_count +
        h4_count +
        h5_count +
        h6_count
    )

    h1 = (
        h1_tags[0].get_text(strip=True)
        if h1_count > 0
        else "Missing H1"
    )

    # ==========================================
    # LINKS AUDIT
    # ==========================================

    links = soup.find_all(
        "a",
        href=True
    )

    total_links = len(links)

    internal_links = 0
    external_links = 0

    link_details = []

    base_domain = urlparse(
        website_url
    ).netloc

    seen_links = set()

    for link in links:

        href = link.get("href")

        anchor_text = link.get_text(
            strip=True
        )

        if not href:
            continue

        # Remove duplicates

        if href in seen_links:
            continue

        seen_links.add(href)

        # Internal / External Detection

        if href.startswith("http"):

            link_domain = urlparse(
                href
            ).netloc

            if base_domain in link_domain:

                internal_links += 1
                link_type = "Internal"

            else:

                external_links += 1
                link_type = "External"

        else:

            internal_links += 1
            link_type = "Internal"

        link_details.append({

            "url": href,
            "text": anchor_text,
            "type": link_type

        })

    unique_links = len(link_details)

    # ==========================================
    # SCHEMA DETECTION
    # ==========================================

    schema_types = []

    json_ld_scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    possible_schemas = [

        "Organization",
        "LocalBusiness",
        "Product",
        "Article",
        "FAQPage",
        "BreadcrumbList",
        "WebSite"

    ]

    for script in json_ld_scripts:

        content = str(script)

        for schema in possible_schemas:

            if schema in content:

                schema_types.append(
                    schema
                )

    schema_types = list(
        set(schema_types)
    )

    # ==========================================
    # SEO SCORE
    # ==========================================

    score = 100

    if title == "Missing Title":
        score -= 25

    if meta_description == "Missing Meta Description":
        score -= 25

    if h1 == "Missing H1":
        score -= 20

    if image_results["total_images"] > 0:

        missing_alt_count = len(
            image_results[
                "missing_alt_images"
            ]
        )

        alt_penalty = min(
            missing_alt_count * 5,
            30
        )

        score -= alt_penalty

    if not sitemap_found:
        score -= 10

    if not robots_found:
        score -= 10

    if not canonical_found:
        score -= 5

    score = max(score, 0)

    # ==========================================
    # ANALYSIS TIME
    # ==========================================

    analysis_time = round(

        time.time() - start_time,

        2

    )

    # ==========================================
    # RETURN RESULTS TO FLASK
    # ==========================================

    return {

        # Score

        "seo_score": score,

        # Timing

        "analysis_time": analysis_time,

        # Title

        "title": title,
        "title_length": title_length,

        # Meta

        "meta_description": meta_description,
        "meta_length": meta_length,

        # Headings

        "h1": h1,

        "h1_count": h1_count,
        "h2_count": h2_count,
        "h3_count": h3_count,
        "h4_count": h4_count,
        "h5_count": h5_count,
        "h6_count": h6_count,

        "total_headings": total_headings,

        # Images

        "total_images":
            image_results["total_images"],

        "missing_alt":
            len(
                image_results[
                    "missing_alt_images"
                ]
            ),

        # Technical SEO

        "sitemap_found": sitemap_found,
        "sitemap_url": sitemap_url,

        "robots_found": robots_found,
        "robots_url": robots_url,

        "canonical_found": canonical_found,
        "canonical_url": canonical_url,

        # Links

        "total_links": total_links,

        "internal_links": internal_links,

        "external_links": external_links,

        "unique_links": unique_links,

        "link_details":
            link_details[:20],

        # Schema

        "schema_types": schema_types

    }