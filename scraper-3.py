import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def buscar_urls(query, limite=3):
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    urls = []

    for a in soup.select("a.result__a"):
        href = a.get("href")
        if href:
            urls.append(href)
        if len(urls) >= limite:
            break

    return urls

def extraer_texto(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    main = soup.find("main") or soup.find("article") or soup.body
    if main:
        return main.get_text(separator="", strip=True)
    return soup.get_text(separator="", strip=True)

def descargar_entidad(nombre):
    urls = buscar_urls(nombre)
    if not urls:
        print("No se encontraron resultados.")
        return

    salida = []
    for url in urls:
        try:
            texto = extraer_texto(url)
            salida.append(f"URL: {url}{texto}{'-'*60}")
        except Exception as e:
            salida.append(f"URL: {url}ERROR: {e}{'-'*60}")

    archivo = nombre.replace(" ", "_") + ".txt"
    with open(archivo, "w", encoding="utf-8") as f:
        f.write("".join(salida))

    print(f"Guardado en {archivo}")

if __name__ == "__main__":
    nombre = input("Escribe el nombre de la empresa o persona: ").strip()
    descargar_entidad(nombre)
