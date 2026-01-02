from langgraph.graph import StateGraph, END
from ethio_agri_advisor.core.state import AgentState
from ethio_agri_advisor.agents.local_analyzer import LocalDataAnalyzerAgent
from ethio_agri_advisor.agents.federated_collaborator import FederatedCollaboratorAgent
from ethio_agri_advisor.agents.crop_planner import CropWeatherPlannerAgent
from ethio_agri_advisor.agents.privacy_auditor import PrivacyAuditorAgent
from ethio_agri_advisor.agents.synthesizer import SynthesizerAgent
from typing import Dict, Any

class AgriAdvisorGraph:
    """
    Orchestrates the multi-agent flow using LangGraph.
    """
    
    def __init__(self):
        self.local_analyzer = LocalDataAnalyzerAgent()
        self.federated_collaborator = FederatedCollaboratorAgent()
        self.crop_planner = CropWeatherPlannerAgent()
        self.privacy_auditor = PrivacyAuditorAgent()
        self.synthesizer = SynthesizerAgent()
        
        self.workflow = StateGraph(AgentState)
        self._build_graph()

    def _build_graph(self):
        # Define Nodes
        self.workflow.add_node("local_analysis", self.node_local_analysis)
        self.workflow.add_node("federated_collaboration", self.node_federated_collaboration)
        self.workflow.add_node("crop_planning", self.node_crop_planning)
        self.workflow.add_node("privacy_audit", self.node_privacy_audit)
        self.workflow.add_node("synthesis", self.node_synthesis)

        # Define Edges
        self.workflow.set_entry_point("local_analysis")
        self.workflow.add_edge("local_analysis", "federated_collaboration")
        self.workflow.add_edge("federated_collaboration", "crop_planning")
        self.workflow.add_edge("crop_planning", "privacy_audit")
        
        # Conditional Edge: If audit fails, loop back to planning (debate/refine)
        self.workflow.add_conditional_edges(
            "privacy_audit",
            self.should_continue,
            {
                "continue": "synthesis",
                "refine": "crop_planning",
                "end": END
            }
        )
        
        self.workflow.add_edge("synthesis", END)
        
        self.app = self.workflow.compile()

    # Node Functions
    def node_local_analysis(self, state: AgentState) -> Dict[str, Any]:
        print("--- Node: Local Analysis ---")
        result = self.local_analyzer.process(state["user_input"])
        return {
            "local_analysis": result,
            "status": "collaborating",
            "messages": ["Local analysis complete. Features anonymized."]
        }

    def node_federated_collaboration(self, state: AgentState) -> Dict[str, Any]:
        print("--- Node: Federated Collaboration ---")
        local_update = state["local_analysis"]["gradient_update"]
        result = self.federated_collaborator.aggregate_insights(local_update)
        return {
            "regional_insights": result,
            "status": "planning",
            "messages": ["Federated aggregation complete. Regional trends extracted."]
        }

    def node_crop_planning(self, state: AgentState) -> Dict[str, Any]:
        print("--- Node: Crop Planning ---")
        result = self.crop_planner.plan(
            local_summary=state["local_analysis"]["summary"],
            regional_trends=state["regional_insights"]["regional_trends"],
            anonymized_features=state["local_analysis"]["anonymized_features"]
        )
        return {
            "recommendation": result,
            "status": "auditing",
            "messages": ["Crop plan generated based on regional and local data."]
        }

    def node_privacy_audit(self, state: AgentState) -> Dict[str, Any]:
        print("--- Node: Privacy Audit ---")
        result = self.privacy_auditor.audit(state["recommendation"])
        return {
            "audit_results": result,
            "iteration_count": state.get("iteration_count", 0) + 1,
            "messages": [f"Audit complete: {result['decision']}"]
        }

    def node_synthesis(self, state: AgentState) -> Dict[str, Any]:
        print("--- Node: Synthesis ---")
        result = self.synthesizer.synthesize(
            recommendation=state["recommendation"],
            audit_status=state["audit_results"]["decision"]
        )
        return {
            "final_report": result,
            "status": "finalized",
            "messages": ["Final report synthesized and translated."]
        }

    # Conditional Logic
    def should_continue(self, state: AgentState) -> str:
        if state["audit_results"]["is_approved"]:
            return "continue"
        elif state.get("iteration_count", 0) < state.get("max_iterations", 3):
            print("--- Audit Failed: Refining Plan ---")
            return "refine"
        else:
            print("--- Audit Failed: Max Iterations Reached ---")
            return "end"

# Example usage
if __name__ == "__main__":
    graph = AgriAdvisorGraph()
    # app = graph.app
