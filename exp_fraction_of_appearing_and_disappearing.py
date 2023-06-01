import random

import networkx as nx

# Create a network object
G = nx.Graph()

# Add nodes to the network
for i in range(10):
    G.add_node(i)

for i in range(15):
    u =random.randint(0, 9)
    v = random.randint(0, 9)
    # print(u, v)
    G.add_edge(u, v)

print(G.nodes)
print(len(G.edges()))

# Remove nodes from the network
for i in range(5):
    G.remove_node(i)

for i in range(10, 14):
    G.add_node(i)

for i in range(2):
    u =random.randint(10, 13)
    v = random.randint(10, 13)
    # print(u, v)
    G.add_edge(u, v)


print(G.nodes)
print(len(G.edges()))
# Calculate the fraction of appearing and disappearing nodes
fraction_appearing = len(G.nodes()) / 10
fraction_disappearing = 5 / 10

print("Fraction of appearing nodes:", fraction_appearing)
print("Fraction of disappearing nodes:", fraction_disappearing)


# # Create two sets
# A = [1, 2, 3, 4]
# B = [2, 4, 5, 6]
#
# # Find the set subtraction of A and B using the difference() method
# new_node_set = set(B).difference(set(A))
# intersection_set = set(A).intersection(set(B))
#
# removed_nodes_set = set(A).difference(intersection_set)
#
# # Print the set subtraction
# print(removed_nodes_set)
# print(new_node_set)


