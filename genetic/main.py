#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright 2018(c). All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
# Author: Ing. Oraldo Jacinto Simon
from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        absolute_import as _py3_abs_import)

from collections import deque
from graph import Graph
from genetic import Genetic
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pylab

class Main(object):

    def __init__(self):
        '''A genetic algorithm to Travelling Salesman Problem.

        '''
        print ('''*******************Genetic algorithm*********************
              * Authors: Oraldo Jacinto Simon
              *          Marco Emanuel Casavantes Moreno
              * ***********************************************************
               ''')

        obj_graph = Graph()
        fichero = open("cities/five_d.txt", 'r')
        matrix_adjacency = np.loadtxt(fichero)
        for i, row in enumerate(matrix_adjacency):
            for j, item in enumerate(row):
                graph = obj_graph.addEdge(i+1, j+1, item, directed=False)
        fichero.close()
        pop_size = 100
        epochs = 80
        # Can be cities or nodes
        elite = 80
        obj_genetic = Genetic(pop_size, epochs, graph, elite,
                              rate_mutation=0.5, selection_type='tourney_probabilistic')
        path = obj_genetic.run()

        #Draw graph
        G = nx.DiGraph()
        for vertex in graph.__iter__():
            for v, w in vertex.adjacency.items():
                G.add_edge(str(vertex.id), str(v), weight=w)

        val_map = {'A': 1.0, 'D': 0.5714285714285714, 'H': 0.0}

        values = [val_map.get(node, 0.45) for node in G.nodes()]
        node_labels = {n:str(n) for n in G.nodes()}
        edge_labels=dict([((u,v,),d['weight'])
                          for u,v,d in G.edges(data=True)])
        red_edges = [(str(e), str(path[index+1])) for index, e in enumerate(path[:-1])]
        edge_colors = ['gray' if not edge in red_edges else 'red' for edge in G.edges()]
        pos=nx.spring_layout(G)
        nx.draw_networkx_labels (G, pos, labels=node_labels)
        nx.draw_networkx_edge_labels(G,pos, edge_labels=edge_labels)
        nx.draw(G,pos, node_color = values, node_size=1500,edge_color=edge_colors,edge_cmap=plt.cm.Reds)
        pylab.show()
        #G.add_edges_from()

Main()
