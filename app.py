import streamlit as st
import os
import pandas as pd
import json
from src.utils.graphs import TestDataGraph_agent

st.set_page_config(page_title="Agentic Test Data Generator", layout="wide")

st.title("🧪 Agentic Test Data Generation")
st.markdown("Upload a document (PDF/Doc) to extract a Knowledge Graph and generate Test Cases with Data.")

uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt'])

if uploaded_file is not None:
    # Save file locally for processing
    upload_dir = "docs"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Generate Test Data"):
        with st.spinner("Processing document and generating data..."):
            try:
                # Initialize state
                initial_state = {"file_path": file_path}
                
                # Run the LangGraph agent
                result = TestDataGraph_agent.invoke(initial_state)
                
                st.success("Generation Complete!")

                # Display Knowledge Graph (Raw Text)
                with st.expander("View Knowledge Graph"):
                    st.markdown(result.get("kg_graph", "No KG generated"))

                # Display Test Cases
                st.subheader("📋 Generated Test Cases")
                test_cases_raw = result.get("test_cases", "[]")
                try:
                    # Attempt to parse if it's a JSON string, otherwise show as text
                    tc_data = json.loads(test_cases_raw) if isinstance(test_cases_raw, str) else test_cases_raw
                    st.dataframe(pd.DataFrame(tc_data), use_container_width=True)
                except:
                    st.text(test_cases_raw)

                # Display Test Data
                st.subheader("📊 Generated Test Data")
                test_data_raw = result.get("test_data", "[]")
                try:
                    td_data = json.loads(test_data_raw) if isinstance(test_data_raw, str) else test_data_raw
                    st.dataframe(pd.DataFrame(td_data), use_container_width=True)
                except:
                    st.text(test_data_raw)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")