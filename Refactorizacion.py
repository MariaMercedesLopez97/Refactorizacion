import heapq  # Esto nos ayuda a trabajar con colas de prioridad, que es esencial para implementar el algoritmo A*

# ----------------------Clase Ansi para colorear la matriz---------------------
class Ansi:
    ESC = '\033['  # Esto es como una palabra para cambiar colores en la pantalla.
    #---Lista de Colores------
    COLORS = {
        'reset': '0',  # "reset" vuelve el texto a su color normal.
        'black': '30',  # negro.
        'red': '31',    # rojo.
        'green': '32',  # verde.
        'yellow': '33', # amarillo.
        'blue': '34',   # azul.
        'magenta': '35',# púrpura.
        'cyan': '36',   # azul claro.
        'white': '37'   # blanco.
    }

    def __init__(self, text): 
        self.text = text  # Guardamos el texto que queremos colorear.

    def colorize(self, color):  # Devuelve el texto coloreando utilizando el codigo ANSI
        color_code = self.COLORS.get(color, self.COLORS['reset'])  # Buscamos el código del color que queremos.
        return f"{self.ESC}{color_code}m{self.text}{self.ESC}0m"  # Devolvemos el texto con el color cambiado.

#---------------------Constantes para la representación del mapa y Obstáculos-------------------
CAMINO = 0  
EDIFICIO = 1 
BACHE = 2  
AREA_BLOQUEADA = 3  

#---Colores de los Obstaculos---

COLOR_CAMINO = 'blue'  # azul.
COLOR_EDIFICIO = 'green'  # verde.
COLOR_BACHE = 'yellow'  # amarillo.
COLOR_AREA_BLOQUEADA = 'red'  # rojo.
COLOR_CAMINO_ENCONTRADO = 'cyan'  # azul claro.

#------------------------Clase Mapa--------------------------------------------
class Mapa:
    def __init__(self, rutas):
        self.rutas = rutas

    def mostrar(self, camino=[]):
        simbolos = {CAMINO: '.', EDIFICIO: 'E', BACHE: 'B', AREA_BLOQUEADA: 'A'}
        colores = {CAMINO: COLOR_CAMINO, EDIFICIO: COLOR_EDIFICIO, BACHE: COLOR_BACHE, AREA_BLOQUEADA: COLOR_AREA_BLOQUEADA}

        #----- Imprimir encabezado horizontal -----
        print("    " + " ".join(map(str, range(len(self.rutas[0])))))
        print("    " + "_" * (len(self.rutas[0]) * 2 - 1))

        for fila in range(len(self.rutas)):
            linea = [str(fila) + " |"]
            for columna in range(len(self.rutas[fila])):
                celda = self.rutas[fila][columna]
                simbolo = simbolos.get(celda, '?')
                if (fila, columna) in camino:
                    color = COLOR_CAMINO_ENCONTRADO
                    simbolo = '*'
                else:
                    color = colores.get(celda, 'reset')
                ansi_text = Ansi(simbolo).colorize(color)
                linea.append(ansi_text)
            linea.append("|")
            print(' '.join(linea))
        print("    " + "_" * (len(self.rutas[0]) * 2 - 1)) # Vertical
        print()

        #-----Agregar Obstaculo-----
    def agregar_obstaculo(self, fila, columna):
        if self.rutas[fila][columna] == CAMINO:
            self.rutas[fila][columna] = EDIFICIO
        else:
            print("La celda ya está ocupada por otro obstáculo. Inténtalo de nuevo.")

        #-----Quitar Obstaculo----
    def quitar_obstaculo(self, fila, columna):
        if self.rutas[fila][columna] != CAMINO:
            self.rutas[fila][columna] = CAMINO
        else:
            print("La celda no tiene un obstáculo. Inténtalo de nuevo.")

        #-----es accesible------
    def es_accesible(self, fila, columna):
        return self.rutas[fila][columna] == CAMINO

