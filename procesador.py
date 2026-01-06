import time
import csv
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuración del CSV ---
DB_FILENAME = 'companias_categorizadas.csv'
HEADERS = ['Nombre_Empresa', 'Industria_Principal', 'Verticales_de_Talento']

def setup_database():
    """Revisa si el CSV existe; si no, lo crea con encabezados."""
    if not os.path.exists(DB_FILENAME):
        print(f"Creando nueva base de datos: {DB_FILENAME}")
        with open(DB_FILENAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)
    else:
        print(f"Base de datos encontrada: {DB_FILENAME}")

# --- Función de Extracción (Selenium) ---
def extraer_texto_web(url):
    """
    Usa Selenium para abrir Chrome, ejecutar JS y extraer el texto limpio.
    """
    print(f"\n[+] Abriendo el navegador para: {url}")
    chrome_options = Options()
    # Dejamos la ventana visible para evitar que nos bloqueen
    # chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        print("[+] Esperando 5 segundos a que cargue el JavaScript...")
        time.sleep(5)
        
        html_cargado = driver.page_source
        print("[+] HTML cargado. Limpiando el texto...")
        
        # Limpiamos el texto
        soup = BeautifulSoup(html_cargado, 'html.parser')
        raw_text = soup.get_text()
        lineas_limpias = [line.strip() for line in raw_text.splitlines() if line.strip()]
        return '\n'.join(lineas_limpias)
        
    finally:
        if driver:
            print("[+] Cerrando el navegador.")
            driver.quit()

# --- Función de Guardado (CSV) ---
def guardar_en_csv(nombre, industria, verticales_input):
    """
    Guarda la información analizada en el archivo CSV.
    """
    try:
        # Limpiamos las verticales por si acaso
        verticales_limpias = ', '.join([v.strip() for v in verticales_input.split(',')])
        
        nueva_fila = [nombre, industria, verticales_limpias]
        
        # 'a' (append) para añadir al final sin borrar
        with open(DB_FILENAME, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(nueva_fila)
            
        print(f"\n[✓] ¡Éxito! '{nombre}' ha sido guardado en {DB_FILENAME}")
        
    except Exception as e:
        print(f"\n[!] Ocurrió un error al guardar en CSV: {e}")

# --- Función Principal (El Orquestador) ---
def main():
    setup_database()
    
    # 1. PEDIR URL
    url = input("Pega el URL de la página a analizar (o 'salir' para terminar): ")
    if url.lower() == 'salir':
        return
    
    # 2. EXTRAER (La parte automática)
    try:
        texto = extraer_texto_web(url)
        if not texto:
            print("[!] No se pudo extraer texto. Abortando.")
            return
            
        print("\n--- ¡EXTRACCIÓN COMPLETA! ---\n")
        print("Copia todo el texto de abajo y pégamelo a mí (la IA) para analizarlo.")
        print("--------------------------------------------------")
        print(texto) # Imprimimos el texto para que lo copies
        print("--------------------------------------------------")
        
        # 3. PAUSA (El "Handoff" manual)
        input("\n...Presiona Enter aquí cuando tengas el análisis y estés listo para guardar...")
        
        # 4. GUARDAR (La parte manual)
        print("\n--- Agregar Análisis ---")
        nombre = input("Nombre de la Empresa: ")
        industria = input("Industria Principal: ")
        verticales_input = input("Pega TODAS las Verticales (separadas por comas): ")
        
        guardar_en_csv(nombre, industria, verticales_input)
        
    except Exception as e:
        print(f"\n[!] Ocurrió un error general: {e}")

if __name__ == "__main__":
    main()