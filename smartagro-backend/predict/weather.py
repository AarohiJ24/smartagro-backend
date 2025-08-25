import requests
import pandas as pd

# --- Step 2: Load NPK dataset ---
npk_data = pd.read_csv("predict/datasets/state_wise_npk_values.csv")
def get_weather_from_state(state):
    # Use Open-Meteo Geocoding API to get lat/lon for the state
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={state}&count=1&language=en&format=json&country=IN"
    geo_resp = requests.get(geo_url).json()
    if "results" not in geo_resp or len(geo_resp["results"]) == 0:
        raise ValueError(f"Could not find coordinates for {state}")

    lat = geo_resp["results"][0]["latitude"]
    lon = geo_resp["results"][0]["longitude"]

    # Request **daily** climate data
    url = (
        "https://climate-api.open-meteo.com/v1/climate?"
        f"latitude={lat}&longitude={lon}"
        "&start_date=2020-01-01&end_date=2024-12-31"
        "&models=MRI_AGCM3_2_S"
        "&daily=temperature_2m_mean,precipitation_sum,relative_humidity_2m_mean&timezone=auto"
    )
    data = requests.get(url).json()

    # Convert to DataFrame
    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temp": data["daily"]["temperature_2m_mean"],
        "rain": data["daily"]["precipitation_sum"],
        "humidity": data["daily"]["relative_humidity_2m_mean"]
    })

    # Monthly averages
    df["date"] = pd.to_datetime(df["date"])
    monthly = df.groupby(df["date"].dt.to_period("M")).agg({
        "temp": "mean",
        "rain": "sum",
        "humidity": "mean"
    }).reset_index()

# Take averages for prediction
    avg_temp = monthly["temp"].mean()
    avg_rain = monthly["rain"].mean()
    avg_humidity = monthly["humidity"].mean()

    return avg_temp, avg_rain, avg_humidity




# Example usage
# if __name__ == "__main__":
#     data = get_weather_from_state("Punjab")
#     print("Sample monthly data:", {k: v[:5] if isinstance(v, list) else v for k, v in data["monthly"].items()})
