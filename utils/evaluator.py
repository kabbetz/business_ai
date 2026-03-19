from langchain.evaluation.qa import QAEvalChain
from langchain_openai import ChatOpenAI

def evaluate_model(qa_chain):
    llm = ChatOpenAI(temperature=0)

    eval_chain = QAEvalChain.from_llm(llm)

    examples = [
        {
            "query": "What is total revenue?",
            "answer": "Revenue is the total income generated from sales."
        },
        {
            "query": "What is profit margin?",
            "answer": "Profit margin is net income divided by revenue."
        }
    ]

    predictions = []

    for example in examples:
        result = qa_chain.invoke(example["query"])
        predictions.append({
            "query": example["query"],
            "result": result.content
        })

    graded_outputs = []

    for example, prediction in zip(examples, predictions):
        result = eval_chain.invoke({
            "query": example["query"],
            "answer": example["answer"],
            "result": prediction["result"]
        })

        graded_outputs.append({
            "query": example["query"],
            "prediction": prediction["result"],
            "expected": example["answer"],
            "evaluation": result
        })

        return graded_outputs