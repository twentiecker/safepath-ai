import joblib
import pandas as pd

model = joblib.load("app/model/risk_model.pkl")


def predict_risk(rainfall, water_level, traffic_density, elevation):
    data = pd.DataFrame(
        [
            {
                "rainfall": rainfall,
                "water_level": water_level,
                "traffic_density": traffic_density,
                "elevation": elevation,
            }
        ]
    )

    prediction = model.predict(data)[0]

    labels = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}

    return labels[prediction]
