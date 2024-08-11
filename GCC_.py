# -*- coding: utf-8 -*-
"""
Created on Wed May 10 00:07:06 2023

@author: asus
"""
import networkx as nx
import numpy as np
from random import sample
import csv
import timeit
import matplotlib.pyplot as plt


global graph
graph = nx.Graph()



def initialization():
    nodeCnt = 0
    
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
            
            


def GCC():
    sub_g = nx.Graph()
    g_comp_size = 0
    for c in sorted(nx.connected_components(graph2), key=len, reverse=True):
        #print(len(c))
        for ci in c:
            sub_g.add_node(ci,v="f")
            for ci_nei in graph.neighbors(ci):
                if ci_nei in c:
                    sub_g.add_node(ci_nei)
                    sub_g.add_edge(ci, ci_nei)
    
    
        
        #run sub_graph bfs for all nodes
        max_size = 0
        for n in sub_g.nodes():
            comp_size = GCC_BFS(sub_g, n)
            if comp_size > max_size:
                max_size = comp_size
        if max_size > g_comp_size:
            g_comp_size = max_size
    return g_comp_size
                    
def find_min_time(time_list, minval):
    min_time = 20000
    for i in time_list:
        if i < min_time and i > minval:
            min_time = i
    
    if  min_time < 2000:
        return min_time
    else:
        return -1
    

def GCC_BFS(new_graph, source):
    q1 = []
    q2 = []
    bfs_time_order = {}
    parent_time = 0
    parent_dic = {}
    
    q1.append( source)
    bfs_time_order[ source] =  parent_time
    
    while q1 or  q2:
        while  q1:
            #print("q1",len(q1))
            parent_time = bfs_time_order[q1[0]]
            for neigh in new_graph.neighbors(q1[0]):
               
                t = find_min_time(graph.edges[q1[0],neigh]["activetime"],parent_time)
                if neigh not in bfs_time_order.keys():
                    bfs_time_order[neigh] = t
                    
                    if t > 0:
                        
                        q2.append(neigh)
                        if q1[0] not in parent_dic.keys():
                            parent_dic[q1[0]] = [neigh]
                        else:
                            parent_dic[q1[0]].append(neigh)
                elif neigh in bfs_time_order.keys():
                    
                    if bfs_time_order[neigh] == -1 and t >= 0:
                        bfs_time_order[neigh] = t
                        
                        q2.append(neigh)
                        if q1[0] not in parent_dic.keys():
                            parent_dic[q1[0]] = [neigh]
                        else:
                            parent_dic[q1[0]].append(neigh)
            #print(len(q1))
            q1.pop(0)
                    
        while q2:
            #print("q2",q2)
            parent_time = bfs_time_order[q2[0]]
            
            for neigh in new_graph.neighbors(q2[0]):
                t = find_min_time(graph.edges[q2[0],neigh]["activetime"],parent_time)
                #print(q2[0],neigh,t)
                if neigh not in bfs_time_order.keys():
                    bfs_time_order[neigh] = t
                    
                    if t > 0:
                        q1.append(neigh)
                        if q2[0] not in parent_dic.keys():
                            parent_dic[q2[0]] = [neigh]
                        else:
                            parent_dic[q2[0]].append(neigh)
                elif neigh in bfs_time_order.keys():
                    if bfs_time_order[neigh] == -1 and t >= 0:
                        bfs_time_order[neigh] = t
                        q1.append(neigh)
                        if q2[0] not in parent_dic.keys():
                            parent_dic[q2[0]] = [neigh]
                        else:
                            parent_dic[q2[0]].append(neigh)
            q2.pop(0)
    return len(bfs_time_order)
    
def remove_node(remove_list):
    if "244" in remove_list:
        print("*************************")
    for i in remove_list:
        graph2.remove_node(int(i))
        

    
    
    
beginTime = timeit.default_timer()        
#file1 = open(r"E:\influensial nodes\Code GCC\high school\indexes betweenness_workplace.csv")
file  = open(r"E:\influensial nodes\DataSet\workplace_dataset_232.csv")
dataset = np.loadtxt(file, delimiter = ",", skiprows = 1)

initialization()


percent = [0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]

#----------------------Beetweenness-----------------------------#
print("Beetweenness")
file1 = open(r"E:\influensial nodes\Code GCC\workplace\indexes betweenness_workplace.csv")
reader_obj = csv.reader(file1)
v_indexes = []

for row in reader_obj:
    v_indexes.append(row)
    
    
comp_size_between = []
for p in percent:
    node_to_remove = []
    x = ((v_indexes)[int((p * len(v_indexes))):])
    
    for x2 in x:
        node_to_remove += x2
    #print(node_to_remove[:10])
    graph2 = graph.copy()
    remove_node(node_to_remove)
    temp = GCC()/len(graph.nodes())
    comp_size_between.append(temp)   
    #print(temp)
endTime = timeit.default_timer()
totalRunTime = (endTime - beginTime)            
            
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8],comp_size_between,label = "Beetweenness",  linestyle='-', color='b',linewidth=3)

print(len(graph.nodes()))
print(len(graph2.nodes()))

#----------------------LocalCentrality-----------------------------#
print("LocalCentrality")
file1 = open(r"E:\influensial nodes\Code GCC\workplace\indexes localcentrality_workplace.csv")
reader_obj = csv.reader(file1)
v_indexes = []

