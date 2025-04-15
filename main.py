from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import logging
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route("/fiverr/search", methods=["POST"])
def buscar_gigs():
    data = request.get_json()
    query = data.get("query", "")
    results = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
            page = browser.new_page()
            url = f"https://www.fiverr.com/search/gigs?query={query.replace(' ', '%20')}"
            page.goto(url, timeout=60000)
            page.wait_for_timeout(5000)

            gigs = page.query_selector_all("li[data-testid='gig-card-layout']")[:5]

            for gig in gigs:
                titulo = gig.query_selector("h3")
                precio = gig.query_selector("[data-testid='price'] span")
                vendedor = gig.query_selector("a[data-testid='seller-link']")
                rating = gig.query_selector("[data-testid='rating-score']")
                link = gig.query_selector("a")
                
                results.append({
                    "titulo": titulo.inner_text().strip() if titulo else "Sin título",
                    "precio": precio.inner_text().strip() if precio else "N/A",
                    "vendedor": vendedor.inner_text().strip() if vendedor else "Desconocido",
                    "rating": rating.inner_text().strip() if rating else "Sin valoraciones",
                    "link_afiliado": (
                        f"https://go.fiverr.com/visit/?bta=1114947&brand=fiverrmarketplace&url={link.get_attribute('href')}"
                        if link else "Sin enlace"
                    )
                })

            browser.close()
        return jsonify(results)

    except Exception as e:
        logging.error(f"Error en la búsqueda: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Servidor Flask activo 🔥"
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

