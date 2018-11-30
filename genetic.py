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

import random, operator
aleatory = lambda a, b : random.randint(a, b)


class Genetic(object):
    '''This class implements all the methods required to apply genetic algorithm
    to Travelling Salesman Problem.

    '''

    def __init__(self, pop_size, epochs, graph, elite, rate_mutation, selection_type):
        self.pop_size = pop_size
        self.epochs = epochs
        self.graph = graph
        self.nodes = graph.list_vertices
        self.count_nodes = graph.count_vertices
        self.elite = elite
        self.rate_mutation = rate_mutation
        self.selection_type = selection_type
        self.population = []
        self.routes_cost = []
        list_nodes = [e for e in self.nodes.keys()]
        for nroute in range(pop_size):
            self.population.append(random.sample(list_nodes, self.count_nodes))


    def fitness(self, route):
        '''Calculate the cost given a route

        '''
        cost = 0
        for index in range(len(route)-1):
            cost += self.graph.get_vertex(route[index]).get_weight(route[index+1])
        cost += self.graph.get_vertex(route[len(route)-1]).get_weight(route[0])
        return cost

    def calculate_routes(self, population):
        '''Calculate the fitness for each route's population and return a
        dict()

        '''
        result_fistness, minimun = {}, {}
        for index, route in enumerate(population[:-1]):
            cost = self.fitness(route)
            next_cost = self.fitness(population[index+1])
            result_fistness[index] = cost
            if next_cost > cost :
                 minimun['cost'] = cost
                 minimun['index'] = index
            else:
                minimun['cost'] = next_cost
                minimun['index'] = index+1
            index += 1
        result_fistness[index] = next_cost
        return result_fistness, minimun

    def selection(self, pop_size, population, routes_cost):
        '''Select the elite in route's population and applies the selection method per
        tournament specified by parameter. If the method of selection is not
        specified applies deterministic tournament by default.

        `tourney_deterministic`: a number of individuals is randomly selected
        (p = 2 is usually chosen). From among the individuals, the most
        suitable options are selected to pass to the next generation.

        `tourney_probabilistic`: only differs in the selection step of the
        winner of the tournament. Instead of always choosing the best one, a
        random number of the interval [0..1] is generated, if it is greater
        than a parameter p (fixed for the whole evolutionary process) the
        highest individual is selected and otherwise the least apt. Generally
        p takes values ​​in the range (0.5 - 1).

        '''
        p =  0.6
        selection_result = []
        method = self.selection_type
        # Select two parents
        for j in range(0, 2):
            index_a = aleatory(0, pop_size-1)
            index_b = aleatory(0, pop_size-1)
            subject_a = population[index_a]
            subject_b = population[index_b]
            cost_a = routes_cost[index_a]
            cost_b = routes_cost[index_b]
            winner = subject_a if cost_a <= cost_b else subject_b
            loser = subject_a if cost_a >= cost_b else subject_b
            if method == 'tourney_deterministic' or method is None:
                selection_result.append(winner)
            elif method == 'tourney_probabilistic':
                aleatory_value = aleatory(0, 10) / 10
                selection_result.append(winner) if aleatory_value >= p else selection_result.append(loser)
        return selection_result

    def mutation(self, childs):
        '''Mutate the chromosomes(routes) by performing a random exchange of genes.

        '''
        for g in range(self.count_nodes):
            mutate = aleatory(0, 10) / 10
            for chi in range(0,2):
                aleatory_value = aleatory(0, self.count_nodes-1)
                if mutate > self.rate_mutation:
                    # Change values in childs
                    temp1 = childs[chi][g]
                    childs[chi][g] = childs[chi][aleatory_value]
                    childs[chi][aleatory_value] = temp1
        return childs


    def get_best_insertion_pos(self, individual, vertex):
        adjacency = self.graph.get_matrix_adjacency()
        count = len(individual)
        value = adjacency[vertex-1][individual[0]-1] + adjacency[vertex-1][individual[count-1]-1]
        best_pos = 0 if value > 0 else None
        min_value = value if value > 0 else 2**10
        for pos in range(count):
            if pos + 1 == count:
                # last element
                pass
            else:
                pos_value = adjacency[individual[pos]-1][vertex-1] + \
                            adjacency[vertex-1][individual[pos+1]-1]
                if pos_value > 0:
                    if pos_value < min_value:
                        best_pos = pos + 1
                        min_value = pos_value
        return best_pos

    def _cross_a_using_b(self, parents_selection):


        part2_a, part2_b = [], []

        _chA = parents_selection[0]
        _chB = parents_selection[0]
        aleatory_value = aleatory(2, len(_chA)-1) # assuming the same length for both

        child_a = _chA[0:aleatory_value]
        subs = list(set(_chB) - set(child_a))
        while subs:
            pos = self.get_best_insertion_pos(child_a, subs[-1])
            if pos is None:
                child_a.append(subs[-1])
            else:
                child_a.insert(pos, subs[-1])
            subs.pop()
        return child_a

    def _new_crossover(self, parents_selection):
        swap = lambda x: (x[1], x[0])
        child_a = self._cross_a_using_b(parents_selection)
        child_b = self._cross_a_using_b(swap(parents_selection))
        return [child_a, child_b]

    def crossover(self, parents_selection, pop_size, mode='simple'):
        '''Crossing of 1 point

        Selected two individuals cut their chromosomes by a randomly selected
        point to generate two different segments in each of them: the head and
        tail. The tails are exchanged between the two individuals to generate the new
        descendants. In this way, both descendants.

        '''
        if mode != 'simple':
            return self._new_crossover(parents_selection)
        part2_a, part2_b = [], []
        aleatory_value = aleatory(0, pop_size)
        child_a = parents_selection[0][0:aleatory_value]
        child_b = parents_selection[1][0:aleatory_value]
        [part2_a.append(n) for n in parents_selection[1][:] if n not in child_a]
        [part2_b.append(l) for l in parents_selection[0][:] if l not in child_b]
        child_a.extend(part2_a)
        child_b.extend(part2_b)
        return [child_a, child_b]

    def reinsertion(self, new_childs, childs_cost, routes_cost):
        '''Make a tournament with each of the new children vs. the individuals
        of the population

        If the child wins is inserted into the population

        '''
        for child, cost in childs_cost:
            aleatory_value = aleatory(0, self.pop_size-1)
            if cost < routes_cost[aleatory_value]:
                self.population[aleatory_value] = new_childs[child]
                self.routes_cost[aleatory_value] = cost


    def next_generation(self, population, elite):
        '''Compute the next generation

        '''
        new_childs = []
        routes_cost, minimun_pop = self.calculate_routes(population)
        self.routes_cost = routes_cost
        pop_size = int(elite/100 * len(population))
        for e in range(0, self.count_nodes):
            # Take a representative (%) size of the elite of the population
            parents_selection = self.selection(pop_size, population, routes_cost)
            # In each crossing, two children are born
            childs = self.crossover(parents_selection, pop_size, mode='')
            childs_mutated = self.mutation(childs)
            [new_childs.append(child) for child in childs_mutated]
        childs_cost, minimun_child = self.calculate_routes(new_childs)
        childs_cost = sorted(childs_cost.items(), key = operator.itemgetter(1))
        self.reinsertion(new_childs, childs_cost, routes_cost)
        routes_cost, mini = self.calculate_routes(population)
        return mini


    def run(self):
        '''Run the genetic algorithm

        '''
        for n in range(self.epochs):
            mini = self.next_generation(self.population, self.elite)
            print ("Epochs %s, cost: %i" % ((n+1), mini['cost']))
        print ("Result: %s" % str(self.population[mini['index']]))
        return self.population[mini['index']]
