# ==========================================
# IMAGE SEO AUDIT FUNCTION
# ==========================================

def audit_images(soup):

    # Find all images
    images = soup.find_all("img")

    total_images = len(images)

    missing_alt_images = []

    # Loop through all images
    for image in images:

        alt_text = image.get("alt")

        # Check if alt is missing or empty
        if not alt_text or alt_text.strip() == "":

            image_url = image.get("src", "No Source Found")

            missing_alt_images.append(image_url)

    # Return results
    return {
        "total_images": total_images,
        "missing_alt_images": missing_alt_images
    }