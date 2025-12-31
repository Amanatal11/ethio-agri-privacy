from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools.climate_search import ClimateSearchTool
from tools.yield_simulator import YieldSimulationTool
from typing import Dict, Any

class CropWeatherPlannerAgent:
    """
    Agent 3: Uses aggregated insights + tools to generate recommendations.
    Grounds outputs in Ethiopian-specific data.
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name)
        self.search_tool = ClimateSearchTool()
        self.yield_tool = YieldSimulationTool()
        self.prompt = ChatPromptTemplate.from_template(
            "You are a Crop and Weather Planner for Ethiopian smallholders. "
            "Based on the following regional trends and local conditions, provide specific, climate-resilient recommendations. "
            "Focus on: drought-resistant varieties, planting schedules, and irrigation tips.\n\n"
            "Regional Trends: {regional_trends}\n"
            "Local Conditions: {local_summary}\n"
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
        
        # 2. Run yield simulation
        yield_sim = self.yield_tool.calculate_yield_risk(
            soil_ph=anonymized_features.get("soil_ph", 6.5),
            rainfall_mm=600, # Mocked for now
            crop_type=crop_type
        )
        
        # 3. Generate plan
        chain = self.prompt | self.llm
        response = chain.invoke({
            "regional_trends": regional_trends,
            "local_summary": local_summary,
            "search_context": search_context,
            "yield_sim": yield_sim
        })
        
        return response.content
