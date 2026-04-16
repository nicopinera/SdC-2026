import requests,csv

# Link API Banco mundial
url_banco_mundial = "https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22"
resultado = requests.get(url=url_banco_mundial) # Se genera la peticion GET
pais_buscado = "Argentina"

print("---"*10)
if resultado:
    print("Se obtuno resultado con metodo GET")
else:
    print("Error al obtener informacion")

print("Status Code: ", resultado.status_code)
print("---"*10)
print(f"Procesando datos de API para {pais_buscado.upper()}")

# Se convierte los datos a JSON
data = resultado.json()
registros = data[1] # Utilizamos el segund item que tiene los datos

# Abrimos el csv
with open('datos_gini.csv','w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['anio', 'valor']) # Encabezados

    for item in registros:
        anio = item['date']
        valor = item['value']
        pais = item["country"]["value"]
        if pais == pais_buscado and valor is not None:
            print(f"Año {anio} : {valor}")
            writer.writerow([anio,valor])

print("---"*10)
print("Fin de programa")