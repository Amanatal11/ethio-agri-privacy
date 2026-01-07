from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ethio_agri_advisor.tools.climate_search import ClimateSearchTool
from ethio_agri_advisor.tools.yield_simulator import YieldSimulationTool
from ethio_agri_advisor.core.weather_service import WeatherService
from ethio_agri_advisor.config import settings
from typing import Dict, Any

class CropWeatherPlannerAgent:
    """
    Generates agricultural recommendations using aggregated insights and tools.
    Grounds outputs in Ethiopian-specific data.
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.DEFAULT_MODEL_NAME
        self.llm = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=settings.GOOGLE_API_KEY)
        self.search_tool = ClimateSearchTool()
        self.yield_tool = YieldSimulationTool()
        self.weather_service = WeatherService()
        self.prompt = ChatPromptTemplate.from_template(
            "You are a Crop and Weather Planner for Ethiopian smallholders. "
            "Based on the following regional trends and local conditions, provide specific, climate-resilient recommendations. "
            "Focus on: drought-resistant varieties, planting schedules, and irrigation tips.\n\n"
            "Regional Trends: {regional_trends}\n"
            "Local Conditions: {local_summary}\n"
            "Real-time Weather: {weather_data}\n"
            "Search Context: {search_context}\n"
            "Yield Simulation: {yield_sim}"
        )

    def plan(self, local_summary: str, regional_trends: Dict[str, Any], anonymized_features: Dict[str, Any]) -> str:
        """
        Generates a detailed agricultural plan.
        """
        # 1. Search for latest guidelines
        crop_type = anonymized_features.get("crop_type", "teff")
        search_context = self.search_tool.search_agri_data(f"{crop_type} resilience {anonymized_features.get('region', 'Ethiopia')}")
        
        # 2. Get Real-time Weather
        # Default to Addis Ababa if no location provided
        lat = anonymized_features.get("latitude", 9.03)
        lon = anonymized_features.get("longitude", 38.74)
        weather_data = self.weather_service.get_current_weather(lat, lon)
        
        # Calculate average rainfall from forecast for simulation (simplified)
        predicted_rainfall = sum(weather_data.get("daily_rain_sum", [0])) * 10 # Estimate for season based on weekly * 10 (very rough, but dynamic)
        # Or better, use a default if forecast is short term, but let's use the dynamic data to influence it.
        # For simulation, let's assume the user might provide historical rainfall, or we use a standard value adjusted by current weather.
        # Let's use a standard season value but adjust by current drought status if available.
        # For now, we'll use a placeholder logic that uses the dynamic weather to adjust a base value.
        
        base_seasonal_rainfall = 600 # mm
        if sum(weather_data.get("daily_rain_sum", [])) < 10: # Dry week
            base_seasonal_rainfall -= 50
            
        # 3. Run yield simulation
        yield_sim = self.yield_tool.calculate_yield_risk(
            soil_ph=anonymized_features.get("soil_ph", 6.5),
            rainfall_mm=base_seasonal_rainfall,
            crop_type=crop_type
        )
        
        # 4. Generate plan
        chain = self.prompt | self.llm
        response = chain.invoke({
            "regional_trends": regional_trends,
            "local_summary": local_summary,
            "weather_data": weather_data,
            "search_context": search_context,
            "yield_sim": yield_sim
        })
        
        return response.content
