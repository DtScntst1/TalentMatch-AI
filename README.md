<div align="center">
  <img src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" width="200" />
  <h1>🎯 TalentMatch AI</h1>
  <p><strong>A Next-Generation Resume & Job Matching AI powered by RAG and LLMs.</strong></p>
</div>

---

## 🚀 Overview

**TalentMatch AI** is a state-of-the-art AI application designed to evaluate a candidate's resume against a specific job description. By utilizing **Retrieval-Augmented Generation (RAG)** and **Google's Gemini Pro LLM**, the system extracts key information from PDFs, performs semantic similarity search using **ChromaDB**, and provides an intelligent evaluation report including a Match Score, Matched Skills, and Missing Skills.

This project demonstrates advanced capabilities in Generative AI, Natural Language Processing, and intelligent application architecture.

## 🌟 Key Features

- **📄 Intelligent Document Parsing:** Automatically reads and chunks PDF resumes using `pypdf`.
- **🧠 Advanced Vector Search (RAG):** Uses HuggingFace embeddings (`all-MiniLM-L6-v2`) and `ChromaDB` for highly accurate semantic search.
- **🤖 LLM Integration:** Powered by `LangChain` and Google's `Gemini Pro` for expert-level HR evaluation.
- **📊 Dynamic Visualizations:** Beautiful interactive match score gauge generated with `Plotly`.
- **🖥️ Clean UI:** Built entirely on `Streamlit` for a seamless user experience.

---

## 🛠️ Technology Stack

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,git,github,vscode&perline=14" />
  </a>
</p>

- **Framework:** Streamlit
- **AI/LLM Engine:** LangChain, Google Gemini Pro API
- **Embeddings:** HuggingFace Sentence Transformers
- **Vector Database:** ChromaDB
- **Data Visualization:** Plotly

---

## 💻 Getting Started

### Prerequisites
- Python 3.9+
- A Free [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DtScntst1/TalentMatch-AI.git
   cd TalentMatch-AI
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

## 📈 Future Enhancements
- Integration with LinkedIn profile links instead of PDF uploads.
- Cover Letter Generation based on the missing skills.
- Multi-resume batch processing for real HR recruiters.

---
*Built with ❤️ for the Data Science Community.*
