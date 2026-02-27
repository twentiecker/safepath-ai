import networkx as nx


def create_graph():
    G = nx.Graph()

    # Tambah node + koordinat (simulasi kota kecil)
    G.add_node("A", pos=(-6.200, 106.800))
    G.add_node("B", pos=(-6.201, 106.805))
    G.add_node("C", pos=(-6.205, 106.802))
    G.add_node("D", pos=(-6.207, 106.807))
    G.add_node("E", pos=(-6.210, 106.810))

    # Edge dengan jarak
    G.add_edge("A", "B", distance=5)
    G.add_edge("A", "C", distance=10)
    G.add_edge("B", "D", distance=3)
    G.add_edge("C", "D", distance=4)
    G.add_edge("D", "E", distance=6)

    return G
