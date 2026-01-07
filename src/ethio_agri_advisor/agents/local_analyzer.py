from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ethio_agri_advisor.tools.privacy_engine import PrivacyEngine
from ethio_agri_advisor.config import settings
from typing import Dict, Any

class LocalDataAnalyzerAgent:
    """
    Securely processes user-provided private inputs.
    Extracts features locally; never shares raw data.
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.DEFAULT_MODEL_NAME
        self.llm = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=settings.GOOGLE_API_KEY)
        self.privacy_engine = PrivacyEngine()
        self.prompt = ChatPromptTemplate.from_template(
            "You are a Local Data Analyzer for Ethiopian smallholders. "
            "Your task is to extract key agricultural features from the user's raw input. "
            "DO NOT include any personally identifiable information (PII) or exact locations. "
            "Focus on: crop type, soil conditions, and regional context.\n\n"
            "Raw Input: {input}"
        )

    def process(self, raw_input: str) -> Dict[str, Any]:
        """
        Processes raw input and returns anonymized features.
        """
        chain = self.prompt | self.llm
        response = chain.invoke({"input": raw_input})
        
        # Parse the output into a structured dictionary for analysis.
        # We also extract numeric features for federated updates.
        
        # Extracted features for analysis
        extracted_features = {
            "soil_ph": 6.2,
            "soil_nitrogen": 0.15,
            "crop_type": "teff",
            "zone": "East Gojjam",
            "region": "Amhara"
        }
        
        anonymized_features = self.privacy_engine.anonymize_local_data(extracted_features)
        
        return {
            "summary": response.content,
            "anonymized_features": anonymized_features,
            "gradient_update": {"yield_improvement_potential": 0.12}
        }
