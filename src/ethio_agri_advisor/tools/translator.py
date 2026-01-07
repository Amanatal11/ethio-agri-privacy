from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ethio_agri_advisor.config import settings
from typing import Dict

class MultilingualTranslatorTool:
    """
    Translates agricultural recommendations into Amharic and Afaan Oromoo.
    Performs high-quality contextual translation.
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.DEFAULT_MODEL_NAME
        self.llm = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=settings.GOOGLE_API_KEY)
        self.prompt = ChatPromptTemplate.from_template(
            "Translate the following agricultural advice into {language}. "
            "Ensure the tone is helpful and culturally appropriate for Ethiopian smallholders.\n\n"
            "Advice: {text}"
        )

    def translate(self, text: str, target_languages: list = ["Amharic", "Afaan Oromoo"]) -> Dict[str, str]:
        """
        Translates text into multiple languages.
        """
        translations = {}
        for lang in target_languages:
            chain = self.prompt | self.llm
            response = chain.invoke({"language": lang, "text": text})
            translations[lang] = response.content
        return translations

# Example usage
if __name__ == "__main__":
    tool = MultilingualTranslatorTool()
    # print(tool.translate("Plant teff in late June for better yields."))
