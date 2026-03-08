from langgraph.graph import StateGraph, START, END
from src.utils.state import TestDataState
from src.utils.models import model as llm
from src.utils.prompts import *
from src.utils.nodes import *


TestDataGraph = StateGraph(TestDataState)
TestDataGraph.add_node("build_context",build_context)
TestDataGraph.add_node("create_kg", create_kg_from_context)
TestDataGraph.add_node("gen_test_cases",generate_test_cases)
TestDataGraph.add_node("gen_test_data", generate_test_data)

TestDataGraph.add_edge(START,"build_context")
TestDataGraph.add_edge("build_context","create_kg")
TestDataGraph.add_edge("create_kg","gen_test_cases")
TestDataGraph.add_edge("gen_test_cases","gen_test_data")
TestDataGraph.add_edge("gen_test_data",END)
TestDataGraph_agent=TestDataGraph.compile()

if __name__ == "__main__":
    pass