#1st 

import os       
import requests    
import sys              
import nltk
nltk.download('punkt')
import pi_heif                                              
                                                #to access working directory
from dotenv  import load_dotenv                                          #to store api keys to env variables
import streamlit as st                                                   #UI
from langchain_community.document_loaders import UnstructuredPDFLoader   #to read pdf file nd extract text from it
from langchain_text_splitters.character import CharacterTextSplitter       #to chunk data into smaller chunks
from langchain_community.vectorstores import FAISS                       #Vector similarity search. Facebook AI 
from langchain_community.embeddings import HuggingFaceEmbeddings         #Text into vector embeddings
from langchain_groq import ChatGroq                                     #to access llama api via cloud                  
from langchain.memory import ConversationBufferMemory                   #import past conv
from langchain.chains import ConversationalRetrievalChain                 #methodology used to connect

import pytesseract
from PIL import Image

# Set the tesseract_cmd to the correct path of tesseract.exe


#Step 1: Build conversational chain
 
from dotenv import load_dotenv
#load the environment variables
load_dotenv()    #call fn
print(os.getenv("GROQ_API_KEY"))  


# Get the working directory
working_dir = os.path.dirname(os.path.abspath(__file__))

#Read the file nd extract the text
def load_document(file_path):
    loader = UnstructuredPDFLoader(file_path)
    documents = loader.load()
    return documents

#The extracted text will be chunked into a vector db
def setup_vectorstore(documents):
    embeddings = HuggingFaceEmbeddings()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200       
    )
    doc_chunks = text_splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(doc_chunks, embeddings)
    return vectorstore

#To create conversational retrieval chain
def create_chain(vectorstore):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0  # Lower temperature ensures consistent answers
    )
    retriever = vectorstore.as_retriever()
    memory = ConversationBufferMemory(
        llm = llm,
        output_key = "answer",
        memory_key = "chat_history",  #stores prev conversation
        return_messages = True
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = retriever,
        chain_type = "map_reduce",   #to reduce the ans in points
        memory = memory,
        verbose = True  #prints intermediate steps
    )
    return chain


#Step 2: Build the User Interface
st.set_page_config(
    page_title = "Chat with Doc",
    page_icon = "📄",
    layout = "centered"
)

st.title("Chat with Doc - LLAMA 3.3🦙:)")

#initialize the chat history in streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader(label = "Upload your pdf file",type = ["pdf"])

if uploaded_file:
    file_path = f"{working_dir}/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

#understand this code
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = setup_vectorstore(load_document(file_path))

    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = create_chain(st.session_state.vectorstore)

#once the user refreshe, no need to retrieve

#Retrieve the previous conversation
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#chatbox with send button (chat widget)
user_input = st.chat_input("Ask Llama....")


#once send button is clicked
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"): #human emoji - red color
        st.markdown(user_input)
    

    with st.chat_message("assistant"): # LLM model: robo emoji - yellow color
        response = st.session_state.conversation_chain({"question": user_input})
        assistant_response = response["answer"]
        st.markdown(assistant_response)
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})
