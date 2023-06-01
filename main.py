import csv

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

def getNetworkDataFromCSV(jdk_version):
    info_file = open(f'dataset/info_{jdk_version}.csv', 'r')
    classes_file = open(f'dataset/classes_{jdk_version}.csv', 'r')
    edges_file = open(f'dataset/edges_{jdk_version}.csv', 'r')

    info_file_reader = csv.reader(info_file)
    classes_file_reader = csv.reader(classes_file)
    edges_file_reader = csv.reader(edges_file)

    total_node = 0
    total_edges = 0
    nodes = []
    edges = []

    # load info
    idx = 0
    for row in info_file_reader:
        if idx == 0:
            idx += 1
            continue
        else:
            total_node = int(row[0])
            total_edges = int(row[1])
            idx += 1

    # load nodes
    idx = 0
    for row in classes_file_reader:
        if idx == 0:
            idx += 1
            continue
        else:
            nodes.append(row[1])
            idx += 1

    # load nodes
    idx = 0
    for row in edges_file_reader:
        if idx == 0:
            idx += 1
            continue
        else:
            edges.append([int(row[0]), int(row[1])])
            idx += 1

    info_file.close()
    classes_file.close()
    edges_file.close()

    network_data = [total_node, total_edges, nodes, edges]
    return network_data

def constructNetwork(net_data):
    net = nx.Graph()
    for i in range(net_data[0]):
        net.add_node(net_data[2][i])
    for edge in net_data[3]:
        net.add_edge(net_data[2][edge[0]], net_data[2][edge[1]])
    return net

def drawNetwork(network):
    # Draw the graph
    nx.draw(network, with_labels=False, node_size=5)

    # Show the graph
    plt.show()

def deleteOutLierNode(net_data):
    new_nodes = []
    for edge in net_data[3]:
        if edge[0] in new_nodes:
            continue
        else:
            new_nodes.append(edge[0])
        if edge[1] in new_nodes:
            continue
        else:
            new_nodes.append(edge[1])
    new_nodes.sort()
    # new_nodes_label = []
    # for node in new_nodes:
    #     new_nodes_label.append(net_data[2][node])
    return new_nodes

def constructNetworkWithoutOutlier(net_data, withoutOutlier):
    net = nx.Graph()
    for i in withoutOutlier:
        net.add_node(net_data[2][i])
    for edge in net_data[3]:
        net.add_edge(net_data[2][edge[0]], net_data[2][edge[1]])
    return net

def drawBarchart(keys, values):
    # create bar chart
    plt.bar(keys, values)

    # add labels and title
    plt.xlabel('classes')
    plt.ylabel('Clustering Co-efficient')
    plt.title('Clustering Co-efficient bar chart')

    # display chart
    plt.show()

def getDictValueMean(dict):
    return np.mean(np.array(list(dict.values())))

def getSomeBasicMetric(network):
    # max_degree = max(dict(network.degree()).values())
    # max_in_degree = max(dict(network.in_degree()).values())
    # max_out_degree = max(dict(network.out_degree()).values())

    # avg_degree = sum(dict(network.degree()).values()) / len(network.nodes)
    # mean_distance = nx.average_shortest_path_length(network)
    # diameter = nx.diameter(network)

    # reciprocity = nx.reciprocity(network)
    # avg_clustering_coefficient = nx.average_clustering(network)
    # clustering = nx.clustering(network)
    # drawBarchart(list(clustering.keys()), list(clustering.values()))
    # return reciprocity, avg_clustering_coefficient

    degree_centrality = nx.degree_centrality(network)
    highest_degree_centrality_node = max(degree_centrality, key=degree_centrality.get)
    # drawBarchart(list(degree_centrality.keys()), list(degree_centrality.values()))

    betweenness_centrality = nx.betweenness_centrality(network)
    highest_betweenness_centrality_node = max(betweenness_centrality, key=betweenness_centrality.get)
    # drawBarchart(list(betweenness_centrality.keys()), list(betweenness_centrality.values()))

    eigenvector_centrality = nx.eigenvector_centrality(network)
    highest_eigenvector_centrality_node = max(eigenvector_centrality, key=eigenvector_centrality.get)
    # drawBarchart(list(eigenvector_centrality.keys()), list(eigenvector_centrality.values()))

    pagerank_centrality = nx.pagerank(network)
    highest_pagerank_centrality_node = max(pagerank_centrality, key=pagerank_centrality.get)
    # drawBarchart(list(pagerank_centrality.keys()), list(pagerank_centrality.values()))

    print("Degree Centrality", highest_degree_centrality_node)
    print("Betweenness Centrality", highest_betweenness_centrality_node)
    print("Eigen Centrality", highest_eigenvector_centrality_node)
    print("Page rank Centrality", highest_pagerank_centrality_node)

    return getDictValueMean(degree_centrality), getDictValueMean(betweenness_centrality), getDictValueMean(
        eigenvector_centrality), getDictValueMean(pagerank_centrality)


def getFractionOfAppearingAndDisappearing(net_old, net_new):
    net_old_node_set = set(net_old.nodes) #A
    net_new_node_set = set(net_new.nodes) #B

    new_node_set = net_new_node_set.difference(net_old_node_set)
    intersection_set = net_old_node_set.intersection(net_new_node_set)
    removed_nodes_set = net_old_node_set.difference(intersection_set)

    #construct network based on old network
    netG = nx.Graph()
    for node in net_old.nodes:
        netG.add_node(node)

    for edge in net_old.edges:
        netG.add_edge(edge[0], edge[1])

    old_net_nodes_count = len(netG.nodes)
    old_net_edges_count = len(netG.edges)

    #add new node from new network
    for node in new_node_set:
        netG.add_node(node)
    added_node_count = len(new_node_set)

    old_edge_set = set(netG.edges)
    added_edge_count = 0
    for edge in net_new.edges:
        if edge in old_edge_set:
            continue
        else:
            netG.add_edge(edge[0], edge[1])
            added_edge_count+=1

    # remove node from network
    removed_nodes_count = len(removed_nodes_set)
    for node in removed_nodes_set:
        netG.remove_node(node)

    removed_edges_count = (old_net_edges_count + added_edge_count) - len(netG.edges)

    # Calculate the fraction of appearing and disappearing nodes
    fraction_appearing_nodes = added_node_count / old_net_nodes_count
    fraction_disappearing_nodes = removed_nodes_count / old_net_nodes_count
    fraction_appearing_links = added_edge_count / old_net_edges_count
    fraction_disappearing_links = removed_edges_count / old_net_edges_count

    print("Fraction of appearing nodes:", fraction_appearing_nodes)
    print("Fraction of disappearing nodes:", fraction_disappearing_nodes)

    print("Fraction of appearing links:", fraction_appearing_links)
    print("Fraction of disappearing links:", fraction_disappearing_links)


network_1_6_data = getNetworkDataFromCSV('1_6')
network_1_7_data = getNetworkDataFromCSV('1_7')
network_1_8_data = getNetworkDataFromCSV('1_8')

network_1_6 = constructNetwork(network_1_6_data)
network_1_7 = constructNetworkWithoutOutlier(network_1_7_data, deleteOutLierNode(network_1_7_data))
network_1_8 = constructNetworkWithoutOutlier(network_1_8_data, deleteOutLierNode(network_1_8_data))

# print(getSomeBasicMetric(network_1_6))
# print(getSomeBasicMetric(network_1_7))
# print(getSomeBasicMetric(network_1_8))

getFractionOfAppearingAndDisappearing(network_1_7, network_1_8)
