# Privacy-Preserving Multi-Agent Climate-Resilient Farming Advisor

A research-grade multi-agent system designed for Ethiopian smallholder farmers, focusing on climate resilience and privacy-preserving federated learning simulation.

## Overview

This project implements a multi-agent system designed to provide climate-resilient agricultural advice to Ethiopian smallholder farmers. It addresses the challenge of delivering personalized, data-driven insights while preserving the privacy of individual farm data. The system utilizes a federated learning simulation to aggregate regional insights without exposing raw user inputs.

The architecture consists of five specialized agents orchestrated by **LangGraph**:
1.  **Local Data Analyzer**: Securely processes user inputs locally.
2.  **Federated Collaborator**: Aggregates insights using Differential Privacy.
3.  **Crop/Weather Planner**: Generates climate-resilient recommendations.
4.  **Privacy Auditor**: Monitors data flows for leaks.
5.  **Synthesizer**: Compiles multilingual reports (English, Amharic, Afaan Oromoo).

## Target Audience

- **Researchers**: Interested in Federated Learning and Multi-Agent Systems in Agriculture.
- **Developers**: Building privacy-preserving AI applications.
- **Agricultural Extension Workers**: Looking for tools to assist smallholder farmers.

## Prerequisites

- **Python**: Version 3.10 or higher.
- **API Keys**: OpenAI and Tavily API keys are required for agent functionality.
- **OS**: Linux, macOS, or Windows (WSL recommended).

## Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ethio-climate-agri-advisor.git
    cd ethio-climate-agri-advisor
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -e .
    # OR
    pip install -r requirements/base.txt
    ```

## Environment Setup

Create a `.env` file in the root directory with your API keys:

```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

## Usage

To run the main advisor demo:

```bash
python3 src/ethio_agri_advisor/main.py
```

The system will simulate a user interaction, process the data through the agent graph, and output a final report in multiple languages along with privacy audit logs.

## Data Requirements

The system accepts natural language input describing farm conditions (e.g., location, crop type, soil issues).
Example input:
> "I am a farmer in East Gojjam. I have 2 hectares. The soil is acidic. I plant Teff."

## Testing

Run the test suite to verify system integrity:

```bash
pip install -r requirements/test.txt
pytest
```

## Configuration

Configuration is managed via `pyproject.toml` and environment variables.
- **Model**: Defaults to `gpt-4o`. Can be changed in agent initialization.
- **Privacy Budget**: Epsilon values for Differential Privacy can be tuned in `tools/privacy_engine.py`.

## Methodology

The system uses a **Federated Learning** simulation where:
1.  Local agents compute gradients (insights) from private data.
2.  A central aggregator averages these gradients with **Differential Privacy (DP)** noise (Laplace mechanism).
3.  Global insights are shared back to local agents to improve recommendations without sharing raw data.

## Performance

- **Privacy**: Validated against membership inference attacks (see `benchmarks/privacy_eval.py`).
- **Utility**: Accuracy loss due to DP noise is minimized through adaptive sensitivity scaling (see `benchmarks/accuracy_eval.py`).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a history of changes.

## Citation

If you use this project in your research, please cite:

```bibtex
@software{ethio_agri_advisor,
  author = {Aman Atalay},
  title = {Privacy-Preserving Multi-Agent Climate-Resilient Farming Advisor},
  year = {2026},
  url = {https://github.com/yourusername/ethio-climate-agri-advisor}
}
```

## Contact

For questions or feedback, please open an issue on GitHub.
