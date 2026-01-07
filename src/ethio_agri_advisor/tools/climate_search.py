from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List, Dict, Any
from datetime import datetime
from ethio_agri_advisor.config import settings

class ClimateSearchTool:
    """
    Retrieves climate and agricultural data specific to Ethiopia.
    Integrates with Tavily for real-time search.
    """
    
    def __init__(self):
        self.search = TavilySearchResults(max_results=3, tavily_api_key=settings.TAVILY_API_KEY)

    def search_agri_data(self, query: str) -> str:
        """
        Searches for Ethiopian agricultural guidelines, weather patterns, or crop resilience.
        """
        current_year = datetime.now().year
        # Enhance query for Ethiopian context
        enhanced_query = f"Ethiopia agriculture {query} climate resilience MoA guidelines {current_year} {current_year + 1}"
        try:
            results = self.search.invoke({"query": enhanced_query})
            
            # Format results
            formatted_results = "\n\n".join([
                f"Source: {res['url']}\nContent: {res['content']}" 
                for res in results
            ])
            return formatted_results
        except Exception as e:
            return f"Error searching data: {e}"

# Example usage
if __name__ == "__main__":
    tool = ClimateSearchTool()
    # print(tool.search_agri_data("drought resistant teff varieties"))
