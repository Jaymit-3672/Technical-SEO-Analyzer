# ==========================================
# IMPORT LIBRARIES
# ==========================================

from flask import (
    Flask,
    render_template,
    request,
    send_file
)

from seo_audit import analyze_website
from report_generator import generate_pdf

# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)

# Store latest SEO results
latest_results = None

# ==========================================
# HOME PAGE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    global latest_results

    results = None

    if request.method == "POST":

        # Get URL from input box
        url = request.form["url"]

        # Run SEO audit
        results = analyze_website(url)

        # Save results for PDF export
        latest_results = results

    return render_template(
        "index.html",
        results=results
    )

# ==========================================
# DOWNLOAD PDF REPORT
# ==========================================

@app.route("/download-report")
def download_report():

    global latest_results

    if latest_results is None:

        return "Please analyze a website first."

    pdf_file = generate_pdf(
        latest_results
    )

    return send_file(
        pdf_file,
        as_attachment=True
    )

# ==========================================
# RUN FLASK SERVER
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)