# =============================================================================
# server.py: Aplicación de usuario que actúa como puente entre el CDD y el navegador.
#
# Lo que hace:
#   - Lee el valor actual del dispositivo (simulado o real en /dev/cdd)
#   - Mantiene un historial de las últimas 60 muestras
#   - Sirve una interfaz web en http://localhost:8080
#   - Expone endpoints HTTP para que el navegador consulte los datos
#
# Endpoints disponibles:
#   GET /          → sirve la página web (index.html)
#   GET /data      → devuelve JSON con el historial de la señal activa
#   GET /select?signal=N → cambia la señal activa (1 o 2) y resetea historial
#
# Para el TP final, VALUE_FILE y SIGNAL_FILE se van a reemplazar por
# lectura/escritura directa sobre /dev/cdd
# =============================================================================

from http.server import HTTPServer, BaseHTTPRequestHandler
import json, time, os, urllib.parse

# Archivos que simulan el dispositivo
SIGNAL_FILE = "/tmp/cdd_signal"   # señal seleccionada ("1" o "2")
VALUE_FILE  = "/tmp/cdd_value"    # último valor medido

MAX_PTS = 60

history = []

current_signal = 1

# Lee el último valor generado por el simulador (o por el CDD real). 
def read_device():

    try:
        with open(VALUE_FILE) as f:
            return int(f.read().strip())
    except:
        return 0  # si falla la lectura, devuelve 0

# Cambia la señal activa escribiendo en el archivo de control.
def select_signal(n):

    global current_signal, history
    with open(SIGNAL_FILE, "w") as f:
        f.write(str(n))
    current_signal = n
    history.clear()  # reset del gráfico al cambiar de señal

# Manejador de requests HTTP. Responde a los tres endpoints definidos.
class Handler(BaseHTTPRequestHandler):

    def log_message(self, *args):
        pass  
    def do_GET(self):
        global history

        
        if self.path == "/":
            with open("/home/juana/SdC-2026/tp5/userapp/web/index.html") as f:
                html = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        
        elif self.path == "/data":
            # Lee el dispositivo, agrega al historial y devuelve JSON
            val = read_device()
            history.append({"t": int(time.time()), "v": val})


            if len(history) > MAX_PTS:
                history.pop(0)

            payload = json.dumps({"signal": current_signal, "data": history})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")  # permite CORS
            self.end_headers()
            self.wfile.write(payload.encode())

        
        elif self.path.startswith("/select"):
            # Extrae el parámetro ?signal=N de la URL
            params = urllib.parse.parse_qs(
                        urllib.parse.urlparse(self.path).query)
            sig = int(params.get("signal", [1])[0])
            select_signal(sig)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

print("Servidor corriendo en http://localhost:8080")
HTTPServer(("", 8080), Handler).serve_forever()