from setuptools import setup, find_packages

setup(
    name="ethio_agri_advisor",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langgraph>=0.0.10",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.5",
        "langchain-community>=0.0.10",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "pandas>=2.0.0",
        "python-dotenv>=1.0.0",
        "tavily-python>=0.3.0",
    ],
)
