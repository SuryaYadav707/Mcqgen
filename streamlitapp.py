import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
# import langchain
from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.logger import logging
from langchain.globals import set_verbose
set_verbose(True)
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcq_generator.MCQGenerator import generate_and_evaluate_quiz

# Load response JSON
with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)
    
# Set page width and sidebar collapse
st.set_page_config(page_title="MCQ Generator", page_icon="📝", layout="wide")

# Title and description with animation
st.title("📚 MCQ Generator")
st.write("Welcome to the MCQ Generator app! Upload a PDF or text file, specify the number of questions, subject, and complexity level, then click the button to generate multiple-choice questions.")

# Sidebar with animation
st.sidebar.header("🎨 Generator")
uploaded_file = st.sidebar.file_uploader("Upload File", type=["pdf", "txt"], help="Upload a PDF or text file containing content to generate MCQs from.")
mcq_count = st.sidebar.number_input("Number of Questions", min_value=3, max_value=50, value=10, help="Specify the number of multiple-choice questions to generate.")
subject = st.sidebar.text_input("Subject", max_chars=20, help="Enter the subject or topic for the generated MCQs.")
tone = st.sidebar.text_input("Complexity Level", max_chars=20, value="Simple", help="Enter the complexity level of the generated MCQs.")
button = st.sidebar.button("Generate MCQs")

# Main content with animation
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner("Generating MCQs..."):
        try:
            text = read_file(uploaded_file)
            # Call the LLM while getting the token metrics
            with get_openai_callback() as cb:
                response = generate_and_evaluate_quiz({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("Error generating MCQs. Please try again.")
        else:
            # Display generated MCQs with animation
            if isinstance(response, dict):
                quiz = response.get("quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.write(df)

                        # Download button for MCQs as CSV
                        st.download_button(
                            label="Download as CSV",
                            data=df.to_csv().encode("utf-8"),
                            file_name="mcqs.csv",
                            mime="text/csv",
                            help="Download the generated MCQs as a CSV file."
                        )

                        # Display review with animation
                        st.subheader("📝 Review:")
                        st.write(response["review"])
                    else:
                        st.error("Error in the table data")
                else:
                    st.error("No MCQs generated. Please check your input and try again.")
            else:
                st.write(response)
