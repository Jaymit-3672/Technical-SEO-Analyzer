# ==========================================
# Technical SEO Analyzer
# Phase 3 - Basic SEO + Image Audit
# ==========================================

# Import required libraries
import requests
from bs4 import BeautifulSoup
from image_audit import audit_images

# ==========================================
# GET WEBSITE URL
# ==========================================

website_url = input("Enter Website URL: ")

print("\nDownloading website...")

# ==========================================
# DOWNLOAD WEBPAGE
# ==========================================

try:
    response = requests.get(website_url, timeout=10)

    print(f"\nStatus Code: {response.status_code}")

except Exception as error:
    print(f"\nError: {error}")
    exit()

# ==========================================
# PARSE HTML
# ==========================================

soup = BeautifulSoup(response.text, "html.parser")

# ==========================================
# RUN IMAGE AUDIT
# ==========================================

image_results = audit_images(soup)

# ==========================================
# TITLE TAG
# ==========================================

if soup.title:
    title = soup.title.get_text(strip=True)
else:
    title = "Missing Title"

# ==========================================
# META DESCRIPTION
# ==========================================

meta_tag = soup.find("meta", attrs={"name": "description"})

if meta_tag:
    meta_description = meta_tag.get("content", "")
else:
    meta_description = "Missing Meta Description"

# ==========================================
# H1 TAG
# ==========================================

h1_tag = soup.find("h1")

if h1_tag:
    h1 = h1_tag.get_text(strip=True)
else:
    h1 = "Missing H1"

# ==========================================
# SEO AUDIT REPORT
# ==========================================

print("\n")
print("=" * 60)
print("TECHNICAL SEO AUDIT REPORT")
print("=" * 60)

print("\nTITLE TAG")
print("-" * 60)
print(title)

print("\nMETA DESCRIPTION")
print("-" * 60)
print(meta_description)

print("\nH1 TAG")
print("-" * 60)
print(h1)

# ==========================================
# IMAGE SEO AUDIT
# ==========================================

print("\nIMAGE SEO AUDIT")
print("-" * 60)

print(f"Total Images Found: {image_results['total_images']}")

missing_count = len(image_results["missing_alt_images"])

print(f"Images Missing ALT Text: {missing_count}")

if missing_count > 0:

    print("\nImages Missing ALT:")

    for image in image_results["missing_alt_images"]:
        print(f"- {image}")

    print("\nRECOMMENDATION")
    print("-" * 60)
    print("Add descriptive ALT text to all images missing ALT attributes.")

else:

    print("\nExcellent! All images have ALT text.")

# ==========================================
# END REPORT
# ==========================================

print("\n")
print("=" * 60)
print("AUDIT COMPLETED")
print("=" * 60)