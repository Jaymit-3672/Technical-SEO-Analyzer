#Flask creates the web server 
from flask import Flask, render_template, request
from seo_audit import analyze_website

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"]) #That "@app.route" Line means " Open the function when user visit the home page " and " get post " method line means the page can be opened and also receive data
def home():

    results = None

    if request.method == "POST":

        url = request.form["url"] #reads the text typed into the input box.

        results = analyze_website(url)

    return render_template( #sends data to the HTML page.
        "index.html",
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)
