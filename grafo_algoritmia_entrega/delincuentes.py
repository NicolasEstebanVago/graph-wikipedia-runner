from funciones_grafo import *
from grafo import *
from collections import deque

# MINIMOS SEGUIMIENTOS
def camino_minimo_bfs(grafo, origen, destino):

    padre, visitados, distancia = recorrido_bfs(grafo, origen)

    if destino not in visitados: #se recorrio todo el grafo(o al menos a componente conexa a la que pertenece el origen) y no se encontro el destino
        return []
    
    #si el destino si existe, tengo que ver cual es su padre y el padre de padre... sucesivamente hasta llegar a origen
    stack = []
    actual = destino
    while actual != origen:
        stack.append(actual)
        actual = padre[actual]
    stack.append(actual)

    camino = []
    while len(stack) != 0:
        camino.append(stack.pop())
    
    return camino

# DELINCUENTE MAS IMPORTANTES
def calcular_delincuentes_importantes(grafo):
    return page_rank(grafo)

# PERSECUCION RAPIDA
def persecucion_rapida(grafo, lista_delincuentes, top_k_delincuentes):

    #primer deberia ver cuales son los k delincuentes mas importantes...

    caminos_delincuentes = {}

    #una vez tengo una lista ordenada con los top k delincuets mas imprtantes, voy viendo para cada infiltrado,
    #cual es su camino mas corto a alguo de los top k
    for v in lista_delincuentes: #infiltrados
        for top_delicunte in top_k_delincuentes:
            camino_minimo = camino_minimo_bfs(grafo, v, top_delicunte)
            if v not in caminos_delincuentes:
                caminos_delincuentes[v] = camino_minimo
            if len(camino_minimo) < len(caminos_delincuentes[v]):
                caminos_delincuentes[v] = camino_minimo
    
    #print(caminos_delincuentes)
    #deberiaordenarlo por longitudes de las claves
    ordenadox = sorted(caminos_delincuentes.items(), key=lambda x: len(x[1]))

    #print(ordenadox)
    
    candidato = ordenadox[0][1]

    pos = 1
    while pos < (len(ordenadox)-1) and len(ordenadox[pos][1]) == len(candidato):
        if top_k_delincuentes.index(ordenadox[pos][1][-1]) < top_k_delincuentes.index(candidato[-1]):
            candidato = ordenadox[pos][1]
        pos += 1

    return candidato

# COMUNIDADES
def comunidades(grafo):
    labels = {}
    
    label_propagation(grafo, labels)
    comunidades = {}
    for l in labels:
        if labels[l] in comunidades:
            comunidades[labels[l]].append(l)
        else:
            comunidades[labels[l]] = [l]

    return comunidades

# DIVULGACION DE RUMOR
def divugacion_rumor_bfs(grafo, delincuente, n):

    padre, visitados, orden = recorrido_bfs(grafo, delincuente)
    lista_rumor = []
    for v in orden:
        if orden[v] <= n and orden[v] > 0:
            lista_rumor.append(v)

    return lista_rumor

# CICLO DE LARGO N
def divulgar_ciclo(grafo, delincuente, n):
    return ciclo_largo_n(grafo, delincuente, n)

# COMPONENTES FUERTEMENTE CONEXAS
def cfc(grafo):
    return componentes_fuertemente_conexas(grafo)