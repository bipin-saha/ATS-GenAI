import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64
from dotenv import load_dotenv
from text_ext import extract_text_from_pdf

load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def file_uploader(uploaded_file):
    if uploaded_file is None:
        st.stop()
    
    else:        
        file_path = os.path.join("Uploaded", "1.pdf")
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getvalue())
    
        return "File Uploaded"

#Streamlit App
st.set_page_config(page_title="ATS Resume Review", layout="wide")
st.header("ATS Resume Review")
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
input_text = st.text_area("Job Description: ", key="input", placeholder="Enter Job Description")
job_field = st.text_input("Job Field: ",key="input2", placeholder="Enter Job Field")
   
pdf_file_path = "Uploaded/1.pdf"   

if uploaded_file is not None:
    response = file_uploader(uploaded_file)
    st.write(response)
    pdf_text = extract_text_from_pdf(pdf_file_path)

else:
    pdf_text = ""

col1, col2, col3 = st.columns([0.33, 0.33, 0.33], gap="small")

submit1 = col1.button("Resume Assesmet")
submit2 = col2.button("Possible Improvements")
submit3 = col3.button("Percentage Match")

input_prompt1 = f"""
 You are an experienced Technical Human Resource Manager, in the field of {job_field}. 
 Your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with that role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
 """

input_prompt2 = f"""
 As an experienced Technical Human Resource Manager, in the field of {job_field}. 
 Your task is to review the provided resume against the job description. 
 Please share your professional evaluation that the candidate can improve his/her profile 
 in which fields that can assure him/her to get this specific job.
 """

input_prompt3 = f"""
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of {job_field} and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        #pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_text, input_text)
        st.subheader("Response")
        st.write(response)
    else:
        st.write("Upload PDF First")

if submit2:
    if uploaded_file is not None:
        #pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_text, input_text)
        st.subheader("Response")
        st.write(response)
    else:
        st.write("Upload PDF First")


elif submit3:
    if uploaded_file is not None:
        #pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_text, input_text)
        st.subheader("Response")
        st.write(response)
    else:
        st.write("Upload PDF First")