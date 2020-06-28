# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 14:04:46 2020

@author: choco
"""

import numpy as np
import matplotlib.pyplot as plt

import qiskit
from qiskit import Aer
from qiskit.visualization import *

import dataprocessing as dp



import torch
from torch.autograd import Function
from torchvision import datasets, transforms
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F

class QuantumCircuit:
    """ 
    This class provides a simple interface for interaction 
    with the quantum circuit 
    """
    
    def __init__(self, n_qubits, backend, shots):
        # --- Circuit definition ---
        self._circuit = qiskit.QuantumCircuit(n_qubits)
        
        all_qubits = [i for i in range(n_qubits)]
        self.theta = qiskit.circuit.Parameter('theta')
        
        self._circuit.h(all_qubits)
        self._circuit.barrier()
        self._circuit.ry(self.theta, all_qubits)
        
        self._circuit.measure_all()
        # ---------------------------

        self.backend = backend
        self.shots = shots
    
    def run(self, thetas):
        job = qiskit.execute(self._circuit, 
                             self.backend, 
                             shots = self.shots,
                             parameter_binds = [{self.theta: theta} for theta in thetas])
        result = job.result().get_counts(self._circuit)
        
        counts = np.array(list(result.values()))
        states = np.array(list(result.keys())).astype(float)
        
        # Compute probabilities for each state
        probabilities = counts / self.shots
        # Get state expectation
        expectation = np.sum(states * probabilities)
        
        return np.array([expectation])

    def draw_circuit(self):
        print(self._circuit.draw())


class HybridFunction(Function):
    """ Hybrid quantum - classical function definition """
    
    @staticmethod
    def forward(ctx, input, quantum_circuit, shift):
        """ Forward pass computation """
        ctx.shift = shift
        ctx.quantum_circuit = quantum_circuit

        expectation_z = ctx.quantum_circuit.run(input[0].tolist())
        result = torch.tensor([expectation_z])
        ctx.save_for_backward(input, result)

        return result
        
    @staticmethod
    def backward(ctx, grad_output):
        """ Backward pass computation """
        input, expectation_z = ctx.saved_tensors
        input_list = np.array(input.tolist())
        
        shift_right = input_list + np.ones(input_list.shape) * ctx.shift
        shift_left = input_list - np.ones(input_list.shape) * ctx.shift
        
        gradients = []
        for i in range(len(input_list)):
            expectation_right = ctx.quantum_circuit.run(shift_right[i])
            expectation_left  = ctx.quantum_circuit.run(shift_left[i])
            
            gradient = torch.tensor([expectation_right]) - torch.tensor([expectation_left])
            gradients.append(gradient)
        gradients = np.array([gradients]).T
        return torch.tensor([gradients]).float() * grad_output.float(), None, None

class Hybrid(nn.Module):
    """ Hybrid quantum - classical layer definition """
    
    def __init__(self, backend, shots, shift):
        super(Hybrid, self).__init__()
        self.quantum_circuit = QuantumCircuit(1, backend, shots)
        self.shift = shift
        
    def forward(self, input):
        return HybridFunction.apply(input, self.quantum_circuit, self.shift)





def c(x):
    return np.cos(x)

def s(x):
    return np.sin(x)

def c2(x,y):
    return c(x) * c(y)

def s2(x,y):
    return s(x) * s(y)

def sc_plus(x,y):
    return s(x) * c(y) + 1j * s(y) * c(x)

def sc_minus(x,y):
    return s(x) * c(y) - 1j * s(y) * c(x)

def cis_plus(x,y):
    return c2(x,y) + 1j * s2(x,y)

def cis_minus(x,y):
    return c2(x,y) - 1j * s2(x,y)


class EntangledCircuit:
    """ 
    This class provides a simple interface for interaction 
    with the quantum circuit 
    """
    
    def __init__(self, backend, shots):
        # --- Circuit definition ---
        self._circuit = qiskit.QuantumCircuit(2)
        
        self.theta = qiskit.circuit.Parameter('theta')
        self.phi = qiskit.circuit.Parameter('phi')
        
        self._circuit.h(0)
        self._circuit.cx(0,1)
        self._circuit.barrier()
        self._circuit.ry(self.theta, 0)
        self._circuit.rx(self.phi,1)
        
        self._circuit.measure_all()
        # ---------------------------

        self.backend = backend
        self.shots = shots
    
    
    
    def get_eigen_values(self,t,p):
        A = np.array([[cis_plus(t,p), -sc_plus(t,p), cis_minus(t,p), sc_minus(t,p) ],
                 [-sc_plus(t,p), cis_plus(t,p), sc_minus(t,p), cis_minus(t,p) ],
                 [sc_minus(t,p), cis_minus(t,p),sc_plus(t,p), -cis_plus(t,p) ],
                 [cis_minus(t,p),sc_minus(t,p),-cis_plus(t,p),sc_plus(t,p) ]
                 ])
        eigenvalues, eigenvectors = np.linalg.eig(A)
        return eigenvalues
    
    def run(self, angles): # 2D array for angle?
        job = qiskit.execute(self._circuit, 
                             self.backend, 
                             shots = self.shots,
                             parameter_binds = [{self.theta:angles[0],self.phi:angles[1]}])
                            
        result = job.result().get_counts(self._circuit)
        
        counts = np.array(list(result.values()))
        states = np.array(list(result.keys())).astype(float)
         
        # Compute probabilities for each state
        probabilities = counts / self.shots
        print("probs:",probabilities)
        print("states:",states)
        
        # Get state expectation
        expectation = np.sum(states * probabilities)
        print("expectation value: ", expectation)
        
        l = self.get_eigen_values(angles[0],angles[1])
        n_expectation = l @ probabilities
        print("new expectation value: ",abs(n_expectation))
        
        return np.array([expectation])
    
    def draw_circuit(self):
        print(self._circuit.draw())


class HybridFunction2(Function):
    """ Hybrid quantum - classical function definition """
    
    @staticmethod
    def forward(ctx, input, quantum_circuit, shift):# Can we imagine shift as a 2D array? :(
        """ Forward pass computation """
        ctx.shift = shift
        ctx.quantum_circuit = quantum_circuit

        expectation_z = ctx.quantum_circuit.run(input[0].tolist())
        result = torch.tensor([expectation_z])
        ctx.save_for_backward(input, result)

        return result
        
    @staticmethod
    def backward(ctx, grad_output):
        """ Backward pass computation """
        input, expectation_z = ctx.saved_tensors
        input_list = np.array(input.tolist())
        
        shift_right = input_list + np.ones(input_list.shape) * ctx.shift
        shift_left = input_list - np.ones(input_list.shape) * ctx.shift
        
        gradients = []
        """
        for i in range(len(input_list)): # Maybe change that? We have only one input 2D Array
            expectation_right = ctx.quantum_circuit.run(shift_right[i])
            expectation_left  = ctx.quantum_circuit.run(shift_left[i])
            
            gradient = torch.tensor([expectation_right]) - torch.tensor([expectation_left])
            gradients.append(gradient)
        """
        #---------- The might break section -----------------------------------------------
        expectation_right = ctx.quantum_circuit.run(shift_right[i])
        expectation_left  = ctx.quantum_circuit.run(shift_left[i])
            
        gradient = torch.tensor([expectation_right]) - torch.tensor([expectation_left])
        gradients.append(gradient)    
        #----------------------------------------------------------------------------------
        gradients = np.array([gradients]).T
        return torch.tensor([gradients]).float() * grad_output.float(), None, None

class Entangled(nn.Module):
    """ Hybrid quantum - classical layer definition """
    
    def __init__(self, backend, shots, shift):
        super(Entangled, self).__init__()
        self.quantum_circuit = QuantumCircuit(1, backend, shots)
        self.shift = shift
        
    def forward(self, input):
        return HybridFunction2.apply(input, self.quantum_circuit, self.shift)



QC1 = QuantumCircuit(1,Aer.get_backend('qasm_simulator'),1024)
QC1.draw_circuit()
QC1.run(np.array([np.pi]))


QC2 = EntangledCircuit(Aer.get_backend('qasm_simulator'),1024)
QC2.draw_circuit()
QC2.run(np.array([np.pi/20,np.pi/3]))



def strinstruction_to_intarray(string):
    conv = {"E":2,"M":1,"O":0}
    output = []
    for idx,char in enumerate(string):
        if idx < 24:
            output.append(conv[char])
        else:
            output.append(int(char))
    return np.array(output)/9


conversione = {"a7": 1, "d7": 2, "g7": 3, "b6": 4, "d6": 5, "f6": 6,
                   "c5": 7,
                   "d5": 8,
                   "e5": 9,
                   "a4": 10,
                   "b4": 11,
                   "c4": 12,
                   "e4": 13,
                   "f4": 14,
                   "g4": 15,
                   "c3": 16,
                   "d3": 17,
                   "e3": 18,
                   "b2": 19,
                   "d2": 20,
                   "f2": 21,    
                   "a1": 22,
                   "d1": 23,
                   "g1": 24}

def moveinstruction_to_intarray_1(string):
    indices = [conversione[string[i:i+2]] - 1 for i in range(0, len(string), 2)] # -1 to have index 
    arrays = []
    for idx in indices:
        tmp = np.zeros((24,))
        tmp[idx] = 1
        arrays.append(tmp)
    return arrays



