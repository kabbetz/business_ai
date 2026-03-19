from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def build_qa_chain(retriever):
    llm = ChatOpenAI(temperature=0)

    prompt = ChatPromptTemplate.from_template("""
    You are a business intelligence analyst.

    Use the context below to answer the question clearly and provide insights.

    Context:
    {context}

    Question:
    {question}
    """)

    def format_docs(docs):
        return "\n".join([doc.page_content for doc in docs])

    chain = (
        {
            "context": retriever | format_docs,
            "question": lambda x: x
        }
        | prompt
        | llm
    )

    return chain
