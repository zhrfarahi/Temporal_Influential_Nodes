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


file2 = open("E:\influensial nodes\DataSet\conferenceDataset_main.csv")
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
    s = random.choice(list(graph.nodes))
    graph.nodes[int(s)]["state"] = True
    return [s]
  
        
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
    #print(new_infected)
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

def remove_node(new_graph,new_p):
    for i in seed[:int(new_p*len(seed))]:
        new_graph.remove_node(int(i))
    return new_graph
            
    




beta = 0.5
landa = 0.005
maxTime = 2000
  
percent = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
total_peak_time = []
total_value_time = []
#---------------------------------Betweenness---------------------------------------------#
print('Betweenness')
initialization()
file1 = open(r"E:\influensial nodes\Code SIR\Conference\indexes betweeness_confrence.csv")

total_di_dt = [0]*maxTime  
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()

peak_percent_time_arr = []
peak_percent_value_arr = []
for p in percent:
    peak_time_arr = []
    peak_value_arr = []
    for i in range(50):
        graph = graph_copy.copy()   
        graph = remove_node(graph, p)
        #print(len(graph.nodes()))
        
        di_dt = dynamic_epidemic()
        #print(di_dt[0])
        total_di_dt = add_list(total_di_dt,di_dt)
        peak_time = total_di_dt.index(max(total_di_dt))
        peak_value = max(total_di_dt)
        
        peak_time_arr.append(peak_time)
        peak_value_arr.append(peak_value)
        
    peak_percent_time_arr.append(sum(peak_time_arr)/len(peak_time_arr))
    peak_percent_value_arr.append(sum(peak_value_arr)/len(peak_value_arr))
total_peak_time.append(peak_percent_time_arr)
total_value_time.append(peak_percent_value_arr)
#plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Betweenness" ,  linestyle='-', color='b',linewidth=1)



#---------------------------------Semi local centrality---------------------------------------------#
print('Semi local centrality')
initialization()
file1 = open(r"E:\influensial nodes\Code SIR\Conference\indexes centrality_conference.csv")
total_di_dt = [0]*maxTime  
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()

peak_percent_time_arr = []
peak_percent_value_arr = []
for p in percent:
    peak_time_arr = []
    peak_value_arr = []
    for i in range(50):
        graph = graph_copy.copy()   
        graph = remove_node(graph, p)
        #print(len(graph.nodes()))
        
        di_dt = dynamic_epidemic()
        #print(di_dt[0])
        total_di_dt = add_list(total_di_dt,di_dt)
        peak_time = total_di_dt.index(max(total_di_dt))
        peak_value = max(total_di_dt)
        
        peak_time_arr.append(peak_time)
        peak_value_arr.append(peak_value)
        
    peak_percent_time_arr.append(sum(peak_time_arr)/len(peak_time_arr))
    peak_percent_value_arr.append(sum(peak_value_arr)/len(peak_value_arr))
total_peak_time.append(peak_percent_time_arr)
total_value_time.append(peak_percent_value_arr)
#plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Betweenness" ,  linestyle='-', color='b',linewidth=1)




#--------------------------------local integration---------------------------------------------#
print('local integration')
initialization()
file1 = open(r"E:\influensial nodes\Code SIR\Conference\indexes Local Integration_conference.csv")
total_di_dt = [0]*maxTime  
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()

peak_percent_time_arr = []
peak_percent_value_arr = []
for p in percent:
    peak_time_arr = []
    peak_value_arr = []
    for i in range(50):
        graph = graph_copy.copy()   
        graph = remove_node(graph, p)
        #print(len(graph.nodes()))
        
        di_dt = dynamic_epidemic()
        #print(di_dt[0])
        total_di_dt = add_list(total_di_dt,di_dt)
        peak_time = total_di_dt.index(max(total_di_dt))
        peak_value = max(total_di_dt)
        
        peak_time_arr.append(peak_time)
        peak_value_arr.append(peak_value)
        
    peak_percent_time_arr.append(sum(peak_time_arr)/len(peak_time_arr))
    peak_percent_value_arr.append(sum(peak_value_arr)/len(peak_value_arr))
total_peak_time.append(peak_percent_time_arr)
total_value_time.append(peak_percent_value_arr)
#plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Betweenness" ,  linestyle='-', color='b',linewidth=1)



