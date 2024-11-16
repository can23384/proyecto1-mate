import time
import concurrent.futures

def construir_conjunto():
    conjunto = []
    while True:
        elemento = input("Ingresa un elemento (A-Z o 0-9) o 'fin' para terminar: ").upper()
        if elemento == 'FIN':
            break
        elif len(elemento) == 1 and (elemento.isdigit() or elemento.isalpha()):
            if elemento not in conjunto:
                conjunto.append(elemento)
        else:
            print("Entrada no válida. Ingresa una letra (A-Z) o un dígito (0-9).")
    return conjunto

def union(conjunto1, conjunto2):
    resultado = conjunto1[:]
    for elemento in conjunto2:
        if elemento not in resultado:
            resultado.append(elemento)
    return resultado

def interseccion(conjunto1, conjunto2):
    resultado = []
    for elemento in conjunto1:
        if elemento in conjunto2:
            resultado.append(elemento)
    return resultado

def diferencia(conjunto1, conjunto2):
    resultado = []
    for elemento in conjunto1:
        if elemento not in conjunto2:
            resultado.append(elemento)
    return resultado

def diferencia_simetrica(conjunto1, conjunto2):
    union_resultado = union(conjunto1, conjunto2)
    interseccion_resultado = interseccion(conjunto1, conjunto2)
    return diferencia(union_resultado, interseccion_resultado)

def complemento(universal, conjunto):
    return diferencia(universal, conjunto)

def ejecutar_operacion(operacion, conjunto1, conjunto2=None, universal=None):
    inicio = time.perf_counter()

    if conjunto1 is None or (conjunto2 is None and operacion != 'complemento'):
        print("Error: Conjunto no seleccionado o inválido.")
        return None, 0

    if operacion == 'union':
        resultado = union(conjunto1, conjunto2)
    elif operacion == 'interseccion':
        resultado = interseccion(conjunto1, conjunto2)
    elif operacion == 'diferencia':
        resultado = diferencia(conjunto1, conjunto2)
    elif operacion == 'diferencia_simetrica':
        resultado = diferencia_simetrica(conjunto1, conjunto2)
    elif operacion == 'complemento':
        resultado = complemento(universal, conjunto1)
    
    duracion = time.perf_counter() - inicio
    
    return resultado, duracion

def seleccionar_conjunto(conjuntos_guardados):
    if not conjuntos_guardados:
        print("No hay conjuntos disponibles. Primero debes crear un conjunto.")
        return None
    print("\nConjuntos disponibles:")
    for i, conjunto in enumerate(conjuntos_guardados):
        print(f"{i + 1}. {conjunto}")
    while True:
        seleccion = input("Selecciona el número del conjunto que deseas usar: ")
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(conjuntos_guardados):
            return conjuntos_guardados[int(seleccion) - 1]
        else:
            print("Selección no válida, intenta nuevamente.")

def operar_conjuntos(conjuntos_guardados):
    universal = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    
    conjunto1 = seleccionar_conjunto(conjuntos_guardados)
    if not conjunto1:
        return
    conjunto2 = None
    if len(conjuntos_guardados) > 1:
        conjunto2 = seleccionar_conjunto(conjuntos_guardados)
    
    print("\nElige una operación:")
    print("1. Unión")
    print("2. Intersección")
    print("3. Diferencia")
    print("4. Diferencia Simétrica")
    print("5. Complemento de Conjunto 1")

    opcion = input("Ingresa la opción deseada: ")

    if opcion == '1':
        operacion = 'union'
    elif opcion == '2':
        operacion = 'interseccion'
    elif opcion == '3':
        operacion = 'diferencia'
    elif opcion == '4':
        operacion = 'diferencia_simetrica'
    elif opcion == '5':
        operacion = 'complemento'
    else:
        print("Opción no válida.")
        return
    
    inicio_total = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(ejecutar_operacion, operacion, conjunto1, conjunto2, universal)
        resultado, duracion_operacion = future.result()

    fin_total = time.perf_counter()
    duracion_total = fin_total - inicio_total

    if resultado is not None:
        print(f"\nEl resultado es: {resultado}")
        print(f"Tiempo de ejecución de la operación: {duracion_operacion:.6f} segundos")
        print(f"Tiempo total de ejecución: {duracion_total:.6f} segundos")
        return resultado

def main():
    conjuntos_guardados = []
    while True:
        print("\n--- Menú Principal ---")
        print("1. Construir conjunto")
        print("2. Operar conjuntos")
        print("3. Finalizar")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            conjunto = construir_conjunto()
            conjuntos_guardados.append(conjunto)
            print(f"Conjunto creado y guardado: {conjunto}")
        elif opcion == '2':
            resultado = operar_conjuntos(conjuntos_guardados)
            if resultado:
                conjuntos_guardados.append(resultado)
                print(f"Resultado guardado como nuevo conjunto: {resultado}")
        elif opcion == '3':
            print("Finalizando el programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
