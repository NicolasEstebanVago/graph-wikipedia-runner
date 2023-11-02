from grafo import Grafo
from grafo import *
import requests
from bs4 import BeautifulSoup
from collections import deque
from funciones_grafo import camino_minimo_bfs

MAIN_URL = "https://es.wikipedia.org"
ORIGIN = "/wiki/Nueva_York"
DESTINY = "/wiki/Max_Verstappen"

def obtener_enlaces_articulo(link): 

    response = requests.get(link) 

    soup = BeautifulSoup(response.text, 'html.parser') 

    lista_ = (soup.find_all('a')) 

    lista_final = []
    for link in lista_:
        
        enlace = str(link.get('href'))

        if filtro_enlace(enlace):
            lista_final.append(enlace)

    return lista_final 

def cargar_grafo(grafo : Grafo, origen): # ERROR

    enlaces = obtener_enlaces_articulo(MAIN_URL + origen)

    for enlace in enlaces:
        grafo.agregar_vertice(enlace)
    
    for enlace in enlaces:
        grafo.agregar_arista(origen, enlace, 1)
        
    return grafo

def carga_bfs(grafo : Grafo, origen):

    # archivo = open("output.txt", "w")

    visitados = set()
    visitados.add(origen)

    cola = deque()
    cola.append(origen) # O(1)

    while cola:
        vertice = cola.popleft()

        print("ANALIZANDO NODO ... " + vertice)
        grafo = cargar_grafo(grafo, vertice)
        
        # una vez que exsita el destino en la red ya no es necesario seguir cargando el grafo...
        if( DESTINY in grafo.obtener_vertices()):
            print("SE LLEGO AL DESTINO...")

    return (grafo)

def main():

    # Creo la estructura de datos para representa la red de conecciones entre las distintos wiki articulos
    grafo_web_conecctions = Grafo(es_dirigido=False)
    
    grafo_web_conecctions.agregar_vertice(ORIGIN) # Se agrega el  vertice origen

    # Se carga el grafo cuyos vertices son los articulos y aristas indican la presencia de un enlace al otro articulo
    carga_bfs(grafo=grafo_web_conecctions, origen=ORIGIN)

    # Resolucion del camino minimo
    print(camino_minimo_bfs(grafo=grafo_web_conecctions, origen=ORIGIN, destino=DESTINY))

if __name__ == "__main__":
    main()