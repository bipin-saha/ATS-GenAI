import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import io
import base64
from dotenv import load_dotenv
from text_ext import extract_text_from_pdf

load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, pdf_content])
    return response.text

def file_uploader(uploaded_file):
    if uploaded_file is None:
        st.stop()
    
    else:        
        file_path = os.path.join("Uploaded", "1.pdf")
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getvalue())
    
        return ""

job_field = ""


#Streamlit App
st.set_page_config(page_title="ATS Resume Review", layout="wide")
st.header("ATS Resume Review")

with st.sidebar:
        st.title("Upload PDF:")
        job_field = st.text_input("Job Field: ",key="input2", placeholder="Enter Job Field")
        uploaded_file = st.file_uploader("", type=["pdf"])
        submit1 = st.button("Submit & Process", type="primary")
        #submit1 = st.button("Resume Assesmet")
        submit2 = st.button("Possible Improvements")
        submit3 = st.button("Percentage Match")

job_description = st.text_input("Job Description: ", key="input", placeholder="Enter Job Description")

pdf_file_path = "Uploaded/1.pdf"   

if uploaded_file is not None:
    response = file_uploader(uploaded_file)
    st.write(response)
    pdf_text = extract_text_from_pdf(pdf_file_path)

else:
    pdf_text = ""

input_prompt1 = f"""
 As an adept Technical Human Resource Manager with expertise in {job_field}, your objective is to assess the 
 provided resume in direct correlation to the requirements of the {job_field} position. Deliver a thorough 
 professional evaluation, emphasizing key highlights from the candidate's resume and drawing connections to the 
 job description. Provide insights into the alignment between the candidate's profile and the specified job role. 
 The response should be a technical report. In the report do not address any one.
 """

input_prompt2 = f"""
 As an accomplished Technical Human Resource Manager specializing in {job_field}, your responsibility is to conduct 
a comprehensive review of the provided CV/resume in alignment with the specified {job_description}. \n \n \n Share 
your expert evaluation highlighting the candidate's strengths and areas for improvement relevant to the {job_description}. 
\n \n \n Offer constructive insights on how the candidate can enhance their profile to increase the likelihood of securing 
this specific position.
"""

input_prompt3 = f"""
As an experienced and highly skilled recruiter well-versed in the intricacies of Applicant Tracking Systems (ATS) 
and possessing profound expertise in {job_field}, your role is to conduct a comprehensive evaluation of the provided 
resume in comparison to the provided {job_description}. \n \n \n Furnish a percentage-based assessment of the alignment
between the resume and the job requirements. Subsequently, identify any missing keywords and conclude with insightful 
remarks on the overall fit for the position.First the output should come as percentage and then keywords missing and last 
final thoughts."""

        
if submit1:
    with st.spinner("Processing..."):
        if uploaded_file is not None:
            #pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt1, pdf_text)
            st.subheader("Response")
            st.write(response)
        else:
            st.write("Upload PDF First")
        
if submit2:
    with st.spinner("Processing..."):
        if uploaded_file is not None:
            #pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt2, pdf_text)
            st.subheader("Response")
            st.write(response)
        else:
            st.write("Upload PDF First")


elif submit3:
    with st.spinner("Processing..."):
        if uploaded_file is not None:
            #pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt3, pdf_text)
            st.subheader("Response")
            st.write(response)
        else:
            st.write("Upload PDF First")
