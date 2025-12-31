from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools.translator import MultilingualTranslatorTool
from typing import Dict, Any

class SynthesizerAgent:
    """
    Agent 5: Compiles final farmer-friendly report.
    Supports multilingual output.
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name)
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
