from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ethio_agri_advisor.tools.translator import MultilingualTranslatorTool
from ethio_agri_advisor.config import settings
from typing import Dict, Any

class SynthesizerAgent:
    """
    Compiles the final farmer-friendly report.
    Supports multilingual output.
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.DEFAULT_MODEL_NAME
        self.llm = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=settings.GOOGLE_API_KEY)
        self.translator = MultilingualTranslatorTool()
        self.prompt = ChatPromptTemplate.from_template(
            "You are a Master Synthesizer for Ethiopian agricultural advice. "
            "Compile the following recommendation into a farmer-friendly report. "
            "Include a clear summary, action items, and a confidence score (0-100%).\n\n"
            "Recommendation: {recommendation}\n"
            "Audit Status: {audit_status}"
        )

    def synthesize(self, recommendation: str, audit_status: str) -> Dict[str, Any]:
        """
        Compiles the final report and translates it.
        """
        chain = self.prompt | self.llm
        report = chain.invoke({
            "recommendation": recommendation,
            "audit_status": audit_status
        })
        
        english_report = report.content
        
        # Translate to local languages
        translations = self.translator.translate(english_report)
        
        return {
            "english_report": english_report,
            "translations": translations,
            "status": "Finalized"
        }
