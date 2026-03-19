import os
import sys
import streamlit as st
import pandas as pd

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from utils.data_loader import load_data
from utils.pdf_loader import load_financial_pdfs
from utils.metrics import compute_metrics
from utils.evaluator import evaluate_model
from utils.visualization import (
    plot_revenue_trend,
    plot_product_performance,
    plot_regional_analysis,
    plot_customer_age_groups)
from utils.financial_extractor import extract_financials
from utils.financial_ratios import compute_ratios
from rag.vectorstore import create_vectorstore
from rag.retriever import get_retriever
from chains.qa_chain import build_qa_chain

st.title("InsightForge - AI Business Intelligence Assistant")

@st.cache_resource
def setup_system():
    import os  
      
    # Load CSV data
    df = load_data()
    metrics = compute_metrics(df)
    docs = [f"{k}: {v}" for k, v in metrics.items()]

    pdf_folder = "data"

    pdf_paths = [
        os.path.join(pdf_folder, file)
        for file in os.listdir(pdf_folder)
        if file.endswith(".pdf")
    ]

    # Load PDF documents
    from utils.pdf_loader import load_financial_pdfs
    pdf_docs = load_financial_pdfs(pdf_paths)

    # Combine CSV + PDF data
    vectorstore = create_vectorstore(docs, pdf_docs)
    retriever = get_retriever(vectorstore)
    qa_chain = build_qa_chain(retriever)

    return qa_chain, retriever
    
qa_chain, retriever = setup_system()

# Visualization Section
st.header("Data Visualizations")

df = load_data()

if st.button("Show Sales Trend"):
    fig = plot_revenue_trend(df)
    st.pyplot(fig)

if st.button("Show Product Performance"):
    fig = plot_product_performance(df)
    st.pyplot(fig)

if st.button("Show Regional Analysis"):
    fig = plot_regional_analysis(df)
    st.pyplot(fig)

if st.button("Show Customer Age Demographic"):
    fig = plot_customer_age_groups(df)
    st.pyplot(fig)

query = st.chat_input("Ask a question about your business data:")

if query:
    docs = retriever.invoke(query)
    # Show user message
    st.chat_message("user").write(query)

    # Save user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": query
    })

    # Build conversation history
    history_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in st.session_state.chat_history]
    )

    # Extract financial data
    docs = retriever.invoke(query)
    combined_text = " ".join([doc.page_content for doc in docs])

    financial_data = extract_financials(combined_text)
    ratios = compute_ratios(financial_data)

    # Optional: show debug
    st.write("Financial Data:", financial_data)
    st.write("Ratios:", ratios)

    # Feed ratios into LLM
    full_query = f"""
    Financial ratios:
    {ratios}

    Conversation history:
    {history_text}

    Question:
    {query}
    """

    # Run RAG chain
    response = qa_chain.invoke(full_query)

    # Show response
    st.chat_message("assistant").write(response.content)

    # Save response
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response.content
    })
    
# Evaluation section
st.header("Model Evaluation")

if st.button("Run Model Evaluation"):
    results = evaluate_model(qa_chain)
    st.write("Evaluation Results:", results)


