"""
File: nodes.py
Description: Implementation of LangGraph nodes for the Test Data Generation workflow, including Knowledge Graph extraction, Test Case generation, and Test Data creation.
Author: Ramendra Tyagi
"""
from langchain_core.prompts import PromptTemplate
from src.utils.state import TestDataState
from langchain_core.messages import HumanMessage
from src.utils.constants import MAX_RETRIES
from src.utils.prompts import *
import json
import traceback
import os
import base64
import pymupdf4llm
from logger import CustomLogger
from dotenv import load_dotenv
load_dotenv()
logger = CustomLogger().get_logger(__name__)
from src.utils.models import model as llm

def encode_image_to_base64(image_path):
    """
    Encodes a local image file to a Base64 string.
    """
    with open(image_path, "rb") as image_file:
        encoded_bytes = base64.b64encode(image_file.read())
        # Decode the bytes to a UTF-8 string for use in JSON/text APIs
        encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def convert_image_text_llm():
    image_dir = "docs/images"
    if not os.path.exists(image_dir):
        return ""
    
    all_images_text = []
    prompt = "Convert below image into text"

    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(image_dir, filename)
            encoded_string = encode_image_to_base64(image_path)
            image_url = f"data:image/png;base64,{encoded_string}"
            
            msg = llm.invoke([
                HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ]
                )
            ])
            all_images_text.append(msg.content)
    
    return "\n".join(all_images_text)


def build_context(state: TestDataState):
    path = state["file_path"]
    md_text = pymupdf4llm.to_markdown(path)
    md_text_images = pymupdf4llm.to_markdown(
    doc=path,
    page_chunks=True,
    write_images=True,
    image_path="docs/images",
    image_format="png",
    dpi=300
    )
    image_to_text = convert_image_text_llm()

    return {"context": md_text + image_to_text}


def create_kg_from_context(state: TestDataState):
    context = state["context"]
    prompt_template  = PromptTemplate.from_template(template=KG_PROMPT)
    prompt= prompt_template.format(context=context)
    response = llm.invoke(prompt)
    return {"kg_graph": response.content}


def generate_test_cases(state: TestDataState):
    context = state['context']
    kg = state["kg_graph"]
    prompt_template  = PromptTemplate.from_template(template=PROMPT_TEST_CASE)
    prompt = prompt_template.format(context=context,kg=kg)
    response =llm.invoke(prompt)
    return {"test_cases": response.content}


def generate_test_data(state: TestDataState):
    context = state['context']
    kg = state["kg_graph"]
    test_cases = json.dumps(state["test_cases"])
    prompt_template  = PromptTemplate.from_template(template=PROMPT_TEST_DATA)
    prompt= prompt_template.format(context=context,kg=kg,test_cases=test_cases)
    response =llm.invoke(prompt)

    return {"test_data": response.content}