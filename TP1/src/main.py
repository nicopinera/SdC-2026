import os
os.system('clear')

# Tiempo de ejecucion por procesador
t_eje_p1 = 83
t_eje_p2 = 97
t_eje_p3 = 52 

# Numero de nucleos
p1_nucleos= 14
p2_nucleos= 12
p3_nucleos= 16

# Rendimientos
r_p1 = round((1/t_eje_p1),ndigits=5)
r_p2 = round((1/t_eje_p2),ndigits=5)
r_p3 = round((1/t_eje_p3),ndigits=5)

# Speedup o aceleracion
s_p1 = 1
s_p2 = round((r_p2/r_p1),ndigits=5)
s_p3 = round((r_p3/r_p1),ndigits=5)

# Eficiencia por nucleo
r_p_n_p1 = round((s_p1/p1_nucleos),ndigits=5)
r_p_n_p2 = round((s_p2/p2_nucleos),ndigits=5)
r_p_n_p3 = round((s_p3/p3_nucleos),ndigits=5)

# Precio en dolares
precio_p1 = 319
precio_p2 = 255
precio_p3 = 699

# Rendimiento por dolar
r_por_d_p1 = r_p1/precio_p1
r_por_d_p2 = r_p2/precio_p2
r_por_d_p3 = r_p3/precio_p3

# Consumo en watts
w_p1 = 125
w_p2 = 105
w_p3 = 170

# Rendimiento por watts
r_por_w_p1 = r_p1/w_p1
r_por_w_p2 = r_p2/w_p2
r_por_w_p3 = r_p3/w_p3

print("---"*10)
print("Analisis de Rendimiento para procesadores")
print("Procesador 1 (base): Intel Core i5-13600K")
print("Procesador 2: AMD Ryzen 9 5900X")
print("Procesador 3: AMD Ryzen 9 7950X")
print("---"*10)
print("Tiempo de ejecucion para compilar el kernel de linux")
print(f"Procesador 1 (base): {t_eje_p1} [s]")
print(f"Procesador 2: {t_eje_p2} [s]")
print(f"Procesador 3: {t_eje_p3} [s]")
print("---"*10)
print("Rendimiento")
print(f"Procesador 1 (base): {r_p1}")
print(f"Procesador 2: {r_p2}")
print(f"Procesador 3: {r_p3}")
print("---"*10)
print("Speedup")
print(f"Procesador 1 (base): {s_p1} - {s_p1*100}%")
print(f"Procesador 2: {s_p2} - {s_p2*100}%")
print(f"Procesador 3: {s_p3} - {s_p3*100}%")
print("---"*10)
print("Eficiencia por nucleo")
print(f"Procesador 1 (base): {r_p_n_p1} - {r_p_n_p1*100}%")
print(f"Procesador 2: {r_p_n_p2} - {r_p_n_p2*100}%")
print(f"Procesador 3: {r_p_n_p3} - {r_p_n_p3*100}%")
print("---"*10)
print("Rendimiento por Dolar")
print(f"Procesador 1 (base): {r_por_d_p1} - {r_por_d_p1*100}%")
print(f"Procesador 2: {r_por_d_p2} - {r_por_d_p2*100}%")
print(f"Procesador 3: {r_por_d_p3} - {r_por_d_p3*100}%")
print("---"*10)
print("Rendimiento por Watts")
print(f"Procesador 1 (base): {r_por_w_p1} - {r_por_w_p1*100}%")
print(f"Procesador 2: {r_por_w_p2} - {r_por_w_p2*100}%")
print(f"Procesador 3: {r_por_w_p3} - {r_por_w_p3*100}%")