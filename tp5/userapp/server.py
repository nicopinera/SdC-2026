# =============================================================================
# server.py: Aplicación de usuario que actúa como puente entre el CDD y el navegador.
#
# Lo que hace:
#   - Lee el valor actual del dispositivo (real o simulado)
#   - Mantiene un historial de las últimas 60 muestras
#   - Sirve una interfaz web en http://0.0.0.0:9090
#   - Expone endpoints HTTP para que el navegador consulte los datos
#
# Endpoints disponibles:
#   GET /          → sirve la página web (index.html)
#   GET /data      → devuelve JSON con el historial de la señal activa
#   GET /select?signal=N → cambia la señal activa (1 o 2) y resetea historial
#
# Modo de operación:
#   USE_DEVICE = True  → lee/escribe sobre /dev/cdd (driver real cargado)
#   USE_DEVICE = False → usa archivos /tmp/ generados por simulador_cdd.sh
# =============================================================================

import json
import os
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- Configuración de modo --------------------------------------------------

USE_DEVICE  = True           # True = /dev/cdd, False = simulación por archivos

DEVICE_FILE = "/dev/cdd"     # dispositivo real
SIGNAL_FILE = "/tmp/cdd_signal"  # (solo modo simulación)
VALUE_FILE  = "/tmp/cdd_value"   # (solo modo simulación)

# ---------------------------------------------------------------------------

MAX_PTS = 60
history = []
current_signal = 1


def read_device():
    """Lee el valor actual — del driver real o del archivo de simulación."""
    try:
        if USE_DEVICE:
            with open(DEVICE_FILE, "r") as f:
                return int(f.read().strip())
        else:
            with open(VALUE_FILE, "r") as f:
                return int(f.read().strip())
    except Exception:
        return 0


def select_signal(n):
    """Cambia la señal activa y resetea el historial."""
    global current_signal, history
    try:
        if USE_DEVICE:
            with open(DEVICE_FILE, "w") as f:
                f.write(str(n))
        else:
            with open(SIGNAL_FILE, "w") as f:
                f.write(str(n))
    except Exception:
        pass
    current_signal = n
    history.clear()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        global history

        if self.path == "/":
            with open(os.path.join(os.path.dirname(__file__), "web/index.html")) as f:
                html = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        elif self.path == "/data":
            val = read_device()
            history.append({"t": int(time.time()), "v": val})
            if len(history) > MAX_PTS:
                history.pop(0)
            payload = json.dumps({"signal": current_signal, "data": history})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload.encode())

        elif self.path.startswith("/select"):
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            sig = int(params.get("signal", [1])[0])
            select_signal(sig)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        else:
            self.send_response(404)
            self.end_headers()


mode = "dispositivo /dev/cdd" if USE_DEVICE else "simulacion por archivos /tmp/"
print(f"Modo: {mode}")
print("Servidor corriendo en http://0.0.0.0:9090")
HTTPServer(("", 9090), Handler).serve_forever()
