import csv
import os

# Nombre de nuestra base de datos
DB_FILENAME = 'companias_categorizadas.csv'
# Los encabezados o títulos de nuestras columnas
HEADERS = ['Nombre_Empresa', 'Industria_Principal', 'Verticales_de_Talento']

def setup_database():
    """
    Esta función revisa si el archivo CSV ya existe.
    Si no existe, lo crea y le escribe los encabezados.
    """
    # os.path.exists() revisa si un archivo ya existe
    if not os.path.exists(DB_FILENAME):
        print(f"Creando nueva base de datos: {DB_FILENAME}")
        
        # 'w' (write) crea un archivo nuevo (o sobrescribe uno)
        with open(DB_FILENAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS) # Escribe la fila de encabezados
        print("Base de datos creada con encabezados.")
    else:
        print(f"Base de datos encontrada: {DB_FILENAME}")

def main():
    """
    Función principal para guardar una nueva compañía.
    """
    setup_database() # Revisa si la base de datos existe
    
    print("\n--- Agregar Nueva Compañía ---")
    print("(Copia y pega la información que te dio la IA)")

    # 1. Pedimos la información al usuario
    nombre = input("Nombre de la Empresa: ")
    industria = input("Industria Principal: ")
    
    # Usamos .strip() para limpiar espacios en blanco al inicio o final
    verticales_input = input("Pega TODAS las Verticales (separadas por comas): ")
    
    # 2. Preparamos la fila de datos para guardar
    # Unimos todas las verticales en una sola celda, separadas por '|'
    # (Usamos '|' en lugar de ',' para que no se confunda con las comas del CSV)
    verticales_limpias = ', '.join([v.strip() for v in verticales_input.split(',')])
    
    nueva_fila = [nombre, industria, verticales_limpias]
    
    # 3. Agregamos la nueva fila al archivo
    # 'a' (append) significa "añadir al final" sin borrar lo anterior
    try:
        with open(DB_FILENAME, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(nueva_fila)
            
        print(f"\n[✓] ¡Éxito! '{nombre}' ha sido guardado en {DB_FILENAME}")
        
    except Exception as e:
        print(f"\n[!] Ocurrió un error al guardar: {e}")

if __name__ == "__main__":
    main()