# test_data_agent
## Overview
This project is an Agentic AI workflow designed to automate the generation of synthetic test data from documentation (PDFs). It leverages **LangGraph** for orchestration, **PyMuPDF4LLM** for document parsing, and Multimodal LLMs for image-to-text conversion and Knowledge Graph extraction.

## Workflow Architecture
The system follows a directed acyclic graph (DAG) structure:
1.  **Build Context**: Extracts text and images from PDF files.
2.  **Create KG**: Generates a Knowledge Graph from the extracted context to understand entities and relationships.
3.  **Generate Test Cases**: Defines logical test scenarios based on the context and KG.
4.  **Generate Test Data**: Produces the final synthetic test data in a structured format.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
To run the application, ensure your environment variables are set in a `.env` file, then launch the Streamlit UI:
```bash
streamlit run app.py
```

## Project Structure
- `src/utils/nodes.py`: Contains the logic for each step in the graph.
- `src/utils/graphs.py`: Defines the LangGraph state machine and edges.
- `src/utils/state.py`: Defines the `TestDataState` schema.
- `src/utils/prompts.py`: Stores the LLM prompt templates.
