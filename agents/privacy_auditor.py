from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tools.privacy_audit import PrivacyAuditTool
from typing import Dict, Any, List

class PrivacyAuditorAgent:
    """
    Agent 4: Monitors all flows for privacy leaks, bias, or ungrounded claims.
    Flags/intervenes if necessary.
    """
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name)
        self.audit_tool = PrivacyAuditTool()
        self.prompt = ChatPromptTemplate.from_template(
            "You are a Privacy and Ethics Auditor for an Ethiopian agricultural advisor system. "
            "Review the following proposed recommendation for privacy leaks (PII, exact GPS) and ethical alignment (cultural sensitivity, over-promising). "
            "If you find issues, provide a rejection reason. Otherwise, approve it.\n\n"
            "Recommendation: {recommendation}"
        )

    def audit(self, recommendation: str) -> Dict[str, Any]:
        """
        Audits the recommendation and returns status.
        """
        # 1. Tool-based audit
        tool_result = self.audit_tool.audit_content(recommendation)
        
        # 2. LLM-based ethical audit
        chain = self.prompt | self.llm
        response = chain.invoke({"recommendation": recommendation})
        
        is_approved = tool_result["is_safe"] and "approve" in response.content.lower()
        
        return {
            "is_approved": is_approved,
            "audit_log": response.content,
            "tool_audit": tool_result,
            "decision": "APPROVED" if is_approved else "REJECTED"
        }
