# 📄 Chat with Doc - LLM PDF Analyzer 🦙💬

Welcome to **Chat with Doc**, a powerful AI assistant that allows you to **chat with your PDF documents**! Just upload any PDF and ask questions – our intelligent bot will give you meaningful answers extracted from your file using **LLama 3.3**, **LangChain**, and **RAG (Retrieval-Augmented Generation)**.

---
### Key Functionalities 🌟

* 📤Upload any PDF document
* 💬Ask contextual questions and get instant, relevant answers
* 🧠 Retains chat memory to keep the conversation natural
* 🔎 Uses RAG (Retrieval-Augmented Generation) for accurate responses
*⚡ Powered by LLama 3.3 on Groq's ultra-fast cloud infrastructure
* 🖥️ Minimal, beautiful UI with Streamlit


## 🛠️ Tech Stack

| Component       | Description                                      |
|----------------|-------------------------------------------------- |
| 🦙 LLama 3.3    | Large Language Model for generating answers      |
| 🔗 LangChain    | Framework to manage chains and memory            |
| 🧠 RAG          | Combines retrieval and generation                |
| 📦 FAISS        | Facebook AI Similarity Search for vector storage|
| 🌐 Streamlit    | Web interface for user interaction               |
| 🧾 HuggingFace  | For embedding textual data into vectors          |
| 🔐 dotenv       | Securely manages environment variables           |
| 📤 OCR (opt.)   | Pytesseract for extracting text from images      

##  Setup Steps
🔧 Step 1: Create Virtual Environment
```
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate for Windows
```
📦 Step 2: Install All Requirements
```
pip install -r requirements.txt
```
🔐 Step 3: Set Your API Key
Create a .env file and insert your Groq key:
```
GROQ_API_KEY=your_groq_api_key_here
```
🚀 Step 4: Run the Application
```
streamlit run main.py
```

### Working Demo:
![llm_pdf_demo](https://github.com/user-attachments/assets/a540b157-9ad4-4eda-8872-822fb246ee8b)



