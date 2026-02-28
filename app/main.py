from fastapi import FastAPI
from app.routing.graph import create_graph
from app.routing.risk_routing import (
    HAZARD_ZONES,
    move_hazard,
    apply_risk_to_graph,
    calculate_total_risk,
    classify_total_risk,
    find_safest_path,
    find_shortest_path,
    get_path_coordinates,
)
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

ENV = os.getenv("ENV", "development")
CORS_SETTINGS = {
    "development": ["http://localhost:5173"],
    "production": ["https://safepath-ai-pi.vercel.app"],
}

allowed_origins = CORS_SETTINGS.get(ENV, [])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

print("Current ENV:", ENV)
print("Allowed origins:", allowed_origins)


@app.get("/")
def root():
    return {"message": "SafePath AI is running 🚀"}


G = create_graph()


@app.post("/evacuate")
def evacuate(start: str, end: str):
    move_hazard()

    G_with_risk = apply_risk_to_graph(G)

    shortest_path = find_shortest_path(G_with_risk, start, end)
    shortest_coords = get_path_coordinates(G_with_risk, shortest_path)
    shortest_total_risk, _ = calculate_total_risk(G_with_risk, shortest_path)
    shortest_risk_level = classify_total_risk(shortest_total_risk)

    safest_path = find_safest_path(G_with_risk, start, end)
    safest_coords = get_path_coordinates(G_with_risk, safest_path)
    safest_total_risk, safest_risk_details = calculate_total_risk(
        G_with_risk, safest_path
    )
    safest_risk_level = classify_total_risk(safest_total_risk)

    return {
        "hazards": HAZARD_ZONES,
        "shortest_path": shortest_path,
        "shortest_coords": shortest_coords,
        "shortest_total_risk": shortest_total_risk,
        "shortest_risk_level": shortest_risk_level,
        "safest_path": safest_path,
        "safest_coords": safest_coords,
        "safest_total_risk": safest_total_risk,
        "safest_risk_level": safest_risk_level,
        "safest_risk_breakdown": safest_risk_details,
    }
