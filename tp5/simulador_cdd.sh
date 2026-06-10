# Simula el comportamiento de un Character Device Driver (CDD) real.
# Para el TP final, este script va a ser reemplazado por el módulo de kernel (cdd.ko) que lee señales reales desde los GPIO de la Raspberry Pi.
#
# Lo que hace:
#   - Genera valores numéricos aleatorios cada 1 segundo
#   - Simula DOS señales distintas según cuál esté seleccionada:
#       Señal 1 → Temperatura entre 20°C y 35°C
#       Señal 2 → Presión entre 950 hPa y 1050 hPa
#   - Escribe el valor actual en /tmp/cdd_value  (lo lee server.py)
#   - Lee la señal seleccionada de /tmp/cdd_signal (lo escribe server.py)
#
# Archivos que usa:
#   /tmp/cdd_signal → indica qué señal está activa ("1" o "2")
#   /tmp/cdd_value  → último valor generado, leído por la app de usuario
# =============================================================================
SIGNAL_FILE="/tmp/cdd_signal"
VALUE_FILE="/tmp/cdd_value"

# Señal inicial: arranca con la señal 1 (temperatura)
echo "1" > $SIGNAL_FILE

# Genera un nuevo valor cada 1 segundo (período = 1s)
while true; do
    # Leer cuál señal está seleccionada actualmente
    SIG=$(cat $SIGNAL_FILE)

    if [ "$SIG" = "1" ]; then
        # Señal 1: simula temperatura en °C
        VAL=$((20 + RANDOM % 15))
    else
        # Señal 2: simula presión en hPa
        VAL=$((950 + RANDOM % 100))
    fi

    # Escribir el valor generado para que lo lea server.py
    echo $VAL > $VALUE_FILE

    sleep 1
done