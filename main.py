from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Servidor Flask activo 🔥"

@app.route("/fiverr/search", methods=["POST"])
def buscar_gigs():
    data = request.get_json()
    query = data.get("query", "")

    results = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = f"https://www.fiverr.com/search/gigs?query={query.replace(' ', '%20')}"
            page.goto(url)
            page.wait_for_timeout(5000)

            # Extraer títulos (máx. 5)
            titles = page.query_selector_all("h3")
            for title in titles[:5]:
                if title:
                    results.append({
                        "title": title.inner_text()
                    })

            browser.close()

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render asigna este puerto
    app.run(host="0.0.0.0", port=port)
