import ctypes
import os

# Cargar la librería (ruta relativa o absoluta)
lib = ctypes.CDLL(os.path.abspath("./libpython.so"))

# Definir tipos de la función
lib.procesar_datos.argtypes = [ctypes.c_float]  # recibe float
lib.procesar_datos.restype = ctypes.c_int  # devuelve int

# Llamada
valor = 3.7
resultado = lib.procesar_datos(ctypes.c_float(valor))

print(f"Entrada: {valor}")
print(f"Resultado: {resultado}")
