import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def generar_nombre_archivo(url):
    """
    Crea un nombre de archivo limpio a partir del URL.
    """
    try:
        domain = urlparse(url).netloc
        if not domain:
            domain = urlparse(f"http://{url}").netloc
        
        clean_domain = domain.replace('www.', '')
        return f"output_{clean_domain}.txt"
    except Exception:
        return "output_sitio_desconocido.txt"

def limpiar_texto(html_content):
    """
    Extrae el texto del HTML y elimina líneas en blanco excesivas.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    raw_text = soup.get_text()
    
    lineas_limpias = [line.strip() for line in raw_text.splitlines() if line.strip()]
    
    return '\n'.join(lineas_limpias)

def main():
    """
    Función principal del script.
    """
    url = input("Pega el URL de la página a extraer y presiona Enter: ")
    nombre_archivo = generar_nombre_archivo(url)
    
    print(f"\n[+] Abriendo el navegador para: {url}")

    # --- NUEVA SECCIÓN DE SELENIUM ---
    
    # Configura las opciones de Chrome
    chrome_options = Options()
    # LA SIGUIENTE LÍNEA ESTÁ COMENTADA PARA EVITAR SER DETECTADOS
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Instala y configura el driver automáticamente
    service = Service(ChromeDriverManager().install())
    
    # Inicializa el navegador (el "driver")
    driver = None # Definimos 'driver' aquí para poder cerrarlo en 'finally'
    
    try:
        # 1. Abre el navegador controlado por Python
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 2. Va al URL (aquí es donde se ejecuta el JavaScript)
        driver.get(url)
        
        # 3. ¡ESPERA 5 SEGUNDOS! Esta es la clave.
        # Le da tiempo al sitio web para cargar todo el contenido de JavaScript.
        print("[+] Esperando 5 segundos a que cargue el JavaScript...")
        time.sleep(5)
        
        # 4. Obtiene el HTML *después* de que todo cargó
        html_cargado = driver.page_source
        
        print("[+] HTML cargado. Limpiando el texto...")
        
        # 5. El resto es igual: limpiamos el texto que obtuvimos
        texto_limpio = limpiar_texto(html_cargado)
        
        # 6. Guardamos el archivo
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(texto_limpio)
            
        print(f"\n[✓] ¡Éxito! Texto limpio guardado en: {nombre_archivo}")

    except Exception as e:
        print(f"\n[!] Ocurrió un error inesperado: {e}")
    
    finally:
        # 7. MUY IMPORTANTE: Cierra el navegador
        # No importa si el script tuvo éxito o falló, siempre cerramos el navegador.
        if driver:
            print("[+] Cerrando el navegador.")
            driver.quit()

# --- Fin de la sección de Selenium ---

if __name__ == "__main__":
    main()