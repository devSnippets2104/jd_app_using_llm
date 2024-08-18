import cohere
import streamlit as st
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(
    api_key=os.getenv("CO_API_KEY")
)

def getResponseFromCohere(input):
    resp= co.generate(
        model='command-r-plus',
        prompt=input
    )
    return resp.generations[0].text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

input_prompt="""
You have to act like a skilled or very experienced ATS(Application tracking system) with a deep
understanding of the tech field, software engineering, data science, data analyst and big data engineer.
Your task is to evaluate the resume based on the job description.
NOTE: Consider the job market is very competitive and you should provide best assistance
for improving the resumes.
Assign the percentage matching based on the JD and the missing keywords with high accuracy
resume:{text}
description:{jd}
I want the response in one single string having the structure and remember to keep it properly formatted.
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

##initate streamlit app
st.title("ATS Tracker")
st.text("Improve your resume ATS")
st.text("Made by Aditya Kumar")
jd=st.text_area("Please add the job description")
uploaded_file=st.file_uploader("Upload your resume",type="pdf",help="Please upload in PDF")
submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        with st.spinner("Please wait, getting your scores ready..."):
            text=input_pdf_text(uploaded_file)
            formatted_prompt = input_prompt.format(text=text, jd=jd)
            response=getResponseFromCohere(formatted_prompt)
        st.subheader(response)