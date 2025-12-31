from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List, Dict, Any

class ClimateSearchTool:
    """
    Retrieves climate and agricultural data specific to Ethiopia.
    Integrates with Tavily for real-time search.
    """
    
    def __init__(self):
        self.search = TavilySearchResults(max_results=3)

    def search_agri_data(self, query: str) -> str:
        """
        Searches for Ethiopian agricultural guidelines, weather patterns, or crop resilience.
        """
        # Augment query for better Ethiopian context
        enhanced_query = f"Ethiopia agriculture {query} climate resilience MoA guidelines 2024 2025"
        results = self.search.invoke({"query": enhanced_query})
        
        # Format results for the agent
        formatted_results = "\n\n".join([
            f"Source: {res['url']}\nContent: {res['content']}" 
            for res in results
        ])
        return formatted_results

# Example usage
if __name__ == "__main__":
    tool = ClimateSearchTool()
    # print(tool.search_agri_data("drought resistant teff varieties"))
