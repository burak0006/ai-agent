import json
import math
import random
import argparse
from pathlib import Path
from typing import List, Any

from src.nine_fin_agent.retriever.vectorize import _retrieve_raw

ROOT_DIR = Path(__file__).resolve().parents[0]
EVAL_DATA_PATH = ROOT_DIR / "fixtures" / "eval_queries.json"

# -------------------
# Retrieval Metrics
# -------------------

def recall_at_k(retrieved: List[Any], expected_text: str, k: int) -> float:
    contents = [doc.page_content for doc in retrieved[:k]]
    return 1.0 if any(expected_text in c for c in contents) else 0.0

def precision_at_k(retrieved: List[Any], expected_text: str, k: int) -> float:
    contents = [doc.page_content for doc in retrieved[:k]]
    hits = sum(1 for c in contents if expected_text in c)
    return hits / k

def ndcg_at_k(retrieved: List[Any], expected_text: str, k: int) -> float:
    contents = [doc.page_content for doc in retrieved[:k]]
    for i, c in enumerate(contents, start=1):
        if expected_text in c:
            return 1.0 / math.log2(i + 1)
    return 0.0

# -------------------
# LLM Output Metrics
# -------------------

def accuracy(answer: str, expected_text: str) -> float:
    return 1.0 if expected_text in answer else 0.0

def conciseness(answer: str, max_sentences: int = 3) -> float:
    sentences = [s for s in answer.split(".") if s.strip()]
    return 1.0 if len(sentences) <= max_sentences else 0.0

def faithfulness(answer: str, retrieved_docs: List[Any]) -> float:
    all_context = " ".join(doc.page_content for doc in retrieved_docs)
    # crude: check if first 5 words appear in context
    return 1.0 if all(word in all_context for word in answer.split()[:5]) else 0.0

# -------------------
# Runner
# -------------------

def run_eval(num_samples: int = 5):
    with open(EVAL_DATA_PATH, "r") as f:
        eval_data = json.load(f)

    if num_samples and num_samples < len(eval_data):
        eval_data = random.sample(eval_data, num_samples)

    results = []
    for item in eval_data:
        q = item["query"]
        expected_text = item["expected_text"]

        serialized, docs = _retrieve_raw(q)

        rec = recall_at_k(docs, expected_text, k=5)
        prec = precision_at_k(docs, expected_text, k=5)
        ndcg = ndcg_at_k(docs, expected_text, k=5)

        acc = accuracy(serialized, expected_text)
        conc = conciseness(serialized)
        faith = faithfulness(serialized, docs)

        result = {
            "query": q,
            "answer": serialized,
            "expected": expected_text,
            "accuracy": acc,
            "conciseness": conc,
            "faithfulness": faith,
            "recall@5": rec,
            "precision@5": prec,
            "nDCG@5": ndcg,
        }
        results.append(result)

        print(f"\nQuery: {q}")
        print(f"Expected: {expected_text}")
        print(f"Answer: {serialized}")
        print(f"Metrics: {result}")

    avg = {
        "accuracy": sum(r["accuracy"] for r in results) / len(results),
        "conciseness": sum(r["conciseness"] for r in results) / len(results),
        "faithfulness": sum(r["faithfulness"] for r in results) / len(results),
        "recall@5": sum(r["recall@5"] for r in results) / len(results),
        "precision@5": sum(r["precision@5"] for r in results) / len(results),
        "nDCG@5": sum(r["nDCG@5"] for r in results) / len(results),
    }

    print("\n==== Summary ====")
    for k, v in avg.items():
        print(f"{k}: {v:.2f}")

    return results, avg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate retrieval + LLM system.")
    parser.add_argument("--num-samples", type=int, default=5, help="Number of eval samples to run")
    args = parser.parse_args()
    run_eval(args.num_samples)
