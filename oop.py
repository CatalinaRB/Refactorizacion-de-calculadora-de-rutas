import heapq

class Mapa:
    def __init__(self, mapa):
        self.mapa = mapa
        self.filas = len(mapa)
        self.columnas = len(mapa[0])

    def agregar_obstaculo(self, fila, columna):
        if self.es_celda_valida(fila, columna) and self.mapa[fila][columna] == 0:
            self.mapa[fila][columna] = 1
            print(f"Obstáculo añadido en ({fila}, {columna})")
        else:
            print("La posición no es válida o ya existe un obstáculo en esa posición.")

    def quitar_obstaculo(self, fila, columna):
        if self.es_celda_valida(fila, columna) and self.mapa[fila][columna] == 1:
            self.mapa[fila][columna] = 0
            print(f"Obstáculo removido en ({fila}, {columna})")
        else:
            print("La posición no es válida o no hay un obstáculo en esa posición.")

    def es_celda_accesible(self, fila, columna):
        return self.es_celda_valida(fila, columna) and self.mapa[fila][columna] == 0

    def es_celda_valida(self, fila, columna):
        return 0 <= fila < self.filas and 0 <= columna < self.columnas

    def visualizar(self, camino=None):
        colores = {
            0: '\033[97m.',     # Carretera (Blanco)
            1: '\033[91mE',     # Edificio (Rojo)
            2: '\033[94mA',     # Agua (Azul)
            3: '\033[93mB',     # Área bloqueada (Amarillo)
            'ruta': '\033[92m*',  # Ruta más corta (Verde)
        }
        
        print("\nMapa actual:")
        print("    " + " ".join(f"{i}" for i in range(self.columnas)))
        print("  " + "--" * self.columnas)

        for fila in range(self.filas):
            visualizacion = f"{fila} | "
            for columna in range(self.columnas):
                if camino and (fila, columna) in camino:
                    visualizacion += colores['ruta']
                else:
                    visualizacion += colores[self.mapa[fila][columna]]
                visualizacion += " "
            print(visualizacion + '|')

        print("  " + "--" * self.columnas)
        print('\033[0m')  # Restablecer el color al valor predeterminado

    def solicitar_coordenadas(self, mensaje):
        while True:
            try:
                fila = int(input(f"Ingrese la fila del {mensaje}: "))
                columna = int(input(f"Ingrese la columna del {mensaje}: "))
                if self.es_celda_valida(fila, columna) and self.mapa[fila][columna] == 0:
                    return (fila, columna)
                else:
                    print(f"La posición ({fila}, {columna}) no es válida o contiene un obstáculo. Intente de nuevo.")
            except (ValueError, IndexError):
                print("Coordenadas inválidas. Intente de nuevo.")

class CalculadoraRutas:
    def __init__(self, mapa):
        self.mapa = mapa
        self.filas = len(mapa)
        self.columnas = len(mapa[0])
        self.movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha

    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_estrella(self, inicio, fin):
        cola = []
        heapq.heappush(cola, (0, inicio))
        costos = {inicio: 0}
        rutas = {inicio: None}

        while cola:
            prioridad, actual = heapq.heappop(cola)

            if actual == fin:
                break

            for movimiento in self.movimientos:
                nx, ny = actual[0] + movimiento[0], actual[1] + movimiento[1]

                if 0 <= nx < self.filas and 0 <= ny < self.columnas and self.mapa[nx][ny] != 1:
                    nuevo_costo = costos[actual] + 1
                    vecino = (nx, ny)

                    if vecino not in costos or nuevo_costo < costos[vecino]:
                        costos[vecino] = nuevo_costo
                        prioridad = nuevo_costo + self.heuristica(fin, vecino)
                        heapq.heappush(cola, (prioridad, vecino))
                        rutas[vecino] = actual

        camino = []
        if fin in rutas:
            actual = fin
            while actual:
                camino.append(actual)
                actual = rutas[actual]
            camino.reverse()

        return camino

def main():
    mapa_inicial = [
        [0, 0, 0, 1, 0],
        [0, 2, 0, 0, 3],
        [3, 0, 0, 0, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 0]
    ]

    mapa_objeto = Mapa(mapa_inicial)
    ruta_calculadora = CalculadoraRutas(mapa_inicial)

    mapa_objeto.visualizar()

    respuesta = input("¿Desea agregar obstáculos? (s/n): ").lower()
    if respuesta == 's':
        num_obstaculos = int(input("¿Cuántos obstáculos desea agregar? "))
        for _ in range(num_obstaculos):
            fila = int(input("Ingrese la fila del obstáculo: "))
            columna = int(input("Ingrese la columna del obstáculo: "))
            mapa_objeto.agregar_obstaculo(fila, columna)

    respuesta = input("¿Desea quitar algún obstáculo? (s/n): ").lower()
    if respuesta == 's':
        num_obstaculos = int(input("¿Cuántos obstáculos desea quitar? "))
        for _ in range(num_obstaculos):
            fila = int(input("Ingrese la fila del obstáculo a quitar: "))
            columna = int(input("Ingrese la columna del obstáculo a quitar: "))
            mapa_objeto.quitar_obstaculo(fila, columna)

    inicio = mapa_objeto.solicitar_coordenadas("inicio")
    fin = mapa_objeto.solicitar_coordenadas("fin")

    camino = ruta_calculadora.a_estrella(inicio, fin)

    print("\nMapa con la ruta más corta encontrada:")
    mapa_objeto.visualizar(camino)

if __name__ == "__main__":
    main()
