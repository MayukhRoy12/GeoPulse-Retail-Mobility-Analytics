import os
import numpy as np
import pandas as pd


RETAIL_ZONES = {
    "Indiranagar": (12.9719, 77.6412),
    "Koramangala": (12.9352, 77.6245),
    "MG Road": (12.9748, 77.6094),
    "Whitefield": (12.9698, 77.7500),
    "Electronic City": (12.8452, 77.6602),
}

STORE_CATEGORIES = {
    "Grocery": (18, 6, 850),
    "Apparel": (38, 12, 2400),
    "Electronics": (28, 10, 5200),
    "Cafe & Dining": (52, 18, 1100),
    "Pharmacy": (10, 4, 480),
}

HOUR_WEIGHTS = np.array([
    0.005, 0.003, 0.002, 0.002, 0.003, 0.008,
    0.015, 0.025, 0.040, 0.055, 0.065, 0.075,
    0.085, 0.080, 0.065, 0.060, 0.070, 0.085,
    0.095, 0.080, 0.045, 0.020, 0.010, 0.007,
])
HOUR_WEIGHTS = HOUR_WEIGHTS / HOUR_WEIGHTS.sum()


def generate_mobility_dataset(num_records=5000, seed=42, output_path="data/raw/retail_mobility_sample.csv"):
    rng = np.random.default_rng(seed)
    zone_names = list(RETAIL_ZONES.keys())
    category_names = list(STORE_CATEGORIES.keys())

    chosen_zones = rng.choice(zone_names, size=num_records, p=[0.24, 0.23, 0.18, 0.19, 0.16])
    chosen_categories = rng.choice(category_names, size=num_records, p=[0.28, 0.22, 0.12, 0.24, 0.14])

    base_dates = pd.date_range(end="2026-11-24", periods=30, freq="D")
    day_weights = np.array([1.35 if d.weekday() >= 5 else 1.0 for d in base_dates])
    day_weights = day_weights / day_weights.sum()

    sampled_days = rng.choice(base_dates, size=num_records, p=day_weights)
    sampled_hours = rng.choice(np.arange(24), size=num_records, p=HOUR_WEIGHTS)
    sampled_minutes = rng.integers(0, 60, size=num_records)

    timestamps = [
        pd.Timestamp(day) + pd.Timedelta(hours=int(hr), minutes=int(mn))
        for day, hr, mn in zip(sampled_days, sampled_hours, sampled_minutes)
    ]

    latitudes = np.empty(num_records)
    longitudes = np.empty(num_records)
    dwell_times = np.empty(num_records)
    spend_inr = np.empty(num_records)

    for i in range(num_records):
        base_lat, base_lon = RETAIL_ZONES[chosen_zones[i]]
        latitudes[i] = round(base_lat + rng.normal(0, 0.0045), 6)
        longitudes[i] = round(base_lon + rng.normal(0, 0.0045), 6)

        mean_dwell, std_dwell, base_spend = STORE_CATEGORIES[chosen_categories[i]]
        dwell = max(3.0, rng.normal(mean_dwell, std_dwell))
        dwell_times[i] = round(dwell, 1)
        spend_factor = dwell / mean_dwell
        spend_inr[i] = round(max(100.0, rng.normal(base_spend * spend_factor, base_spend * 0.25)), 2)

    visitor_types = rng.choice(["Returning", "First-Time"], size=num_records, p=[0.62, 0.38])

    df = pd.DataFrame({
        "timestamp": timestamps,
        "retail_zone": chosen_zones,
        "store_category": chosen_categories,
        "latitude": latitudes,
        "longitude": longitudes,
        "dwell_time_minutes": dwell_times,
        "estimated_spend_inr": spend_inr,
        "visitor_type": visitor_types,
    })

    df = df.sort_values("timestamp").reset_index(drop=True)
    df.insert(0, "event_id", [f"GP-{i + 1:06d}" for i in range(len(df))])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records at {output_path}")
    return df


if __name__ == "__main__":
    generate_mobility_dataset()
