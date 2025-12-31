from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict

class MultilingualTranslatorTool:
    """
    Translates agricultural recommendations into Amharic and Afaan Oromoo.
    Uses LLM for high-quality contextual translation.
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name)
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