for row in reader_obj:
    v_indexes.append(row)
    
print()    
comp_size_local = []
for p in percent:
    node_to_remove = []
    x = ((v_indexes)[int((p * len(v_indexes))):])
    
    for x2 in x:
        node_to_remove += x2
    #print(node_to_remove[:10])

    graph2 = graph.copy()
    print(p,len(graph2.nodes()))
    remove_node(node_to_remove)
    temp = GCC()/len(graph.nodes())
    comp_size_local.append(temp)   
    #print(temp)
endTime = timeit.default_timer()
totalRunTime = (endTime - beginTime)            
            
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8],comp_size_local,label = "SemiLocalCentrality",  linestyle='-', color='g',linewidth=2)



#----------------------LocalIntegration-----------------------------#
print("LocalIntegration")
file1 = open(r"E:\influensial nodes\Code GCC\workplace\indexes localIntegration_workplace.csv")
reader_obj = csv.reader(file1)
v_indexes = []

reader = csv.reader(x.replace('\0', '') for x in reader_obj)

if '\0' in open('E:\influensial nodes\Code GCC\workplace\indexes localIntegration_workplace.csv').read():
    print ("you have null bytes in your input file")
else:
    print ("you don't")

for row in reader_obj:
    #print(row)
    v_indexes.append(row)
    
comp_size_local = []
for p in percent:
    node_to_remove = []
    x = ((v_indexes)[int((p * len(v_indexes))):])
    
    for x2 in x:
        node_to_remove += x2
    #print(node_to_remove[:10])

    graph2 = graph.copy()
    ###########3
    for kk in range(len(node_to_remove)):
        if node_to_remove[kk] == "244":
            print("indices", kk)
        
    ############
    remove_node(node_to_remove)
    temp = GCC()/len(graph.nodes())
    comp_size_local.append(temp)   
    #print(temp)
endTime = timeit.default_timer()
totalRunTime = (endTime - beginTime)            
            
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8],comp_size_local,label = "LocalIntegration",  linestyle='-', color='r',linewidth=2)
print(len(graph.nodes()))
print(len(graph2.nodes()))



#----------------------DegreeDeviation-----------------------------#
print("DegreeDeviation")
file1 = open(r"E:\influensial nodes\Code GCC\workplace\indexes degreeDeviation_workplace.csv")
reader_obj = csv.reader(file1)
v_indexes = []




for row in reader_obj:
    #print(row)
    v_indexes.append(row)
    
print()    
comp_size_local = []
for p in percent:
    node_to_remove = []
    x = ((v_indexes)[int((p * len(v_indexes))):])
    
    for x2 in x:
        node_to_remove += x2
    #print(node_to_remove[:10])

    graph2 = graph.copy()
    print(p,len(graph2.nodes()))
    remove_node(node_to_remove)
    temp = GCC()/len(graph.nodes())
    comp_size_local.append(temp)   
    #print(temp)
endTime = timeit.default_timer()
totalRunTime = (endTime - beginTime)            
            
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8],comp_size_local,label = "DegreeDeviation",  linestyle='-', color='orange',linewidth=2)
print(len(graph.nodes()))
print(len(graph2.nodes()))

#----------------------Closeness-----------------------------#
print("Closeness")
file1 = open(r"E:\influensial nodes\Code GCC\workplace\indexes closeness_workplace.csv")
reader_obj = csv.reader(file1)
v_indexes = []




for row in reader_obj:
    #print(row)
    v_indexes.append(row)
    
print()    
comp_size_local = []
for p in percent:
    node_to_remove = []
    x = ((v_indexes)[int((p * len(v_indexes))):])
    
    for x2 in x:
        node_to_remove += x2
    #print(node_to_remove[:10])

    graph2 = graph.copy()
    print(p,len(graph2.nodes()))
    remove_node(node_to_remove)
    temp = GCC()/len(graph.nodes())
    comp_size_local.append(temp)   
    #print(temp)
endTime = timeit.default_timer()
totalRunTime = (endTime - beginTime)            
            
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8],comp_size_local,label = "Closeness Centrality",  linestyle='-', color='purple',linewidth=3)
print(len(graph.nodes()))
print(len(graph2.nodes()))


#----------------------CycleRatio-----------------------------#
print("CycleRatio")
file1 = open(r"E:\influensial nodes\Code GCC\workplace\indexes cycleratio_workplace.csv")
reader_obj = csv.reader(file1)
v_indexes = []




for row in reader_obj:
    #print(row)
    v_indexes.append(row)
    
print()    
comp_size_local = []
for p in percent:
    node_to_remove = []
    x = ((v_indexes)[int((p * len(v_indexes))):])
    
    for x2 in x:
        node_to_remove += x2
    #print(node_to_remove[:10])

    graph2 = graph.copy()
    print(p,len(graph2.nodes()))
    remove_node(node_to_remove)
    temp = GCC()/len(graph.nodes())
    comp_size_local.append(temp)   
    #print(temp)
endTime = timeit.default_timer()
totalRunTime = (endTime - beginTime)            
            
plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8],comp_size_local,label = "CycleRatio", linestyle='-', color='Turquoise',linewidth=2)
print(len(graph.nodes()))
print(len(graph2.nodes()))
plt.xlabel('removed nodes %')
plt.ylabel('GCC mean size')
plt.legend()    
plt.savefig('workplace_gcc_test.eps', format='eps')    
plt.show()    
                                  
