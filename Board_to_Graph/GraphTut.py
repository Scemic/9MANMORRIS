import networkx as nx
G = nx.Graph()
G.add_node(1)
G.add_nodes_from([2, 3])

H = nx.path_graph(10)
G.add_nodes_from([2,3])

H = nx.path_graph(10)
G.add_nodes_from(H)

G.add_node(H)

G.add_edge(1, 2)
e = (2,3)
G.add_edge(*e)

G.add_edges_from([(1, 2), (1, 3)])

G.add_edges_from(H.edges)

G.clear()


import networkx as nx
G = nx.Graph()

G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1, 2)
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')

print((G.number_of_nodes()))

print((G.number_of_edges()))

eval(input())