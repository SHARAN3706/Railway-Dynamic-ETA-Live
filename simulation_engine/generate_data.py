import pandas as pd
import numpy as np

def generate_railway_dataset(num_samples=10000):
    np.random.seed(42)
    
    # Corridor: MAS (Chennai Central) to SBC (Bangalore City) ~ 360 km
    stations = ["MAS", "AJJ", "KPD", "JTJ", "BWT", "KJM", "SBC"]
    distances = [0, 68, 130, 214, 290, 345, 360]  # Cumulative KM
    
    data = []
    
    for _ in range(num_samples):
        current_stn_idx = np.random.randint(0, len(stations) - 1)
        next_stn_idx = current_stn_idx + 1
        
        distance_to_next = distances[next_stn_idx] - distances[current_stn_idx]
        current_speed = np.random.uniform(40, 110) # km/h
        
        # Ground-reality dynamic factors
        preceding_train_gap = np.random.uniform(2.0, 25.0) # km gap
        signal_aspect = np.random.choice([0, 1, 2], p=[0.1, 0.2, 0.7]) # 0: Red/Caution, 1: Yellow, 2: Green
        downstream_congestion_index = np.random.uniform(0.1, 1.0) # 1.0 = heavy traffic
        weather_impact_score = np.random.choice([1.0, 1.2, 1.5], p=[0.7, 0.2, 0.1]) # 1.0 = clear, 1.5 = heavy fog/rain
        temporary_speed_restriction = np.random.choice([30, 50, 80, 110], p=[0.1, 0.15, 0.25, 0.5])
        
        # Dynamic base transit calculation
        effective_speed = min(current_speed, temporary_speed_restriction)
        if preceding_train_gap < 5.0 or signal_aspect < 2:
            effective_speed = effective_speed * 0.6
            
        base_time_mins = (distance_to_next / effective_speed) * 60
        
        # Ground reality actual arrival time calculation
        actual_transit_time = (base_time_mins * weather_impact_score) + (downstream_congestion_index * 15) + np.random.normal(2, 1)
        
        data.append({
            "distance_km": distance_to_next,
            "current_speed": round(current_speed, 2),
            "preceding_gap_km": round(preceding_train_gap, 2),
            "signal_aspect": signal_aspect,
            "congestion_index": round(downstream_congestion_index, 2),
            "weather_impact": weather_impact_score,
            "speed_restriction": temporary_speed_restriction,
            "actual_time_mins": round(actual_transit_time, 2)
        })
        
    df = pd.DataFrame(data)
    df.to_csv("train_telemetry_dataset.csv", index=False)
    print(">>> Success: train_telemetry_dataset.csv created with 10,000 telemetry samples!")

if __name__ == "__main__":
    generate_railway_dataset()