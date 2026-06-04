import streamlit as st
import os
import tempfile
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="TalentMatch AI", page_icon="🎯", layout="wide")

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def create_vector_store(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    
    # Using local embeddings (free) to create the vector store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma.from_texts(chunks, embedding=embeddings)
    return vector_store

import google.generativeai as genai

def analyze_match_direct(cv_context, job_desc, api_key):
    try:
        genai.configure(api_key=api_key)
        
        # Auto-detect the best available model for this specific API key
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return "ERROR: No suitable models found for this API key. Please check your Google AI Studio account."
            
        # 2026 Model Selection Logic (Prefer free-tier friendly flash models)
        target_model = available_models[0]
        preferred_models = ['models/gemini-flash-latest', 'models/gemini-2.5-flash', 'models/gemini-2.0-flash']
        
        for pref in preferred_models:
            if pref in available_models:
                target_model = pref
                break
                
        # Remove the 'models/' prefix for the GenerativeModel class
        model_name = target_model.replace('models/', '')
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
        You are an expert HR Tech AI Assistant. Your task is to evaluate a candidate's resume against a job description.
        
        Resume Context:
        {cv_context}
        
        Job Description:
        {job_desc}
        
        Provide your analysis in the following format exactly:
        SCORE: [A number between 0 and 100 representing the match percentage]
        MATCHED_SKILLS: [Comma separated list of skills they have]
        MISSING_SKILLS: [Comma separated list of skills they are missing]
        SUMMARY: [A 2-3 sentence summary of why they are a good or bad fit]
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        available_str = ', '.join(available_models) if 'available_models' in locals() else 'Could not fetch'
        return f"ERROR: Gemini API failure -> {str(e)}"

def analyze_match(vector_store, job_desc, api_key):
    try:
        # Retrieve relevant CV parts based on job description
        docs = vector_store.similarity_search(job_desc, k=3)
        cv_context = "\n".join([doc.page_content for doc in docs])
        
        # Use official Google SDK directly
        return analyze_match_direct(cv_context, job_desc, api_key)
    except Exception as e:
        return f"ERROR: Vector Search failed -> {str(e)}"

def parse_response(response_text):
    data = {"SCORE": 0, "MATCHED_SKILLS": "", "MISSING_SKILLS": "", "SUMMARY": ""}
    
    if response_text.startswith("ERROR:"):
        data["SUMMARY"] = response_text
        return data
        
    lines = response_text.split('\n')
    for line in lines:
        if line.startswith("SCORE:"):
            try:
                # Handle cases where model might output "SCORE: 85%"
                score_str = line.replace("SCORE:", "").replace("%", "").strip()
                data["SCORE"] = int(score_str)
            except:
                data["SCORE"] = 50
        elif line.startswith("MATCHED_SKILLS:"):
            data["MATCHED_SKILLS"] = line.replace("MATCHED_SKILLS:", "").strip()
        elif line.startswith("MISSING_SKILLS:"):
            data["MISSING_SKILLS"] = line.replace("MISSING_SKILLS:", "").strip()
        elif line.startswith("SUMMARY:"):
            data["SUMMARY"] = line.replace("SUMMARY:", "").strip()
    return data

def draw_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Match Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps' : [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "gray"}],
            'threshold' : {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 80}
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
    return fig

def main():
    st.title("🎯 TalentMatch AI: Smart Resume & Job Matcher")
    st.markdown("Upload your resume and a job description to see how well you match using AI & RAG!")

    # --- Sidebar ---
    with st.sidebar:
        st.header("⚙️ Settings")
        api_key = st.text_input("Enter Gemini API Key", type="password", help="Get your key from Google AI Studio")
        if not api_key:
            st.warning("Please enter your API Key to proceed.")
            st.markdown("[Get your free Gemini API Key here](https://aistudio.google.com/app/apikey)")
            
        st.markdown("---")
        st.header("📄 Upload Files")
        resume_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"])

    # --- Main Layout ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 Job Description")
        job_desc = st.text_area("Paste the job description here...", height=300, 
                                placeholder="e.g. We are looking for a Data Scientist with 3+ years of experience in Python, SQL, and Machine Learning...")
        
    with col2:
        st.subheader("🚀 Analysis Results")
        if st.button("Analyze Match", use_container_width=True, type="primary"):
            if not api_key:
                st.error("API Key is required! Please enter it in the sidebar.")
            elif not resume_file:
                st.error("Please upload a resume (PDF) in the sidebar!")
            elif not job_desc:
                st.error("Please provide a job description!")
            else:
                with st.spinner("Step 1: Reading CV & Creating Embeddings..."):
                    raw_text = get_pdf_text([resume_file])
                    vector_store = create_vector_store(raw_text)
                
                with st.spinner("Step 2: Performing Semantic Search & AI Analysis..."):
                    raw_response = analyze_match(vector_store, job_desc, api_key)
                    results = parse_response(raw_response)
                
                st.success("Analysis Complete!")
                
                st.plotly_chart(draw_gauge(results["SCORE"]), use_container_width=True)
                
                st.markdown("### 📝 AI Summary")
                st.info(results["SUMMARY"])
                
                st.markdown("### ✅ Matched Skills")
                st.success(results["MATCHED_SKILLS"])
                
                st.markdown("### ❌ Missing Skills")
                st.error(results["MISSING_SKILLS"])

if __name__ == "__main__":
    main()

