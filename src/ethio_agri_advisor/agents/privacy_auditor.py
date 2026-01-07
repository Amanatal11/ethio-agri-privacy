from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from ethio_agri_advisor.tools.privacy_audit import PrivacyAuditTool
from ethio_agri_advisor.config import settings
from typing import Dict, Any, List

class PrivacyAuditorAgent:
    """
    Monitors data flows for privacy leaks, bias, or ungrounded claims.
    Flags/intervenes if necessary.
    """
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.DEFAULT_MODEL_NAME
        self.llm = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=settings.GOOGLE_API_KEY)
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
        
        # 2. Ethical audit
        chain = self.prompt | self.llm
        response = chain.invoke({"recommendation": recommendation})
        
        is_approved = tool_result["is_safe"] and "approve" in response.content.lower()
        
        return {
            "is_approved": is_approved,
            "audit_log": response.content,
            "tool_audit": tool_result,
            "decision": "APPROVED" if is_approved else "REJECTED"
        }
