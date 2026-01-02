from typing import TypedDict, List, Dict, Any, Annotated
import operator

class AgentState(TypedDict):
    """
    Represents the state of the multi-agent system.
    """
    # User input
    user_input: str
    
    # Agent outputs
    local_analysis: Dict[str, Any]
    regional_insights: Dict[str, Any]
    recommendation: str
    audit_results: Dict[str, Any]
    final_report: Dict[str, Any]
    
    # Control flow
    iteration_count: int
    max_iterations: int
    status: str # 'analyzing', 'collaborating', 'planning', 'auditing', 'synthesizing', 'rejected'
    
    # History of messages (optional, for tracing)
    messages: Annotated[List[str], operator.add]
