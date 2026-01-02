import numpy as np
from typing import Dict, Any

class YieldSimulationTool:
    """
    Simulates crop yield and risk based on environmental factors.
    Uses numpy for calculations.
    """

    def calculate_yield_risk(self, soil_ph: float, rainfall_mm: float, crop_type: str) -> Dict[str, Any]:
        """
        Calculates estimated yield and risk score.
        Simplified model for demonstration.
        """
        # Base yields (quintals per hectare)
        base_yields = {
            "teff": 15,
            "maize": 40,
            "sorghum": 25
        }
        
        base = base_yields.get(crop_type.lower(), 20)
        
        # pH factor (optimal 6.0 - 7.5)
        ph_factor = 1.0 - abs(soil_ph - 6.75) * 0.2
        ph_factor = max(0.5, min(1.0, ph_factor))
        
        # Rainfall factor (simplified)
        rain_factor = 1.0
        if rainfall_mm < 500: # Drought risk
            rain_factor = rainfall_mm / 500
        elif rainfall_mm > 1500: # Flood risk
            rain_factor = 0.7
            
        estimated_yield = base * ph_factor * rain_factor
        risk_score = 1.0 - (ph_factor * rain_factor)
        
        return {
            "estimated_yield_q_ha": round(estimated_yield, 2),
            "risk_score": round(risk_score, 2),
            "status": "High Risk" if risk_score > 0.4 else "Stable"
        }

# Example usage
if __name__ == "__main__":
    tool = YieldSimulationTool()
    print(tool.calculate_yield_risk(5.5, 400, "teff"))
