from grafo import Grafo
from grafo import *
import requests
from bs4 import BeautifulSoup
from collections import deque

from funciones_grafo import camino_minimo_bfs

ORIGIN = "/wiki/Nueva_York"
DESTINY = "/wiki/Max_Verstappen"

def filtro_enlace(enlace):

    if("wiki" in enlace and "Anexo" not in enlace and "https" not in enlace and "Usuario" not in enlace and "Especial" not in enlace 
    and "#" not in enlace and "index.php" not in enlace and "Archivo" not in enlace and ".org" not in enlace and "Wikipedia" not in enlace
    and "Categor%C3%ADa" not in enlace and ".jpg" not in enlace):
        return True

    return False

def obtener_enlaces_articulo(link): # Agregar a la funcion los filtros... eliminar links que sean inutiles para la red!!!
    #opcion... limitar a unicamente los primeros 150 enlaces... los demas dejarlos... se hace muy grande el grafo y demasiado extensa la carga de la red...

    response = requests.get(link) # Request al servidor de wikipedia, se obtiene la HTTP RESPONSE de dicha rquest...

    soup = BeautifulSoup(response.text, 'html.parser') # Parsing el texto HTML de la response...

    lista_ = (soup.find_all('a')) # Se obtienen todos los elementos del codigo HTML que cumplan con label "a"

    lista_final = []
    for link in lista_:
        
        enlace = str(link.get('href'))

        if filtro_enlace(enlace):
            lista_final.append(enlace) # Se obtiene el link de cada label...

    return lista_final # MALA SOLUCION PARA BAJAR TIEMPO DE RESOLUCION slicear la lista de enlaces de un articulo...

def cargar_grafo(grafo : Grafo, origen): # ERROR

    enlaces = obtener_enlaces_articulo("https://es.wikipedia.org" + origen)

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