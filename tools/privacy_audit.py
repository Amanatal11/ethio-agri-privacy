import re
from typing import List, Dict, Any

class PrivacyAuditTool:
    """
    Monitors inter-agent communication for potential privacy leaks or ungrounded claims.
    """

    def audit_content(self, content: str, private_keys: List[str] = ["name", "phone", "gps", "coordinates"]) -> Dict[str, Any]:
        """
        Checks if any sensitive keys or patterns are present in the content.
        """
        leaks = []
        for key in private_keys:
            if re.search(rf"\b{key}\b", content, re.IGNORECASE):
                leaks.append(key)
        
        # Check for coordinate-like patterns
        coord_pattern = r"\d{1,2}\.\d{4,},\s?\d{1,2}\.\d{4,}"
        if re.search(coord_pattern, content):
            leaks.append("exact_coordinates")

        is_safe = len(leaks) == 0
        return {
            "is_safe": is_safe,
            "detected_leaks": leaks,
            "recommendation": "Proceed" if is_safe else "REJECT: Potential data exposure detected."
        }

# Example usage
if __name__ == "__main__":
    tool = PrivacyAuditTool()
    print(tool.audit_content("The farmer's name is Abebe and his GPS is 9.0249, 38.7469"))
