import networkx as nx
import random


# def create_graph():
#     G = nx.Graph()

#     # Tambah node + koordinat (simulasi kota kecil)
#     G.add_node("A", pos=(-6.200, 106.800))
#     G.add_node("B", pos=(-6.201, 106.805))
#     G.add_node("C", pos=(-6.205, 106.802))
#     G.add_node("D", pos=(-6.207, 106.807))
#     G.add_node("E", pos=(-6.210, 106.810))

#     # Edge dengan jarak
#     G.add_edge("A", "B", distance=5)
#     G.add_edge("A", "C", distance=10)
#     G.add_edge("B", "D", distance=3)
#     G.add_edge("C", "D", distance=4)
#     G.add_edge("D", "E", distance=6)

#     return G


def create_graph():
    G = nx.Graph()

    base_lat = -6.200
    base_lon = 106.800
    node_count = 25

    # Generate nodes
    for i in range(node_count):
        node_name = f"N{i}"
        lat = base_lat + random.uniform(-0.02, 0.02)
        lon = base_lon + random.uniform(-0.02, 0.02)
        G.add_node(node_name, pos=(lat, lon))

    # Generate edges
    nodes = list(G.nodes())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if random.random() < 0.2:
                distance = random.randint(1, 15)
                G.add_edge(nodes[i], nodes[j], distance=distance)

    # Forced to connect
    while not nx.is_connected(G):
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u != v:
            G.add_edge(u, v, distance=random.randint(1, 15))

    return G