#--------------------------------degree deviation---------------------------------------------#
print('degree deviation')
initialization()
file1 = open(r"E:\influensial nodes\Code SIR\Conference\indexes Degreedeviation_conference.csv")
total_di_dt = [0]*maxTime  
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()

peak_percent_time_arr = []
peak_percent_value_arr = []
for p in percent:
    peak_time_arr = []
    peak_value_arr = []
    for i in range(50):
        graph = graph_copy.copy()   
        graph = remove_node(graph, p)
        #print(len(graph.nodes()))
        
        di_dt = dynamic_epidemic()
        #print(di_dt[0])
        total_di_dt = add_list(total_di_dt,di_dt)
        peak_time = total_di_dt.index(max(total_di_dt))
        peak_value = max(total_di_dt)
        
        peak_time_arr.append(peak_time)
        peak_value_arr.append(peak_value)
        
    peak_percent_time_arr.append(sum(peak_time_arr)/len(peak_time_arr))
    peak_percent_value_arr.append(sum(peak_value_arr)/len(peak_value_arr))
total_peak_time.append(peak_percent_time_arr)
total_value_time.append(peak_percent_value_arr)
#plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Betweenness" ,  linestyle='-', color='b',linewidth=1)





#--------------------------------Closeness---------------------------------------------#
print('Closeness')
initialization()
file1 = open(r"E:\influensial nodes\Code SIR\Conference\indexes closeness_conference.csv")
total_di_dt = [0]*maxTime  
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()

peak_percent_time_arr = []
peak_percent_value_arr = []
for p in percent:
    peak_time_arr = []
    peak_value_arr = []
    for i in range(50):
        graph = graph_copy.copy()   
        graph = remove_node(graph, p)
        #print(len(graph.nodes()))
        
        di_dt = dynamic_epidemic()
        #print(di_dt[0])
        total_di_dt = add_list(total_di_dt,di_dt)
        peak_time = total_di_dt.index(max(total_di_dt))
        peak_value = max(total_di_dt)
        
        peak_time_arr.append(peak_time)
        peak_value_arr.append(peak_value)
        
    peak_percent_time_arr.append(sum(peak_time_arr)/len(peak_time_arr))
    peak_percent_value_arr.append(sum(peak_value_arr)/len(peak_value_arr))
total_peak_time.append(peak_percent_time_arr)
total_value_time.append(peak_percent_value_arr)
#plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Betweenness" ,  linestyle='-', color='b',linewidth=1)





#--------------------------------CycleRatio---------------------------------------------#
print('CycleRatio')
initialization()
file1 = open(r"E:\influensial nodes\Code SIR\Conference\indexes CycleRatio-conference.csv")
total_di_dt = [0]*maxTime  
seed = list(np.loadtxt(file1, delimiter = ","))
graph_copy = graph.copy()

peak_percent_time_arr = []
peak_percent_value_arr = []
for p in percent:
    peak_time_arr = []
    peak_value_arr = []
    for i in range(50):
        graph = graph_copy.copy()   
        graph = remove_node(graph, p)
        #print(len(graph.nodes()))
        
        di_dt = dynamic_epidemic()
        #print(di_dt[0])
        total_di_dt = add_list(total_di_dt,di_dt)
        peak_time = total_di_dt.index(max(total_di_dt))
        peak_value = max(total_di_dt)
        
        peak_time_arr.append(peak_time)
        peak_value_arr.append(peak_value)
        
    peak_percent_time_arr.append(sum(peak_time_arr)/len(peak_time_arr))
    peak_percent_value_arr.append(sum(peak_value_arr)/len(peak_value_arr))
total_peak_time.append(peak_percent_time_arr)
total_value_time.append(peak_percent_value_arr)
#plt.plot([t for t in range(maxTime)], [dd/50 for dd in total_di_dt],label = "Betweenness" ,  linestyle='-', color='b',linewidth=1)




'''for t in range(len(total_peak_time)):
    print(t)
    plt.plot([p for p in percent], total_peak_time[t])'''

for t in range(len(total_value_time)):
    print(t)
    plt.plot([p for p in percent], total_value_time[t])

'''plt.xlabel('number of nodes')
plt.ylabel('di/dt')
plt.legend()  
plt.savefig('test.eps', format='eps')    
file1.close()'''