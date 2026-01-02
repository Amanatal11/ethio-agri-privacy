import os
from dotenv import load_dotenv
from ethio_agri_advisor.core.graph import AgriAdvisorGraph

# Load environment variables (API keys)
load_dotenv()

def run_advisor_demo():
    """
    Runs a demo of the Privacy-Preserving Multi-Agent Climate-Resilient Farming Advisor.
    """
    print("="*60)
    print("ETHIOPIAN CLIMATE-RESILIENT FARMING ADVISOR (PRIVACY-PRESERVING)")
    print("="*60)
    
    # Initialize the graph
    advisor = AgriAdvisorGraph()
    
    # Sample user input (hypothetical farm data)
    # Note: The system will anonymize this and only share aggregated insights.
    user_input = (
        "I am a farmer in East Gojjam, Amhara. I have 2 hectares of land. "
        "The soil is slightly acidic. I usually plant Teff, but last season was very dry. "
        "My name is Abebe and my phone is +251911223344. My farm is at 10.3292, 37.8742."
    )
    
    print(f"\n[User Input]: {user_input}\n")
    
    # Initial state
    initial_state = {
        "user_input": user_input,
        "iteration_count": 0,
        "max_iterations": 3,
        "messages": ["Starting advisor session..."]
    }
    
    # Run the graph
    final_state = advisor.app.invoke(initial_state)
    
    print("\n" + "="*60)
    print("FINAL RECOMMENDATION REPORT")
    print("="*60)
    print(f"\n{final_state['final_report']['english_report']}")
    
    print("\n" + "="*60)
    print("MULTILINGUAL OUTPUTS")
    print("="*60)
    for lang, translation in final_state['final_report']['translations'].items():
        print(f"\n[{lang}]:\n{translation}")
        
    print("\n" + "="*60)
    print("PRIVACY & AUDIT LOGS")
    print("="*60)
    print(f"Audit Decision: {final_state['audit_results']['decision']}")
    print(f"Audit Rationale: {final_state['audit_results']['audit_log']}")
    print(f"Detected Leaks in Final Output: {final_state['audit_results']['tool_audit']['detected_leaks']}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment. Please set it in .env file.")
    elif not os.getenv("TAVILY_API_KEY"):
        print("Error: TAVILY_API_KEY not found in environment. Please set it in .env file.")
    else:
        run_advisor_demo()
