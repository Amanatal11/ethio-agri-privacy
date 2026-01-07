import requests
from typing import Dict, Any, Optional
from ethio_agri_advisor.config import settings

class WeatherService:
    """
    Service to fetch weather data from Open-Meteo API.
    """
    
    def __init__(self):
        self.base_url = settings.WEATHER_API_BASE_URL

    def get_current_weather(self, lat: float = 9.03, lon: float = 38.74) -> Dict[str, Any]:
        """
        Get current weather and forecast for a location (default: Addis Ababa).
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing weather data.
        """
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
                "hourly": "temperature_2m,relativehumidity_2m,rain",
                "daily": "temperature_2m_max,temperature_2m_min,rain_sum",
                "timezone": "auto"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "current_temp": data.get("current_weather", {}).get("temperature"),
                "wind_speed": data.get("current_weather", {}).get("windspeed"),
                "daily_rain_sum": data.get("daily", {}).get("rain_sum", [])[:7], # Next 7 days
                "max_temp_forecast": data.get("daily", {}).get("temperature_2m_max", [])[:7],
                "min_temp_forecast": data.get("daily", {}).get("temperature_2m_min", [])[:7]
            }
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            # Fallback to historical averages for Ethiopia (Addis Ababa context)
            return {
                "current_temp": 20.0,
                "wind_speed": 10.0,
                "daily_rain_sum": [5.0] * 7, # Moderate rain assumption
                "max_temp_forecast": [25.0] * 7,
                "min_temp_forecast": [10.0] * 7,
                "note": "Data fetched from fallback (historical averages) due to API error."
            }

if __name__ == "__main__":
    service = WeatherService()
    print(service.get_current_weather())
