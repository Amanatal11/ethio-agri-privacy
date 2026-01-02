import numpy as np
from typing import List, Dict, Any
import logging

class PrivacyEngine:
    """
    Simulates privacy-preserving mechanisms for federated learning in agriculture.
    Implements differential privacy mechanisms for federated learning.
    """
    
    def __init__(self, epsilon: float = 0.1, delta: float = 1e-5):
        self.epsilon = epsilon
        self.delta = delta
        self.logger = logging.getLogger(__name__)

    def add_differential_privacy_noise(self, data: np.ndarray, sensitivity: float = 1.0) -> np.ndarray:
        """
        Adds Laplacian noise to data to achieve epsilon-differential privacy.
        """
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale, data.shape)
        return data + noise

    def simulate_federated_averaging(self, client_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Simulates the Federated Averaging (FedAvg) algorithm.
        Aggregates gradients/insights from multiple 'farms' without raw data exposure.
        """
        if not client_updates:
            return {}

        # Assume updates are dictionaries of numeric features (e.g., yield predictions, soil trends)
        keys = client_updates[0].keys()
        aggregated_update = {}

        for key in keys:
            values = [update[key] for update in client_updates if key in update]
            if values:
                # Aggregate with DP noise
                mean_val = np.mean(values)
                # Sensitivity for mean is 1/N if range is [0,1]
                dp_val = self.add_differential_privacy_noise(np.array([mean_val]), sensitivity=1.0/len(values))[0]
                aggregated_update[key] = float(dp_val)

        return aggregated_update

    def anonymize_local_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts features and anonymizes local data before sharing.
        Removes PII and exact coordinates, keeping only regional/zonal context.
        """
        # Example: Keep 'Zone', 'CropType', but remove 'FarmerName', 'ExactGPS'
        safe_keys = ['zone', 'region', 'soil_ph', 'soil_nitrogen', 'crop_type', 'elevation']
        anonymized = {k: v for k, v in raw_data.items() if k in safe_keys}
        
        # Add noise to sensitive numeric features
        if 'soil_ph' in anonymized:
            anonymized['soil_ph'] = float(self.add_differential_privacy_noise(np.array([anonymized['soil_ph']]), sensitivity=0.5)[0])
            
        return anonymized

# Example usage for verification
if __name__ == "__main__":
    engine = PrivacyEngine(epsilon=0.5)
    
    # Client updates (e.g., predicted yield improvements)
    updates = [
        {"yield_gain": 0.15, "pest_risk": 0.2},
        {"yield_gain": 0.18, "pest_risk": 0.25},
        {"yield_gain": 0.12, "pest_risk": 0.18}
    ]
    
    global_insight = engine.simulate_federated_averaging(updates)
    print(f"Aggregated Global Insight (with DP): {global_insight}")
