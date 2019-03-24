import networkx as nx
import matplotlib.pyplot as plt
import random 
import argparse


p=0.3
n=100

k=10 #number of neighboors
m=5 #numer of edges to attach from a new node to existing nodes



parser = argparse.ArgumentParser()
parser.add_argument("-gnp", "--gnp", help="Gnp graph", type=float, nargs=2)
parser.add_argument("-sw", "--smallworld", help="Small World graph", type=float, nargs=3)
parser.add_argument("-pa", "--preferentialattachment", help="Preferencial Attachment graph", type=int, nargs=2)
parser.add_argument("-f", "--file", help="input graph FILE", type=argparse.FileType('r'))


args = parser.parse_args()



graph=object

name_file_out=''

if args.gnp is not None:
    print("GNP")
    name_file_out="GNP"
    graph=nx.gnp_random_graph(int(args.gnp[0]),args.gnp[1])


if args.smallworld is not None:
    print("SW")
    name_file_out="SmallWorld"
    graph=nx.watts_strogatz_graph(int(args.smallworld[0]),int(args.smallworld[1]),args.smallworld[2])


if args.preferentialattachment is not None:
    print("PA")
    name_file_out="PreferentialAttachment"
    graph=nx.barabasi_albert_graph(int(args.preferentialattachment[0]),int(args.preferentialattachment[1]))


if args.file is not None:
    print("file")
    file=args.file

    str1=file.readline()
    #print(str1)

    for str1 in file:
        if(str1.find("*Edges")>=0):
            break

    graph=nx.Graph()

    for str1 in file:
        if(str1.find("*Triangles")>=0):
            break
        edges=str1.split()
        if edges[0]!=edges[1]:
            graph.add_edge(edges[0],edges[1])        

    if nx.is_connected(graph)==False:
        print("Not connected")
        graph=graph.subgraph(sorted(nx.connected_components(graph), key = len, reverse=True)[0])
#        graph=nx.connected_components(graph)[0]

    file.close()


#nx.draw_networkx(graph)
#plt.show()

prune_ratio=0.1

sizeTrainningTest=int(graph.number_of_edges()*prune_ratio)
listTrainningTest=[]
#sizeTrainningTest=5
print(graph.number_of_nodes())
print(graph.number_of_edges())


#has_edge_false=0

#for i in range(1,sizeTrainningTest+1):
#    index_i=random.randint(1,graph.number_of_nodes())
#    index_j=random.randint(1,graph.number_of_nodes())
#    if index_i==index_j: index_j=(index_j+1) % graph.number_of_nodes()
#    listTrainningTest.append([str(index_i),str(index_j),graph.has_edge(str(index_i),str(index_j))])
#    if graph.has_edge(str(index_i),str(index_j))==False:
#        has_edge_false+=1
#    else:
#        graph.remove_edge(str(index_i),str(index_j))
#    if has_edge_false == int(sizeTrainningTest/2): break

n=graph.number_of_nodes()
p=2*graph.number_of_edges()/(n*(n-1))

print(p)

randGraph=nx.gnp_random_graph(n,p)

print(randGraph.number_of_nodes())
print(randGraph.number_of_edges())

#l=0
#try:
#    l=nx.average_shortest_path_length(graph)
#except nx.NetworkXError:
#    listnodes=list(graph.nodes())
#    count=0
#    sum_path=0
#    print("disconnected")
#    while listnodes:
#        node1=listnodes.pop()
#        for node2 in listnodes:
#            try:
#                dist=nx.shortest_path_length(graph,node1,node2)
#                sum_path+=dist
#            except nx.NetworkXNoPath:
#                count+=1
#    l=sum_path/((graph.number_of_nodes()*(graph.number_of_nodes()-1))/2-count)
#    print(len(listnodes))

l=0
try:
    l=nx.average_shortest_path_length(graph)
except nx.exception.NetworkXError:
    if nx.is_connected(graph)==False:
        print("Not connected")
        count=0
        for component_nodes in nx.connected_components(graph):
            l+=nx.average_shortest_path_length(graph.subgraph(component_nodes))
            count+=1
            print("component_node done")
        l/=count
    else: print("Graph error in eccentricity")


print("average path done")

if nx.is_connected(randGraph)==False:
    print("Rand graph not connected")
    print(randGraph.number_of_nodes())
    print(randGraph.number_of_edges())
    randGraph=randGraph.subgraph(sorted(nx.connected_components(randGraph), key = len, reverse=True)[0])
    print(randGraph.number_of_nodes())
    print(randGraph.number_of_edges())

        
lrand=nx.average_shortest_path_length(randGraph)


c=nx.transitivity(graph)  #global clustering

crand=nx.transitivity(randGraph)

#nx.average_clustering(graph) #local clustering average

smallworldness=(c/crand)/(l/lrand)

print("Smallworldness:")
print(c/crand)
print(l/lrand)

print(smallworldness)
