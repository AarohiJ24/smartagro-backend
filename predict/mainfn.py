# app/predict/mainfn.py

import os, sys, json
import pandas as pd

# --- Fix imports so Python can always find predict.* ---
CURRENT_DIR = os.path.dirname(__file__)
APP_DIR = os.path.dirname(CURRENT_DIR)   # parent is "app"
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from predict.rec_model import model   # load model
from predict.weather import get_weather_from_state

# --- Fix dataset path (absolute, not relative) ---
# npk_csv = os.path.join(CURRENT_DIR, "datasets", "state_wise_npk_values.csv")
npk_data = pd.read_csv("predict/datasets/state_wise_npk_values.csv")

def recommend_crop(state: str):
    # Climate
    avg_temp, avg_rain, avg_humidity = get_weather_from_state(state)

    # NPK
    try:
        row = npk_data[npk_data["State/Area"].str.lower() == state.lower()].iloc[0]
    except IndexError:
        return {"error": f"State '{state}' not found in NPK dataset"}

    N, P, K = row["N"], row["P"], row["K"]

    # Prepare input for model
    features = [[N, P, K, avg_temp, avg_humidity, avg_rain]]
    predicted_crop = model.predict(features)[0]

    return {
        "state": state,
        "climate": {
            "temperature": float(avg_temp),
            "rainfall": float(avg_rain),
            "humidity": float(avg_humidity),
        },
        "NPK": {"N": float(N), "P": float(P), "K": float(K)},
        "predicted_crop": str(predicted_crop),
    }

if __name__ == "__main__":
    state = sys.argv[1] if len(sys.argv) > 1 else ""
    result = recommend_crop(state)
    print(json.dumps(result))
