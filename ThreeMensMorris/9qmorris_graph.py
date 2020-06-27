import dimod
from dwave.system.samplers import DWaveSampler
import networkx as nx
import dwave_networkx as dnx
from dwave.system.composites import EmbeddingComposite
from board24 import Board
import matplotlib.pyplot as plt
import minorminer
import numpy as np
import sys

num_spots = 24
max_checkers = 18
our = np.zeros(num_spots,dtype=int)
enemy = np.zeros(num_spots,dtype=int)
previous_enemy = np.zeros(num_spots,dtype=int)
h_const = 100
j_const = 1
constraint_const = 3
mill_constant = 0.1
anti_mill_constant = 2

H = nx.Graph()
H.add_nodes_from(np.arange(num_spots))
H.add_edges_from([(0,1),(1,2),(3,4),(4,5),(6,7),(7,8),(9,10),(10,11),(12,13),(13,14),(15,16),(16,17),
                    (18,19),(19,20),(21,22),(22,23),(0,9),(9,21),(3,10),(10,18),(6,11),(11,15),(1,4),(4,7),
                    (16,19),(19,22),(8,12),(12,17),(5,13),(13,20),(2,14),(14,23)])
#pos=dnx.chimera_layout(H)
plt.ion()
connectivity_structure =dnx.chimera_graph(3, 3)
embeded_graph = minorminer.find_embedding(H.edges(),connectivity_structure.edges())
dnx.draw_chimera_embedding(connectivity_structure,embeded_graph)
#dnx.draw_chimera(G)
#dnx.draw_chimera(H, node_color='b', node_shape='*', style='dashed', edge_color='b', width=3)
plt.savefig('plot.png',dpi=200)
plt.close()
nx.draw_networkx(H, with_labels=False)
plt.savefig('nx_plot.png',dpi=200)
sys.exit()
b = Board()
# FOR BOARD MARKERS:
# OURS IS 1
# ENEMY IS 2
# FREE IS 0



stopped = False
while not stopped:
    num_checkers_on_board = np.sum(our) + np.sum(enemy)
    if num_checkers_on_board >= max_checkers:

        sys.exit('Switch to phase 2')

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
            else:
                if i < j:
                    quadratic[(i+1,j+1)] += 2*mill_constant
                else:
                    quadratic[(j+1,i+1)] += 2*mill_constant


    offset -= (2*num_spots)*mill_constant

    # update quadratic for mill energy decrease

    for i in range(0,num_spots):
        if our[i] == 0:
            continue
        idx = b.get_rowcol_idx(i)
        for j in idx:
            if our[j] == 1:
                if i < j:
                    quadratic[(i+1,j+1)] += 2*anti_mill_constant
                else:
                    quadratic[(j+1,i+1)] += 2*anti_mill_constant
            else:
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
    sampler = dimod.SimulatedAnnealingSampler()
    sample_set = sampler.sample(bqm,num_reads=10)
    #sampler = dimod.ExactSolver()
    #sample_set = sampler.sample(bqm)
    next_state = sample_set.samples()[0] # Maybe do sampling instead??

    for i in range(1,num_spots+1):
        if next_state[i]==1:
            enemy[i-1]=1
            b.place_marker(pos=i-1,player_num=2)
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


    #stopped = True
