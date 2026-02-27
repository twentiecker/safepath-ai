import random
import networkx as nx
import math
from app.model.predict import predict_risk

RISK_MULTIPLIER = {"LOW": 1, "MEDIUM": 5, "HIGH": 20}
HAZARD_ZONES = [{"lat": -6.205, "lng": 106.804, "radius": 0.002}]


def move_hazard():
    for zone in HAZARD_ZONES:
        zone["lat"] += random.uniform(-0.0005, 0.0005)
        zone["lng"] += random.uniform(-0.0005, 0.0005)


def is_near_hazard(coord):
    lat, lng = coord

    for zone in HAZARD_ZONES:
        distance = math.sqrt((lat - zone["lat"]) ** 2 + (lng - zone["lng"]) ** 2)

        if distance < zone["radius"]:
            return True

    return False


def apply_risk_to_graph(G):
    for u, v, data in G.edges(data=True):

        # Random kondisi tiap jalan
        rainfall = random.randint(0, 150)
        water_level = random.randint(0, 200)
        traffic_density = random.randint(0, 2)
        elevation = random.randint(0, 50)

        risk = predict_risk(rainfall, water_level, traffic_density, elevation)

        multiplier = RISK_MULTIPLIER[risk]

        # cek midpoint edge
        lat1, lng1 = G.nodes[u]["pos"]
        lat2, lng2 = G.nodes[v]["pos"]

        midpoint = ((lat1 + lat2) / 2, (lng1 + lng2) / 2)

        if is_near_hazard(midpoint):
            print(f"Edge {u}-{v} terkena hazard zone!")
            multiplier *= 2  # penalty besar

        final_weight = data["distance"] * multiplier

        data["weight"] = final_weight
        data["risk"] = risk

        print(f"Edge {u}-{v} | Risk: {risk} | Weight: {final_weight}")

    return G


def calculate_total_risk(G, path):
    total = 0
    risk_details = []

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]

        edge_data = G[u][v]
        total += edge_data["weight"]

        risk_details.append(
            {
                "from": u,
                "to": v,
                "risk": edge_data["risk"],
                "weight": edge_data["weight"],
            }
        )

    return total, risk_details


def classify_total_risk(total_risk):
    if total_risk < 20:
        return "LOW"
    elif total_risk < 50:
        return "MEDIUM"
    else:
        return "HIGH"


def find_shortest_path(G, start, end):
    return nx.shortest_path(G, start, end, weight="distance")


def find_safest_path(G, start, end):
    path = nx.astar_path(G, start, end, weight="weight")
    return path


def get_path_coordinates(G, path):
    coords = []
    for node in path:
        coords.append(G.nodes[node]["pos"])
    return coords
