from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

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
            page.wait_for_timeout(6000)

            # Buscar bloques de gigs
            gigs = page.query_selector_all("li.gig-card-layout")

            for gig in gigs[:5]:  # Solo los primeros 5
                try:
                    title = gig.query_selector("h3").inner_text()
                    price = gig.query_selector("div.price-wrapper").inner_text()
                    seller = gig.query_selector("a.seller-name").inner_text()
                    rating = gig.query_selector("span.rating").inner_text()
                    link = gig.query_selector("a").get_attribute("href")

                    # Enlace de afiliado
                    affiliate_link = f"https://go.fiverr.com/visit/?bta=1114947&brand=fiverrmarketplace&url=https://www.fiverr.com{link}"

                    results.append({
                        "titulo": title,
                        "precio": price,
                        "vendedor": seller,
                        "rating": rating,
                        "link_afiliado": affiliate_link
                    })
                except Exception:
                    continue

            browser.close()
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
