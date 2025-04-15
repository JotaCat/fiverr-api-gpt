from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

AFFILIATE_ID = "1114947"
BASE_AFFILIATE_URL = f"https://go.fiverr.com/visit/?bta={AFFILIATE_ID}&brand=fiverrmarketplace&url="

@app.route("/fiverr/search", methods=["POST"])
def buscar_gigs():
    data = request.get_json()
    query = data.get("query", "")

    resultados = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = f"https://www.fiverr.com/search/gigs?query={query.replace(' ', '%20')}"
            page.goto(url)
            page.wait_for_timeout(6000)

            gigs = page.query_selector_all("li[data-testid='gig-card-layout']")
            for gig in gigs[:5]:
                titulo = gig.query_selector("h3")
                precio = gig.query_selector("[data-testid='price']")
                enlace = gig.query_selector("a")
                vendedor = gig.query_selector("[data-testid='seller-name']")
                rating = gig.query_selector("[data-testid='rating-score']")

                titulo_texto = titulo.inner_text() if titulo else "Sin título"
                precio_texto = precio.inner_text() if precio else "No disponible"
                vendedor_texto = vendedor.inner_text() if vendedor else "Desconocido"
                rating_texto = rating.inner_text() if rating else "Sin rating"
                enlace_href = enlace.get_attribute("href") if enlace else "#"
                enlace_completo = f"{BASE_AFFILIATE_URL}https://www.fiverr.com{enlace_href}" if enlace_href.startswith("/") else enlace_href

                resultados.append({
                    "titulo": titulo_texto,
                    "precio": precio_texto,
                    "vendedor": vendedor_texto,
                    "rating": rating_texto,
                    "link_afiliado": enlace_completo
                })

            browser.close()
        return jsonify(resultados)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Servidor Flask activo 🔥"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
