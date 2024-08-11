# -*- coding: utf-8 -*-
"""
Created on Tue May  9 10:06:50 2023

@author: asus
"""
import networkx as nx
import numpy as np
#import timeit
import matplotlib.pyplot as plt
#import csv
import random
#from igraph import *
#import timeit
#import copy


global graph
graph = nx.Graph()
graph_copy = nx.Graph()


file2 = open("E:\influensial nodes\DataSet\detailed_list_of_contacts_Hospital.csv")
dataset = np.loadtxt(file2, delimiter = ",", skiprows = 1)
def initialization():
    
    for row in range(len(dataset)):
        
        i = int(dataset[row][0])
        j = int(dataset[row][1])
        #print(i,j)
        graph.add_node(i, state = False, infTime = 0) 
        graph.add_node(j, state = False, infTime = 0)
        if graph.has_edge(i,j):
            if int(dataset[row][2]) not in graph.edges[i,j]["activetime"]:
                graph.edges[i,j]["activetime"].append(int(dataset[row][2])) 
        else:
            graph.add_edge(i, j, weight = 0,activetime = [int(dataset[row][2])])




def set_seed():
    infected_nodes = []
    for s in seed:
        #print(s)
        if s not in graph.nodes():
            print(s)
        graph.nodes[int(s)]["state"] = True
        infected_nodes.append(int(s))
    return infected_nodes
        
def generate_random():
    landa_p = random.random()
    if landa_p < landa:
        return True
    else:
        return False

def recovery(to_recover,time):
    recovered = [x for x in to_recover if generate_random()]
    for r2 in recovered:
        graph.nodes[r2]["state"] = "R"
    not_recovered = [x for x in to_recover if x not in recovered]
    return not_recovered
            
    

def dynamic_epidemic():
    infected_nodes = []
    new_infected = set_seed()
    di_dt = [0]*maxTime    
    time = 0
    total_Infected = 0# total number of infected nodes 
    while total_Infected < graph.number_of_nodes() and time < maxTime: 
        infected_nodes = infected_nodes +  new_infected  
        new_infected.clear()
        for v1 in infected_nodes:            
            for v2 in graph.neighbors(v1):  
                
                if (graph.nodes[v1]["state"] == True and time in graph.edges[v1,v2]["activetime"]
                    and graph.nodes[v1]["infTime"] <= time and graph.nodes[v2]["state"] == False) :
                    beta_p = random.random()
                    #print(beta_p)
                    if beta_p < beta:
                        graph.nodes[v2]["state"] = True                        
                        graph.nodes[v2]["infTime"] = time
                        total_Infected += 1
                        (new_infected).append(v2)
        infected_nodes = recovery(infected_nodes,time) 
        #print('i',time,new_infected)
        di_dt[time] = len(new_infected) + len(infected_nodes) 
        time += 1
    return (di_dt)

def add_list(total_di_dt,di_dt):
    return[total_di_dt[x]+di_dt[x] for x in range(len(di_dt)) ]

beta = 0.5
landa = 0.005
maxTime = 3510
#total_di_dt = [0]*maxTime    
initialization()

#############################Betweenness##########################
print("Betweenness")
total_di_dt = [0]*maxTime    
initialization()

file1 = open(r"E:\influensial nodes\Code SIR\hospital\indexes betweeness_hospital.csv")
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()
for i in range(50):
    graph = graph_copy.copy()
    set_seed()
    di_dt = dynamic_epidemic()
    #print(di_dt[0])
    total_di_dt = add_list(total_di_dt,di_dt)

plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Betweenness",  linestyle='-', color='b',linewidth=1)


#############################Semi local centrality##########################
total_di_dt = [0]*maxTime    
initialization()

print("Semi local centrality")
file1 = open(r"E:\influensial nodes\Code SIR\hospital\indexes centrality_hospital.csv")
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()
for i in range(50):
    graph = graph_copy.copy()
    set_seed()
    di_dt = dynamic_epidemic()
    #print(di_dt[0])
    total_di_dt = add_list(total_di_dt,di_dt)

plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Semi local centrality", linestyle='-', color='g',linewidth=1)

#############################Local Integration##########################
total_di_dt = [0]*maxTime    
initialization()

print("Local Integration")
file1 = open(r"E:\influensial nodes\Code SIR\hospital\indexes Local Integration_hospital.csv")
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()
for i in range(50):
    graph = graph_copy.copy()
    set_seed()
    di_dt = dynamic_epidemic()
    #print(di_dt[0])
    total_di_dt = add_list(total_di_dt,di_dt)

plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "local integration", linestyle='-', color='r',linewidth=1)


#############################DegreeDeviation##########################
total_di_dt = [0]*maxTime    
initialization()

print("DegreeDeviation")
file1 = open(r"E:\influensial nodes\Code SIR\hospital\indexes Degreedeviation_hospital.csv")
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()
for i in range(50):
    graph = graph_copy.copy()
    set_seed()
    di_dt = dynamic_epidemic()
    #print(di_dt[0])
    total_di_dt = add_list(total_di_dt,di_dt)

plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Degree deviation", linestyle='-', color='orange',linewidth=1)


#############################Closeness##########################
total_di_dt = [0]*maxTime    
initialization()

print("Closeness")
file1 = open(r"E:\influensial nodes\Code SIR\hospital\indexes closeness_hospital.csv")
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()
for i in range(50):
    graph = graph_copy.copy()
    set_seed()
    di_dt = dynamic_epidemic()
    #print(di_dt[0])
    total_di_dt = add_list(total_di_dt,di_dt)

plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Closeness", linestyle='-', color='purple',linewidth=1)


#############################Cycle ratio##########################
total_di_dt = [0]*maxTime    
initialization()

print("Cycle ratio")
file1 = open(r"E:\influensial nodes\Code SIR\hospital\indexes CycleRatio-hospital.csv")
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()
for i in range(50):
    graph = graph_copy.copy()
    set_seed()
    di_dt = dynamic_epidemic()
    ##print(di_dt[0])
    total_di_dt = add_list(total_di_dt,di_dt)

plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Cycle ratio", linestyle='-', color='Turquoise',linewidth=1)


plt.xlabel('time')
plt.ylabel('di/dt')
plt.legend()  
plt.savefig('hospital_SIR_speed.eps', format='eps')    
  

file1.close()