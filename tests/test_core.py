import pytest
from ethio_agri_advisor.core.graph import AgriAdvisorGraph
from ethio_agri_advisor.tools.privacy_engine import PrivacyEngine

def test_graph_initialization():
    """Test that the main graph can be initialized."""
    import os
    from unittest.mock import patch, MagicMock

    # Mock environment variables and settings
    with patch.dict(os.environ, {"GOOGLE_API_KEY": "test-key", "TAVILY_API_KEY": "test-key"}), \
         patch("ethio_agri_advisor.config.settings.GOOGLE_API_KEY", "test-key"):
        # Mock ChatGoogleGenerativeAI to avoid actual API calls
        with patch("langchain_google_genai.ChatGoogleGenerativeAI") as mock_llm:
            mock_llm.return_value = MagicMock()
            try:
                graph = AgriAdvisorGraph()
                assert graph is not None
            except Exception as e:
                pytest.fail(f"Graph initialization failed: {e}")

def test_privacy_engine_noise():
    """Test that privacy engine adds noise."""
    engine = PrivacyEngine(epsilon=1.0)
    import numpy as np
    data = np.array([10.0])
    noisy_data = engine.add_differential_privacy_noise(data)
    assert noisy_data[0] != 10.0