#------Clase Calculadora de Rutas----------
class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa

    def heuristica_manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def encontrar_camino(self, punto_inicio, punto_final):
        rutas = self.mapa.rutas
        filas, columnas = len(rutas), len(rutas[0])
        lista_abierta = [(0, punto_inicio)]
        rastrea = {}
        guarda_costo_camino = {punto_inicio: 0}
        guarda_costo_total = {punto_inicio: self.heuristica_manhattan(punto_inicio, punto_final)}

        while lista_abierta:
            _, nodo_actual = heapq.heappop(lista_abierta)

            if nodo_actual == punto_final:
                camino = []
                while nodo_actual in rastrea:
                    camino.append(nodo_actual)
                    nodo_actual = rastrea[nodo_actual]
                camino.append(punto_inicio)
                return camino[::-1]

            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                vecino = (nodo_actual[0] + dr, nodo_actual[1] + dc)

                if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                    if self.mapa.es_accesible(vecino[0], vecino[1]):
                        costo_tentativo = guarda_costo_camino[nodo_actual] + 1
                        if vecino not in guarda_costo_camino or costo_tentativo < guarda_costo_camino[vecino]:
                            rastrea[vecino] = nodo_actual
                            guarda_costo_camino[vecino] = costo_tentativo
                            guarda_costo_total[vecino] = costo_tentativo + self.heuristica_manhattan(vecino, punto_final)
                            heapq.heappush(lista_abierta, (guarda_costo_total[vecino], vecino))

        return []

#-----------------Función para ingresar coordenadas----------------------------
def ingresar_coordenadas(mensaje, max_filas, max_columnas):
    while True:
        try:
            fila, columna = map(int, input(mensaje).split(','))
            if 0 <= fila < max_filas and 0 <= columna < max_columnas:
                return (fila, columna)
            else:
                print("Coordenadas fuera de rango. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada inválida. Usa el formato fila,columna. Inténtalo de nuevo.")

#----------- Ejecución del programa------------
rutas_iniciales = [
    [0, 0, 0, 0, 0],  
    [0, 3, 0, 0, 2],  
    [2, 0, 0, 0, 0], 
    [0, 0, 2, 0, 0], 
    [0, 0, 0, 3, 0]   
]

mapa = Mapa(rutas_iniciales)
calculadora = CalculadoraRutas(mapa)


print("Mapa inicial:")
mapa.mostrar()

#-------- Coordenadas---------
punto_inicio = ingresar_coordenadas("Ingresa las coordenadas del punto de inicio (fila,columna): ", len(rutas_iniciales), len(rutas_iniciales[0]))
punto_final = ingresar_coordenadas("Ingresa las coordenadas del punto final (fila,columna): ", len(rutas_iniciales), len(rutas_iniciales[0]))


#-------Agregar o quitar obstaculos y si quieres realizar otra accion-----------------
while True:
    accion = input("¿Quieres agregar o quitar un obstáculo? (agregar/quitar): ").lower()
    if accion in ['agregar', 'quitar']:
        obstaculo = ingresar_coordenadas(f"Ingresa las coordenadas del obstáculo para {accion} (fila,columna): ", len(rutas_iniciales), len(rutas_iniciales[0]))
        if accion == 'agregar':
            mapa.agregar_obstaculo(obstaculo[0], obstaculo[1])
        elif accion == 'quitar':
            mapa.quitar_obstaculo(obstaculo[0], obstaculo[1])
        mapa.mostrar()
    continuar = input("¿Quieres realizar otra acción? (si/no): ").lower()
    if continuar != 'si':
        break

camino = calculadora.encontrar_camino(punto_inicio, punto_final)

# Para Imprimir el mensaje
if camino:
    print(f"El camino más corto de {punto_inicio} a {punto_final} es:")
    mapa.mostrar(camino)
else:
    print("No hay un camino disponible desde el punto de inicio hasta el punto final.")
# Imprime el camino es corto desde hasta donde y si no hay camino disponible desde hasta donde
