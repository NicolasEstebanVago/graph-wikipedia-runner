#Estas funciones son genericas para cualquier grafo. No conocen a Delincuentes...
from collections import deque
import random

def cargar_grafo(grafo, archivo): #recibe un archivo .tsv...

    archivo = open(archivo, "r")
    linea = archivo.readline()
    linea.replace("\n", "")

    while linea:
        vertices = linea.split('\t')

        if int(vertices[0]) not in grafo.obtener_vertices(): #ACA HAY UN ON, ahora es O(1)
            grafo.agregar_vertice(int(vertices[0]))
        if int(vertices[1]) not in grafo.obtener_vertices():
            grafo.agregar_vertice(int(vertices[1]))
        

        grafo.agregar_arista(int(vertices[0]), int(vertices[1]), 1)
        linea = archivo.readline()
        linea.replace("\n", "")

    archivo.close()

    return grafo

def grado_salida(grafo):

    grado_salida={}
    for vertice in grafo.obtener_vertices():
        grado_salida[vertice]=0
    for vertice in grafo.obtener_vertices():
        for ady in grafo.adyacentes(vertice):
            grado_salida[vertice]=grado_salida[vertice]+1
    return grado_salida

def recorrido_bfs(grafo, origen):
    
    orden, padre = {}, {}
    visitados = set()
    
    orden[origen] = 0
    padre[origen] = None
    visitados.add(origen)

    cola = deque()
    cola.append(origen) #O1
    #cola.append(origen)

    while cola:

        v = cola.popleft()#O1
        
        for w in grafo.adyacentes(v):
            if w not in visitados:
                orden[w] = orden[v] + 1
                visitados.add(w)
                padre[w] = v
                cola.append(w)
    
    return padre, visitados, orden

def obtener_vertices_que_apuntan_a(grafo):

    vertices_que_apuntan_a = {} 

    for vertice in grafo.obtener_vertices():
        vertices_que_apuntan_a[vertice] = []
    
    for vertice in grafo.obtener_vertices():
        for w in grafo.adyacentes(vertice):
            vertices_que_apuntan_a[w].append(vertice)
    
    return vertices_que_apuntan_a

#algoritmo label propagation y funcion auxiliar
def max_freq(labels, vertices_adyacentes):
    mas_frecuentes = {}
    for v in vertices_adyacentes:
        if labels[v] in mas_frecuentes:
            mas_frecuentes[labels[v]] += 1
        else:
            mas_frecuentes[labels[v]] = 1
    
    mas_frecuente = None
    for f in mas_frecuentes:
        if not mas_frecuente:
            mas_frecuente = f
        elif mas_frecuentes[f] > mas_frecuentes[mas_frecuente]:
            mas_frecuente = f
    return mas_frecuente

def label_propagation(grafo, labels):
    i = 0
    aleatorio_vertices  = []
    for v in grafo.obtener_vertices():
        aleatorio_vertices.append(v)
        labels[v] = i
        i+=1

    nro_iteraciones = len(grafo.obtener_vertices())//10
    for i in range(nro_iteraciones):
        random.shuffle(aleatorio_vertices)
        for v in aleatorio_vertices:
            labels[v] = max_freq(labels, grafo.adyacentes(v))

# Encontrar ciclo de largo n
def _dfs_ciclo_largo_n(grafo, v, origen, n, visitados, camino_actual):
    visitados.add (v)
    if len(camino_actual) == n:
        if origen in grafo.adyacentes(v):
            return camino_actual + [origen]
        return None
    for w in grafo.adyacentes(v):
        if w in visitados: continue
        solucion = _dfs_ciclo_largo_n(grafo, w, origen, n, visitados, camino_actual + [w])
        if solucion is not None:
            return solucion
    visitados.remove(v)
    return None

def ciclo_largo_n(grafo, origen, n):
    return _dfs_ciclo_largo_n(grafo, origen, origen, n, set(), [origen])

# Obtener Componentes Fuertemente Conexas
def obtener_cfc(grafo, v, visitados, pila, apilados, orden, mas_bajo, cfcs, indice): 
    visitados.add(v)
    pila.append(v)
    apilados.add(v)
    mas_bajo[v] = orden[v]
    for w in grafo.adyacentes(v):
        if w not in visitados:
            orden [w] = indice[0] + 1
            indice[0] += 1
            obtener_cfc(grafo, w, visitados, pila, apilados, orden, mas_bajo, cfcs, indice) 
            mas_bajo[v] = min(mas_bajo[v], mas_bajo[w])
        elif w in apilados:
            mas_bajo[v] = min(mas_bajo[v], orden[w])
    if mas_bajo[v] == orden[v]:
        nueva_cfc = []
        w = pila.pop()
        apilados.remove(w) 
        nueva_cfc.append(w)
        while w != v:
            w = pila.pop()
            apilados.remove(w) 
            nueva_cfc.append(w)
        cfcs.append(nueva_cfc)

def componentes_fuertemente_conexas(grafo):
    visitados = set()
    pila = []
    apilados = set()
    orden = {}
    mas_bajo = {}
    cfcs = []
    v = grafo.vertice_aleatorio()
    indice = [0]
    orden[v] = 0
    obtener_cfc(grafo, v, visitados, pila, apilados, orden, mas_bajo, cfcs, indice)
    return cfcs

def page_rank(grafo):

    #PageRank
    cantidad_vertices = len(grafo.obtener_vertices())
    valor_amortiguacion = 0.85 #damping factor
    score = {} #diccionario para almacenar el puntaje de cada vertice...valor entre 0 y 1...
    valor_default = 1/cantidad_vertices
    
    #diccionario con los vertices del grafo como claves, y como dato, lista con los vertices que lo tienen a este como adyacente
    vertices_que_apuntan_a = obtener_vertices_que_apuntan_a(grafo)
    
    for vertice in grafo.obtener_vertices():
        score[vertice] = valor_default

    for i in range(20):
        for vertice in grafo.obtener_vertices():#A cada vertice, le doy como puntaje: Los puntajes
            #de los vertices que lo tienen a este como adyacente (PR(vj,...,vk)) / Grado de Salida de los mismos
            score[vertice] = valor_default
            for w in vertices_que_apuntan_a[vertice]:
                score[vertice] += score[w]/len(grafo.adyacentes(w)) * valor_amortiguacion
    
    ordenadox = sorted(score.items(), key=lambda x: x[1], reverse=True) # ordeno por score

    lista_vertices_importantes = []
    for i in range(len(ordenadox)):
        lista_vertices_importantes.append(ordenadox[i][0])
    
    return lista_vertices_importantes