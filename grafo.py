import random
class Grafo(object):

    def __init__(self, es_dirigido):
        self.es_dirigido = es_dirigido
        self.vertices = {}
        self.vertices_participantes = set()

    def agregar_vertice(self, v):
        self.vertices_participantes.add(v)
        self.vertices[v] = {}
    
    def borrar_vertice(self, v):
        self.vertices.pop(v)
        self.vertices_participantes.remove(v)
    
    def agregar_arista(self, v, w, peso):
        if not self.es_dirigido:
            self.vertices[v][w] = peso
            self.vertices[w][v] = peso
        else:
            self.vertices[v][w] = peso
    
    def borrar_arista(self, v, w):
        if self.es_dirigido:
            self.vertices[v].pop(w)
        else:
            self.vertices[v].pop(w)
            self.vertices[w].pop(v)
    
    def estan_unidos(self, v, w):
        if v in self.vertices[w]:
            return True
        if w in self.vertices[v]:
            return True
        return False

    def peso_arista(self, v, w):
        if self.estan_unidos(v, w):
            return self.vertices[v][w]
    
    def obtener_vertices(self):
        return self.vertices_participantes
    
    def vertice_aleatorio(self):
        return random.choice(list(self.obtener_vertices()))

    def adyacentes(self, v):
        return self.vertices[v]