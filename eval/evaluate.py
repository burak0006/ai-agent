import json
import math
import random
import argparse
from pathlib import Path
from typing import List, Dict, Any

from src.nine_fin_agent.retriever.vectorize import _retrieve_raw

ROOT_DIR = Path(__file__).resolve().parents[0]
EVAL_DATA_PATH = ROOT_DIR / "fixtures" / "eval_queries.json"

# -------------------
# Retrieval Metrics
# -------------------

def recall_at_k(retrieved: List[Dict[str, Any]], expected_id: str, k: int) -> float:
    ids = [doc.metadata.get("_id") for doc in retrieved[:k]]
    return 1.0 if expected_id in ids else 0.0

def precision_at_k(retrieved: List[Dict[str, Any]], expected_id: str, k: int) -> float:
    ids = [doc.metadata.get("_id") for doc in retrieved[:k]]
    return ids.count(expected_id) / k

def ndcg_at_k(retrieved: List[Dict[str, Any]], expected_id: str, k: int) -> float:
    ids = [doc.metadata.get("_id") for doc in retrieved[:k]]
    if expected_id not in ids:
        return 0.0
    rank = ids.index(expected_id) + 1
    return 1.0 / math.log2(rank + 1)

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

        rec = recall_at_k(docs, expected_id=None, k=5)
        prec = precision_at_k(docs, expected_id=None, k=5)
        ndcg = ndcg_at_k(docs, expected_id=None, k=5)

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
