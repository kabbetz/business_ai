from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def create_vectorstore(text_docs, pdf_docs=None):
    embeddings = OpenAIEmbeddings()

    all_texts = text_docs.copy()

    if pdf_docs:
        all_texts.extend([doc.page_content for doc in pdf_docs])

    vectorstore = Chroma.from_texts(
        texts=all_texts,
        embedding=embeddings,
        collection_name="business_data"
    )

    return vectorstore
