# Prueba del agente explicador (`explicador_python`)

## Tema 1: Explica las listas de Python

Aquí tienes la explicación sobre las listas en Python:

### 1. Explicación breve y clara
Las **listas** en Python son colecciones ordenadas y mutables (se pueden modificar) que permiten almacenar múltiples elementos en una sola variable. Pueden contener datos de diferentes tipos (números, texto, booleanos u otras listas) y se definen utilizando corchetes `[]`, separando los elementos con comas.

---

### 2. Ejemplo pequeño y funcional de código

```python
# Crear una lista de frutas
frutas = ["manzana", "banana", "naranja"]

# Agregar un nuevo elemento al final
frutas.append("pera")

# Modificar el primer elemento (los índices inician en 0)
frutas[0] = "fresa"

# Imprimir la lista y un elemento en particular
print("Lista completa:", frutas)
print("El segundo elemento es:", frutas[1])
3. Error frecuente o advertencia
Un error muy común es el IndexError: list index out of range.

Este error ocurre cuando intentas acceder a un índice que no existe en la lista. Recuerda que en Python se empieza a contar desde el índice 0. Por lo tanto, si una lista tiene 3 elementos, sus posiciones válidas son 0, 1 y 2. Si intentas acceder a lista[3], Python lanzará una excepción indicando que estás fuera del rango de la lista.

Tema 2: Explica las funciones de Python
1. Explicación breve y clara
Las funciones en Python son bloques de código reutilizables diseñados para realizar una tarea específica. Sirven para organizar el programa en partes más pequeñas, evitar la repetición de código y hacer que sea más fácil de leer y mantener.

Se definen utilizando la palabra clave def, seguida del nombre de la función y paréntesis (). Pueden recibir datos de entrada (llamados parámetros) y pueden devolver un resultado hacia donde fueron llamadas mediante la instrucción return.

2. Ejemplo de código en Python
Python
# Definición de la función que calcula el área de un rectángulo
def calcular_area(base, altura):
    area = base * altura
    return area

# Llamada a la función pasándole argumentos
resultado = calcular_area(5, 3)

# Imprimir el resultado
print(f"El área del rectángulo es: {resultado}")
# Salida: El área del rectángulo es: 15
3. Error frecuente o advertencia
Un error muy común al empezar es olvidar la sentencia return cuando necesitas usar el resultado de la función más adelante. Si no colocas un return, Python ejecutará el código pero devolverá implícitamente None.

Ejemplo del error:

Python
def sumar(a, b):
    total = a + b
    # Falta: return total

resultado = sumar(4, 2)
print(resultado)  # Imprimirá 'None' en lugar de 6, lo que causará fallos en cálculos posteriores.

Guárdalo en `ejemplos/prueba_explicador.md`, borra el archivo temporal `evidencia.py` si todavía lo tienes, marca todas las casillas de autovalidación de esta tarea y ya puedes pasar a la **Tarea 3: Guardar Markdown de forma segura**.