import dimod
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from board24 import Board
import numpy as np
import sys

num_spots = 24
max_checkers = 18
our = np.zeros(num_spots,dtype=int)
enemy = np.zeros(num_spots,dtype=int)
h_const = 100
j_const = 1
constraint_const = 2
mill_constant = 0.1
anti_mill_constant = 2


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
            #idx = b.get_rowcol_idx(i) # This is the original
            idx = b.get_neighbor_idx(i)
            for j in idx:
                if i > j:
                    quadratic[(j+1,i+1)] += -j_const
                else:
                    quadratic[(i+1,j+1)] += -j_const

    # update quadratic for mill energy decrease
    for i in range(0,num_spots):
        if enemy[i] == 0:
            continue
        #idx = b.get_rowcol_idx(i) # This is the original
        idx = b.get_neighbor_idx(i)
        for j in idx:
            if i < j:
                quadratic[(i+1,j+1)] -= 2*mill_constant
    offset -= (2*num_spots)*mill_constant
    # update quadratic for mill energy decrease
    for i in range(0,num_spots):
        if our[i] == 0:
            continue
        #idx = b.get_rowcol_idx(i) # This is the original
        idx = b.get_neighbor_idx(i)
        for j in idx:
            if i < j:
                quadratic[(i+1,j+1)] -= 2*anti_mill_constant
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
    print("sample_set:", sample_set)
    next_state = sample_set.samples()[0] # Maybe do sampling instead??
    print("next_state:",next_state)
    for i in range(1,num_spots+1):
        if next_state[i]==1 and enemy[i-1] != 1:
            enemy[i-1]=1
            b.place_marker(pos=i-1,player_num=2)
    print(enemy)
    print(b)
    
    # Choose our input
    our_pos = int(eval(input('Give position to place marker (1-24): ')))
    our[our_pos-1] = 1
    b.place_marker(pos=our_pos-1,player_num=1)
    
    print("Linear size :",len(linear))
    print("Quadratic size :",len(quadratic))
    
    
    #stopped = True
