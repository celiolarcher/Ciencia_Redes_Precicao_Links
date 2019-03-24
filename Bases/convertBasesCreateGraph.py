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

#nx.draw_networkx(graph)
#plt.show()

prune_ratio=0.1

sizeTrainningTest=int(graph.number_of_edges()*prune_ratio)
listTrainningTest=[]
#sizeTrainningTest=5
print(graph.number_of_nodes())
print(graph.number_of_edges())
print(sizeTrainningTest)


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

for i in range(1,int(sizeTrainningTest/2)+1):
    index_i=0
    index_j=0
    while True:
        index_i=random.randint(0,graph.number_of_nodes()-1)
        index_j=random.randint(0,graph.number_of_nodes()-1)
        if index_i==index_j: index_j=(index_j+1) % graph.number_of_nodes()        
        index_i=int(list(graph.nodes())[index_i])
        index_j=int(list(graph.nodes())[index_j])
        if graph.has_edge(index_i,index_j)==False: break

    listTrainningTest.append([index_i,index_j,graph.has_edge(index_i,index_j)])


graph_connected=nx.is_connected(graph)

for i in range(1,sizeTrainningTest-len(listTrainningTest)+1):
    degree_i=0
    degree_j=0
    index_i=0
    index_j=0

    count=0
    while degree_i<=1 or degree_j<=1:
        rand_edge=random.randint(0,graph.number_of_edges()-1)    
        index_i=list(graph.edges())[rand_edge][0]
        index_j=list(graph.edges())[rand_edge][1]
        degree_i=graph.degree(index_i)
        degree_j=graph.degree(index_j)  
        if degree_i>1 and degree_j>1:
            graph.remove_edge(index_i,index_j)
            if graph_connected==True and nx.is_connected(graph)==False:
                graph.add_edge(index_i,index_j)
                degree_i=0
            else:
                listTrainningTest.append([index_i,index_j,True])                
                count=0
        count+=1
        if(count>=100): 
            print("Too many randoms")
            break
  

#print(listTrainningTest)

#for i in range(1,graph.number_of_nodes()+1):
#    for j in range(i+1,graph.number_of_nodes()+1):
#        degree_i=graph.degree(str(i))
#        degree_j=graph.degree(str(j))
#        print(i,j,degree_i if degree_i>degree_j else degree_j, degree_j if degree_i>degree_j else degree_i,len(list(nx.shortest_simple_paths(graph,str(i),str(j)))[0])-1,nx.clustering(graph,str(i)),nx.clustering(graph,str(j)), graph.has_edge(str(i),str(j)))
       # nx.center
       # nx.katz_centrality
       # nx.jaccard_coefficient
       # nx.attribute_assortativity_coefficient

#nx.draw_networkx(graph)
#plt.show()


name_file_out=name_file_out +".arff"
file_out=open(name_file_out,'w')
file_out.write('@relation grafo\n')
file_out.write('@attribute degree_H numeric\n')
file_out.write('@attribute degree_L numeric\n')
file_out.write('@attribute short_path numeric\n')
file_out.write('@attribute clustering_H numeric\n')
file_out.write('@attribute clustering_L numeric\n')
file_out.write('@attribute betweenness_centrality_H numeric\n')
file_out.write('@attribute betweenness_centrality_L numeric\n')
file_out.write('@attribute closeness_centrality_H numeric\n')
file_out.write('@attribute closeness_centrality_L numeric\n')
file_out.write('@attribute eccentricity_H numeric\n')
file_out.write('@attribute eccentricity_L numeric\n')
file_out.write('@attribute eigenCentrality_H numeric\n')
file_out.write('@attribute eigenCentrality_L numeric\n')
file_out.write('@attribute common_neighbors numeric\n')
file_out.write('@attribute has_edge {True,False}\n')
file_out.write('\n\n@data\n\n')

print("Load done")

dicEccentricity={}

try:
    dicEccentricity=nx.eccentricity(graph)
except nx.exception.NetworkXError:
    if nx.is_connected(graph)==False:
        print("Not eccentricity")
        for component_nodes in nx.connected_components(graph):
            dicEccentricity.update(nx.eccentricity(graph.subgraph(component_nodes)))
    else: print("Graph error in eccentricity")
print("eccentricity")
dicBetweenness=nx.betweenness_centrality(graph)
print("between")
dicCloseness=nx.closeness_centrality(graph)
print("closeness")
dicEigenCentrality=nx.eigenvector_centrality_numpy(graph)
print("eigen")
print("Start List")
#print(dicEigenCentrality)

for i in range(0,sizeTrainningTest):
        degree_i=graph.degree(listTrainningTest[i][0])
        degree_j=graph.degree(listTrainningTest[i][1])
        cluster_i=nx.clustering(graph,listTrainningTest[i][0])
        cluster_j=nx.clustering(graph,listTrainningTest[i][1])
        between_central_i=dicBetweenness[listTrainningTest[i][0]]
        between_central_j=dicBetweenness[listTrainningTest[i][1]]
        close_central_i=dicCloseness[listTrainningTest[i][0]]
        close_central_j=dicCloseness[listTrainningTest[i][1]]
        eccentricity_i=dicEccentricity[listTrainningTest[i][0]]
        eccentricity_j=dicEccentricity[listTrainningTest[i][1]]
        eigenCentrality_i=dicEigenCentrality[listTrainningTest[i][0]]
        eigenCentrality_j=dicEigenCentrality[listTrainningTest[i][1]]
        
        #str(len(list(nx.shortest_simple_paths(graph,listTrainningTest[i][0],listTrainningTest[i][1]))[0])-1)

        dist=0
        try:
            dist=str(len(nx.shortest_path(graph,listTrainningTest[i][0],listTrainningTest[i][1]))-1) 
        except nx.NetworkXNoPath:
            dist=graph.number_of_nodes()

        file_out.write(str(degree_i if degree_i>degree_j else degree_j) +','+ str(degree_j if degree_i>degree_j else degree_i) + ',' + str(dist) + ',' + str(cluster_i if cluster_i>cluster_j else cluster_j) + ',' + str(cluster_j if cluster_i>cluster_j else cluster_i) + "," + str(between_central_i if between_central_i >between_central_j else between_central_j) + "," + str(between_central_j if between_central_i>between_central_j else between_central_i)  + ',' + str(close_central_i if close_central_i >close_central_j else close_central_j) + "," + str(close_central_j if close_central_i>close_central_j else close_central_i)  + ','  + str(eccentricity_i if eccentricity_i >eccentricity_j else eccentricity_j) + "," + str(eccentricity_j if eccentricity_i>eccentricity_j else eccentricity_i)  + ',' + str(eigenCentrality_i if eigenCentrality_i >eigenCentrality_j else eigenCentrality_j) + "," + str(eigenCentrality_j if eigenCentrality_i>eigenCentrality_j else eigenCentrality_i) + ',' + str(len(list(nx.common_neighbors(graph,listTrainningTest[i][0],listTrainningTest[i][1])))) + ','  + str(listTrainningTest[i][2]) + '\n' )
 


file_out.close()
