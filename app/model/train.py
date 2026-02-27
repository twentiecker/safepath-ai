import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ==============================
# 1. Generate Dummy Dataset
# ==============================

np.random.seed(42)
data_size = 1000

rainfall = np.random.randint(0, 150, data_size)  # mm
water_level = np.random.randint(0, 200, data_size)  # cm
traffic_density = np.random.randint(0, 3, data_size)  # 0=low,1=medium,2=high
elevation = np.random.randint(0, 100, data_size)  # meter

# Risk logic (simulasi sederhana)
risk = []
for r, w, t, e in zip(rainfall, water_level, traffic_density, elevation):
    score = r * 0.3 + w * 0.4 + t * 10 - e * 0.2
    if score < 50:
        risk.append(0)  # LOW
    elif score < 100:
        risk.append(1)  # MEDIUM
    else:
        risk.append(2)  # HIGH

df = pd.DataFrame(
    {
        "rainfall": rainfall,
        "water_level": water_level,
        "traffic_density": traffic_density,
        "elevation": elevation,
        "risk": risk,
    }
)

# ==============================
# 2. Split Data
# ==============================

X = df.drop("risk", axis=1)
y = df["risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==============================
# 3. Train Model
# ==============================

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# ==============================
# 4. Evaluate Model
# ==============================

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# ==============================
# 5. Save Model
# ==============================

joblib.dump(model, "risk_model.pkl")
print("Model saved as risk_model.pkl")
