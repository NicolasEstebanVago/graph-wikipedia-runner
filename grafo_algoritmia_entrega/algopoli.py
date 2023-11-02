#!/usr/bin/python3
from grafo import *
from funciones_grafo import *
from delincuentes import *
import sys

# Archivo main entrega

def main():

    archivo = sys.argv[1] # obtengo el archivo que se pasa por parametro...

    grafo = Grafo(True) # creo un grafo...
    grafo = cargar_grafo(grafo, archivo) # cargo el grafo con el archivo pasado por parametro...

    rankings_page_rank = None #aca se guarda el ranking de delincuentes mas importantes

    for linea in sys.stdin:

        linea_dividida = linea.rstrip('\n').split()
        comando = linea_dividida[0]

        if (comando == "min_seguimientos"):
            camino = camino_minimo_bfs(grafo, int(linea_dividida[1]), int(linea_dividida[2]))
            if len(camino) == 0:
                print("Seguimiento imposible")
            else:
                for i in range(len(camino)-1):
                    print(str(camino[i]), end=" -> ")
                print(camino[-1])

        if (comando =="mas_imp"):
            if rankings_page_rank == None:#Caso que sea la primera vez que se calcula. Si ya habia sido calculado, se vuelve a usar
                rankings_page_rank = calcular_delincuentes_importantes(grafo)
            k = int(linea_dividida[1])
            for v in range(k-1):
                print(str(rankings_page_rank[v]) + ", ", end="")
            print(v)
        
        if(comando == "persecucion"):

            delincuentes = linea_dividida[1].split(',')
            for i in range(len(delincuentes)):
                delincuentes[i] = int(delincuentes[i])
            
            if rankings_page_rank == None:
                rankings_page_rank = calcular_delincuentes_importantes(grafo)

            persecucion = persecucion_rapida(grafo, delincuentes, rankings_page_rank[:int(linea_dividida[2])])
            for i in range(len(persecucion)-1):
                print(str(persecucion[i]), end=" -> ")
            print(persecucion[-1])
        
        if(comando == "comunidades"):
            dic_comunidades = comunidades(grafo)
            for c in dic_comunidades:
                largo = len(dic_comunidades[c])
                cont = 0 
                if len(dic_comunidades[c]) >= int(linea_dividida[1]):
                    print(f"Comunidad {c}:", end="")
                    for i in dic_comunidades[c]:
                        cont += 1
                        if cont == largo:
                            print(f" {i}")
                        else:
                            print(f" {i},", end="")

        if(comando == "divulgar"):
            llegados = divugacion_rumor_bfs(grafo, int(linea_dividida[1]), int(linea_dividida[2]))
            for v in llegados[:len(llegados)-1]:
                print(str(v) + ", ", end='')
            print(llegados[-1])
        
        if(comando == "divulgar_ciclo"):
            lista_ciclo = divulgar_ciclo(grafo, int(linea_dividida[1]), int(linea_dividida[2]))
            if lista_ciclo:
                largo = len(lista_ciclo)
                for d in range(largo):
                    if d+1 == largo:
                        print(lista_ciclo[d])
                        break
                    print(lista_ciclo[d], end=" -> ")
            else:
                print("No se encontro recorrido")

        if(comando == "cfc"):
            cfcs = cfc(grafo)
            cont_c = 1
            for cfc_ in cfcs:
                largo = len(cfc_)
                cont  = 0
                print(f"CFC {cont_c}:", end="")
                for c in cfc_:
                    cont += 1
                    if cont == largo:
                        print(f" {c}")
                    else:
                        print(f" {c},", end="")
                cont_c +=1

if __name__ == "__main__":
    main()