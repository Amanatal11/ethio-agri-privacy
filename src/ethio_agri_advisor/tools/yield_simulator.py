import numpy as np
import json
from typing import Dict, Any
from ethio_agri_advisor.config import settings

class YieldSimulationTool:
    """
    Simulates crop yield and risk based on environmental factors.
    Uses numpy for calculations and dynamic data from JSON.
    """
    
    def __init__(self):
        self.crop_data = self._load_crop_data()

    def _load_crop_data(self) -> Dict[str, Any]:
        """Load crop yield data from JSON file."""
        try:
            with open(settings.CROP_YIELDS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading crop data: {e}")
            return {}

    def calculate_yield_risk(self, soil_ph: float, rainfall_mm: float, crop_type: str) -> Dict[str, Any]:
        """
        Calculates estimated yield and risk score.
        """
        crop_info = self.crop_data.get(crop_type.lower())
        
        if not crop_info:
            # Fallback if crop not found
            base = 20
            optimal_ph_min = 6.0
            optimal_ph_max = 7.5
            water_req = 500
        else:
            base = crop_info.get("base_yield_q_ha", 20)
            optimal_ph_min = crop_info.get("optimal_ph_min", 6.0)
            optimal_ph_max = crop_info.get("optimal_ph_max", 7.5)
            water_req = crop_info.get("water_requirement_mm", 500)
        
        # pH factor
        optimal_ph_avg = (optimal_ph_min + optimal_ph_max) / 2
        ph_factor = 1.0 - abs(soil_ph - optimal_ph_avg) * 0.2
        ph_factor = max(0.5, min(1.0, ph_factor))
        
        # Rainfall factor (simplified)
        rain_factor = 1.0
        if rainfall_mm < water_req: # Drought risk
            rain_factor = rainfall_mm / water_req
        elif rainfall_mm > (water_req * 3): # Flood risk
            rain_factor = 0.7
            
        estimated_yield = base * ph_factor * rain_factor
        risk_score = 1.0 - (ph_factor * rain_factor)
        
        return {
            "estimated_yield_q_ha": round(estimated_yield, 2),
            "risk_score": round(risk_score, 2),
            "status": "High Risk" if risk_score > 0.4 else "Stable",
            "factors": {
                "ph_factor": round(ph_factor, 2),
                "rain_factor": round(rain_factor, 2)
            }
        }

# Example usage
if __name__ == "__main__":
    tool = YieldSimulationTool()
    print(tool.calculate_yield_risk(5.5, 400, "teff"))
