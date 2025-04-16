import subprocess
import os
import logging
from flask import Flask, request, jsonify, send_file
from playwright.sync_api import sync_playwright
from waitress import serve

# Instalación automática de navegadores para entornos como Render
try:
    subprocess.run(["playwright", "install"], check=True)
except Exception as e:
    logging.error(f"❌ Error instalando navegadores Playwright: {e}")

# Activamos logs en modo DEBUG
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

def extraer_gigs(query: str):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = browser.new_page()
        url = f"https://www.fiverr.com/search/gigs?query={query.replace(' ', '%20')}"
        logging.info(f"🌐 Visitando URL: {url}")
        page.goto(url, timeout=60000)
        page.wait_for_timeout(10000)

        # Captura HTML
        html = page.content()
        logging.debug(f"\n\n== HTML capturado ==\n{html[:3000]}\n...\n")

        # Guardar HTML para revisar manualmente
        with open("/tmp/fiverr_debug.html", "w", encoding="utf-8") as f:
            f.write(html)

        # Buscar los gigs con selectores
        gigs = page.query_selector_all("li[data-testid='gig-card-layout']")
        if not gigs:
            logging.warning("⚠️ No se encontraron gigs con selector principal. Probando fallback...")
            gigs = page.query_selector_all("article")

        for gig in gigs[:5]:
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
                "descripcion": (
                    f"{titulo.inner_text().strip() if titulo else 'Gig sin título'} "
                    f"por {vendedor.inner_text().strip() if vendedor else 'vendedor desconocido'}, "
                    f"desde {precio.inner_text().strip() if precio else 'precio no disponible'} "
                    f"con valoración de {rating.inner_text().strip() if rating else 'sin puntuación'} estrellas."
                ),
                "link_afiliado": (
                    f"https://go.fiverr.com/visit/?bta=1114947&brand=fiverrmarketplace&url={link.get_attribute('href')}"
                    if link else "Sin enlace"
                )
            })

        browser.close()
    return results

@app.route("/fiverr/search", methods=["POST"])
def buscar_gigs():
    try:
        data = request.get_json()
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Falta el parámetro 'query'"}), 400

        resultados = extraer_gigs(query)
        return jsonify(resultados)

    except Exception as e:
        logging.error(f"❌ Error en la búsqueda: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/debug/html", methods=["GET"])
def ver_html():
    """Devuelve el HTML que capturamos en la última búsqueda."""
    if os.path.exists("/tmp/fiverr_debug.html"):
        return send_file("/tmp/fiverr_debug.html", mimetype="text/html")
    return "❌ No se ha capturado HTML aún", 404

@app.route("/", methods=["GET"])
def home():
    return "Servidor Flask activo 🔥"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    serve(app, host='0.0.0.0', port=port)
