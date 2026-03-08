from typing import TypedDict, List, Dict


class TestDataState(TypedDict):
    file_path: str
    image_path: str
    context: str
    kg_graph: str
    test_cases: List[Dict]
    test_data: List[Dict]