import networkx as nx
G = nx.Graph()

G.add_edges_from([(1, 2), (1, 3)])
G.add_node(1)
G.add_edge(1,2) #We technically don't need this as it was added 2 lines above
G.add_node("spam")        # adds node "spam"
G.add_nodes_from("spam")  # adds 4 nodes: 's', 'p', 'a', 'm'
G.add_edge(3, 'm')

print((G.number_of_nodes()))

print((G.number_of_edges()))

G.remove_node(2)
G.remove_nodes_from("spam")
list(G.nodes)
G.remove_edge(1, 3)

G.add_edge(1, 2)
H = nx.DiGraph(G)   # create a DiGraph using the connections from G
list(H.edges())
edgelist = [(0, 1), (1, 2), (2, 3)]
H = nx.Graph(edgelist)

G[1]  # same as G.adj[1]
G[1][2]
G.edges[1, 2]

G.add_edge(1, 3)
G[1][3]['color'] = "blue"
G.edges[1, 2]['color'] = "red"

FG = nx.Graph()
FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2, 4, 1.2), (3, 4, 0.375)])
for n, nbrs in list(FG.adj.items()):
	for nbr, eattr in list(nbrs.items()):
		wt = eattr['weight']
		if wt < 0.5: print(('(%d, %d, %.3f)' % (n, nbr, wt)))

for (u, v, wt) in FG.edges.data('weight'):
	if wt < 0.5: print(('(%d, %d, %.3f)' % (u, v, wt)))

eval(input())