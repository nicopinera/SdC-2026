import requests,os,ctypes
from dotenv import load_dotenv

actual = os.path.abspath(__file__) # Ruta actual del script
carpeta = os.path.dirname(actual) # Carpeta actual
RUTA_BASE = os.path.dirname(carpeta) # Carpeta TP2
RUTA_ENV = os.path.join(RUTA_BASE,".env") # Archivo .env
RUTA_DATA = os.path.join(RUTA_BASE,"data")


def cargar_env():
    """
    Funcion que carga las variables de entorno y devuelve
    el url del banco mundial junto con el pais a analizar
    """
    load_dotenv(RUTA_ENV) # Carga de variables de entorno dentro del .env
    return os.getenv('URL_BANCO_MUNDIAL'),os.getenv('PAIS') # Devolvemos la url del api

def realizar_peticion_banco_mundial(url):
    """
    Realiza la peticion HTTP GET
    """
    resultado = requests.get(url)
    if not resultado:
        print("Error al realizar en HTTP GET")
        return None
    
    if resultado.status_code != 200:
        print(f"Fallo en peticion GET, status_code = {resultado.status_code}")
        return None

    datos = resultado.json()
    return datos[1]

def obtener_datos_pais(datos,pais):
    """
    Obtiene los años y valores del indice GINI de un pais especifico

    Devuelve dos array: anios y valores
    """
    anios = []
    valores = []
    for item in datos:
        anio = item['date'] # string
        valor = item['value'] # float
        pais_aux = item["country"]["value"]
        if pais_aux == pais and valor is not None:
            anios.append(anio)
            valores.append(valor)
    return anios,valores

def generar_txt(pais,anios,valores):
    txt = os.path.join(RUTA_DATA,f"{pais}.txt")
    with open(txt,"w") as f:
        for a,v in zip(anios,valores):
            f.write(f"{a} - {v}\n")

def c_y_asm(valores):
    ruta_lib = os.path.join(RUTA_BASE,"libpython.so")
    lib = ctypes.CDLL(ruta_lib)
    

def main():
    """
    Funcion principal
    """

    # Obtenemos las variables de entorno
    url_banco_mundial,pais = cargar_env()

    # Obtenemos la informacion por HTTP GET
    informacion = realizar_peticion_banco_mundial(url=url_banco_mundial)
    if not informacion:
        print("Error al obtener informacion")

    anios, valores = obtener_datos_pais(informacion,pais)
    
    generar_txt(pais,anios,valores)



if __name__ == "__main__":
    main()