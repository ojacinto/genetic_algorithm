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

class Main(object):

    def __init__(self):
        '''A genetic algorithm to Travelling Salesman Problem.

        '''
        print ('''*******************Genetic algorithm********************
               Author: Oraldo Jacinto Simon
               ''')

        list_edges_weight = []
        fichero = open("VLSI.txt", 'r')
        lines = fichero.read()
        lines = lines.rsplit('\n')
        list_edges_weight = [edge.split(' ') for edge in lines if edge !='']
        fichero.close()
        obj_graph = Graph()
        graph = obj_graph.add_from_edge(list_edges_weight, directed=False)
        pop_size = 100
        epochs = 10000
        # Can be cities or nodes
        elite = 80
        obj_genetic = Genetic(pop_size, epochs, graph, elite,
                              rate_mutation=0.5, selection_type='tourney_probabilistic')
        obj_genetic.run()
Main()
