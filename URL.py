import requests
from bs4 import BeautifulSoup

# --- Configuración ---
# Esta es la URL que pusiste en tu ejecución
url = 'https://careers.mcdonalds.com/2026-global-technology-cybersecurity-intern/job/A645606D5F5E911CABC9E57C920EA047'
nombre_archivo = 'sitioweb.txt'

# <<< ¡ESTA ES LA PARTE NUEVA! >>>
# Estos encabezados (headers) simulan ser un navegador Chrome en una Mac.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}
# --------------------------------

print(f"Obteniendo datos de: {url}")

try:
    # 1. Hacemos la petición, AHORA CON LOS HEADERS
    #    Le pasamos el diccionario de 'headers' a la función .get()
    response = requests.get(url, headers=headers)
    
    # 2. "Parseamos" o analizamos el HTML con BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # 3. Extraemos TODO el texto visible de la página
    texto = soup.get_text()

    # 4. Guardamos el texto en un archivo .txt
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write(texto)

    print(f"¡Éxito! Todo el texto ha sido guardado en: {nombre_archivo}")

except requests.exceptions.RequestException as e:
    # Esto atrapará errores (ej. si no tienes internet o la URL está mal)
    print(f"Error al intentar obtener la página: {e}")