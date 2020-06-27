import dimod
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from board24 import Board
import morris
import pygame
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys

game = morris.GameState()

num_spots = 24
max_checkers = 18
our = np.zeros(num_spots,dtype=int)
enemy = np.zeros(num_spots,dtype=int)
previous_enemy = np.zeros(num_spots,dtype=int)
h_const = 100
j_const = 1
constraint_const = 3
mill_constant = 0
anti_mill_constant = 1.7


b = Board()
# FOR BOARD MARKERS:
# OURS IS 1
# ENEMY IS 2
# FREE IS 0

stopped = False
while not stopped:
    num_checkers_on_board = np.sum(our) + np.sum(enemy)
    if num_checkers_on_board >= max_checkers:
        print("Going into Phase 2")
        sys.exit('Switch to phase 2')
        #phase_2(enemy,our,previous_enemy)
    num_checker_constraint = - num_spots + num_checkers_on_board + 2
    c = num_checker_constraint # just to simplify
    linear = {}
    for i in range(num_spots):
        if our[i] == 1:
            linear[i+1] = h_const
        elif enemy[i] == 1:
            linear[i+1] = -h_const
        else:
            linear[i+1] = 0
        #print(linear)

    # Adding quadratic terms for constraint
    quadratic = {}
    for i in range(1,num_spots):
        for j in range(i+1,num_spots+1):
            quadratic[(i,j)] = 2*constraint_const
    # Update linear for constraint
    for i in range(1,num_spots+1):
        linear[i] -= 2*c*constraint_const

    offset = (c**2+num_spots)*constraint_const # Think about sign
    # Set interactions, i.e. update quadratic
    for i in range(num_spots):
        if enemy[i]:
            idx = b.get_rowcol_idx(i)
            for j in idx:
                if i < j:
                    quadratic[(i+1,j+1)] += -j_const
                else:
                    quadratic[(j+1,i+1)] += -j_const

    # update quadratic for mill energy decrease
    for i in range(0,num_spots):
        if enemy[i] == 0:
            continue
        idx = b.get_rowcol_idx(i)
        for j in idx:
            if enemy[j]:
                if i < j:
                    quadratic[(i+1,j+1)] -= 2*mill_constant
                else:
                    quadratic[(j+1,i+1)] -= 2*mill_constant


    offset -= (2*num_spots)*mill_constant

    # update quadratic for mill energy increase
    for i in range(0,num_spots):
        if our[i] == 0:
            continue
        idx = b.get_rowcol_idx(i)
        for j in idx:
                if i < j:
                    quadratic[(i+1,j+1)] += 2*anti_mill_constant
                else:
                    quadratic[(j+1,i+1)] += 2*anti_mill_constant


    offset += (2*num_spots)*anti_mill_constant

    vartype = dimod.SPIN

    bqm = dimod.BinaryQuadraticModel(
        linear,
        quadratic,
        offset,
        vartype)


    #graph_bqm = bqm.to_networkx_graph()
    #nx.draw_networkx(graph_bqm, with_labels=False)
    #values = [graph_bqm.get_edge_data(edge[0],edge[1],default=0) for edge in graph_bqm.edges()]
    #print(values)
    #plt.savefig('nx_plot.png',dpi=200)

    sampler = dimod.SimulatedAnnealingSampler()
    sample_set = sampler.sample(bqm,num_reads=10)
    #sampler = dimod.ExactSolver()
    #sample_set = sampler.sample(bqm)
    next_state = sample_set.samples()[0] # Maybe do sampling instead??

    for i in range(1,num_spots+1):
        if next_state[i]==1:
            enemy[i-1]=1
            b.place_marker(pos=i-1,player_num=2)
            game.board = b.convert_to_gui_array()
            b.check_mill()
    print(b)
    # Find the move
    move = enemy - previous_enemy
    for i in range(num_spots):
        if move[i]:
            move_to = i+1
            print("Moved to: " + str(move_to))
    previous_enemy = list(enemy)

   # Choose our input
    our_pos = int(input('Give position to place marker (1-24): '))
    our[our_pos-1] = 1
    b.place_marker(pos=our_pos-1,player_num=1)
    game.board = b.convert_to_gui_array()
    b.check_mill()


    #stopped = True




############################3
def phase_2(enemy,our,previous_enemy):
    h_const_2          = 2
    num_checkers_on_board = np.sum(our) + np.sum(enemy)
    num_checker_constraint = - num_spots + num_checkers_on_board
    c                  = num_checker_constraint
    constraint_const_2 = 40
    j_const_2          = 2
    mill_constant_2    = 1
    linear = {}
    for i in range(num_spots):
        if our[i] == 1:
            linear[i+1] = h_const_2
        elif enemy[i] == 1:
            linear[i+1] = -h_const_2
        else:
            linear[i+1] = 0
        #print(linear)
    # Adding quadratic terms for constraint
    quadratic = {}
    for i in range(1,num_spots):
        for j in range(i+1,num_spots+1):
            quadratic[(i,j)] = 2*constraint_const_2
    # Update linear for constraint
    for i in range(1,num_spots+1):
        linear[i] -= 2*c*constraint_const_2

    offset = (c**2+num_spots)*constraint_const # Think about sign
    # Set interactions, i.e. update quadratic
    for i in range(num_spots):
        if enemy[i]:
            idx = b.get_rowcol_idx(i)
            for j in idx:
                if i < j:
                    quadratic[(i+1,j+1)] += -j_const_2
                else:
                    quadratic[(j+1,i+1)] += -j_const_2

    # update quadratic for mill energy decrease
    for i in range(0,num_spots):
        if enemy[i] == 0:
            continue
        idx = b.get_rowcol_idx(i)
        for j in idx:
            if enemy[j]:
                if i < j:
                    quadratic[(i+1,j+1)] -= 2*mill_constant_2
                else:
                    quadratic[(j+1,i+1)] -= 2*mill_constant_2
            else:
                if i < j:
                    quadratic[(i+1,j+1)] += 2*mill_constant_2
                else:
                    quadratic[(j+1,i+1)] += 2*mill_constant_2


    offset -= (2*num_spots)*mill_constant_2


    vartype = dimod.SPIN

    bqm = dimod.BinaryQuadraticModel(
        linear,
        quadratic,
        offset,
        vartype)
    sampler = dimod.SimulatedAnnealingSampler()
    sample_set = sampler.sample(bqm,num_reads=10)
    #sampler = dimod.ExactSolver()
    #sample_set = sampler.sample(bqm)
    next_state = sample_set.samples()[0] # Maybe do sampling instead??
    #print(next_state)
    #print("Previous: " + str(previous_enemy))
    #print("New: " + str(enemy))
    #print(quadratic)
    for i in range(1,num_spots+1):
        if next_state[i]==1:
            enemy[i-1]=1
            b.place_marker(pos=i-1,player_num=2)
    # Find the move
    move = enemy - previous_enemy
    print(move)
    for i in range(num_spots):
        if move[i]:
            move_to = i+1
            print("Moved to: " + str(move_to))
    previous_enemy = list(enemy)

    print(b)
    print(sample_set)
  # Choose our input
    our_pos = int(input('Give position to place marker (1-24): '))
    our[our_pos-1] = 1
    b.place_marker(pos=our_pos-1,player_num=1)
    return
###############################33
