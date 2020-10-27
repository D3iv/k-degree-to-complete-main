from random import randint
import numpy as np
import collections
from numpy import array
import networkx as nx
import sys
import os


def compute_I(d,i,j):
    cost=0
    for index in range(i,j+1):
        cost+=d[i]-d[index]
        #print("iterazione di compute {}".format(cost))
    return cost

def c_merge(d, d1, i, k):
    #print("Costo di d1-d(k): {}".format(d1-d[i]))
    #print("-----Iterazioni di Cmerge()")
    return ((d1 - d[k])+compute_I(d,i+1,k+i))

def c_new(d, i, k):
    #print("-----Iterazioni di Cnew()")
    return compute_I(d,i,i+k-1)

def greedy_rec_algorithm(array_degrees, k_degree, pos_init, extension):
    return

def dp_graph_anonymization(k_degree):
    # Iniziamo prendendo il nodo con il numero di connessioni più alto
    d1 = array_degrees_greedy[1]
    d_cap = np.empty(shape=k_degree,dtype='int16')
    # Creiamo l'array d^ inserendo il primo valore di array_degrees, k volte
    for i in range(0, k_degree):
        d_cap[i]=d1

    print("dimensione dell'array : {}".format(array_degrees_greedy.size))
    index = k_degree
    # Applicazione Greedy Algorithm
    while index < array_degrees_greedy.size:
        if (array_degrees.size - index >= k_degree):
            if (c_merge(array_degrees_greedy, d1, index, k_degree) < c_new(array_degrees_greedy, index, k_degree)):
                d_cap= np.append(d_cap,array_degrees_greedy[index-1])
                #print(d_cap)
                index+=1
            else:
                v_to_append = np.empty(shape=k_degree,dtype='int16')
                for i in range(0,k_degree):
                    v_to_append[i] = array_degrees_greedy[index]
                d_cap = np.append(d_cap, v_to_append)
                #print(d_cap)
                index+=k_degree
                #print("valore dell'indice: {}".format(index))
        else:
            i = index-k_degree
            d_cap = np.append(d_cap,array_degrees_greedy[i])
            index+=1


    #print(d_cap)
    return d_cap

def construct_graph():
    G_anonymous = nx.Graph()
    v= randint(1,d_anonimous.size-1)
    # Array dei nodi-->archi
    v_dv = np.empty(shape=0,dtype='int16')
    print("Vertice casuale: {}".format(v))
    if d_anonimous[v] == 0:
        v= randint(1,d_anonimous.size-1)

    if(d_anonimous.size % 2 != 0):
        print("This graph can't be anonymized, dim is odd")

    while(True):
        #Controllo che non ci sia un nodo con valore negativo
        all_positive = np.all(d_anonimous >=0)
        if (all_positive == False):
            print("This graph can't be anonymized, negative value of edges")
            return;

        # Controllo che i nodi abbiano tutti valore 0
        all_zeros = np.all(d_anonimous == 0)
        if all_zeros:
            print("Graph building complete")
            return G_anonymous;


        #Costruisco il vettore degli archi per il nodo v
        for i in range(1,v_dv.size,1):
            if(i!=v):
                v_dv[i-1]=i
                print(v_dv)


        #Selezioniamo i primi d_anonimous[v] vertici con grado maggiore
        #e costruiamo gli archi
        for i in range(0,d_anonimous[v]):
            if (i != v):
                if node_to_add not in G:
                    G.add_node(node_to_add)
                    print("Aggiunto nodo : {}".format(node_to_add))

                G_anonymous.add_edge(i,v)
                d_anonimous[i]-1

        # Il vertice selezionato in modo casuale viene "tagliato" dal grafo
        d_anonimous[v] = 0

    return G_anonymous

if __name__ == "__main__":
    k_degree = int(sys.argv[1])
    file_graph = sys.argv[2]
    G = nx.Graph()
    
    if os.path.exists(file_graph): 
        # if file exist
        with open(file_graph) as f:
            content = f.readlines()
        # read each line
        content = [x.strip() for x in content]
        for line in content:
            # split name inside each line
            names = line.split(",")
            start_node = names[0]
            if start_node not in G:
                G.add_node(start_node)
            for index in range(1, len(names)):
                node_to_add = names[index]
                if node_to_add not in G:
                    G.add_node(node_to_add)
                G.add_edge(start_node, node_to_add)

    # Degree arrays preparation
    d = [x[1] for x in G.degree()]
    array_index = np.argsort(d)[::-1]
    array_degrees = np.sort(d)[::-1]
    #print("Array of degrees (d) : {}".format(d))
    #print("Array of degrees sorted (array_degrees) : {}".format(array_degrees))
    array_degrees_greedy = array_degrees
    #Anonimizzazione del vettore d
    d_anonimous = dp_graph_anonymization(k_degree)
    #print("Array of degrees anonymized(d^) : {}".format(d_anonimous))
    #Costruiamo il grafo anonimo
    G_anonymous = construct_graph()
    #print("Array of degrees anonymized(G_anonymous) : {}".format(G_anonymous))





