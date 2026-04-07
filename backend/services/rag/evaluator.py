from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from .pipeline import rag_query
from services.agent.agent import run_agent

def evaluate_rag(test_cases: list[dict], retriever, reranker) -> dict:
    questions = []
    answers = []
    contexts_list = []
    ground_truths = []

    for case in test_cases:
        contexts = rag_query(case["persona_prompt"], case["question"], retriever, reranker)
        result = run_agent(case["persona_prompt"], case["question"], contexts)
        answer = result["answer"]
        
        questions.append(case["question"])
        answers.append(answer)
        contexts_list.append(contexts)
        ground_truths.append(case["ground_truth"])

    dataset = Dataset.from_dict({
        "question" : questions,
        "answer" : answers,
        "contexts" : contexts_list,
        "ground_truth" : ground_truths,
    })

    result = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall])
    return result.to_pandas().mean().to_dict()