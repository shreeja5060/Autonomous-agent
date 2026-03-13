import requests
import time

queries = [
    "what is machine learning",
    "what is quantum computing",
    "what is blockchain",
    "what is reinforcement learning",
    "what is computer vision"
]

results = []

for query in queries:
    print(f"Testing: {query}")
    start = time.time()
    
    response = requests.post(
        "http://127.0.0.1:8000/run",
        json={"topic": query}
    )
    
    end = time.time()
    latency = round(end - start, 2)
    data = response.json()
    score = data["final_evaluation"]["overall_score"]
    
    results.append({
        "query": query,
        "latency": latency,
        "score": score
    })
    
    print(f"✓ Score: {score}/10 | Time: {latency}s")

# Summary
avg_latency = round(sum(r["latency"] for r in results) / len(results), 2)
avg_score = round(sum(r["score"] for r in results) / len(results), 2)

print(f"\n=== BENCHMARK RESULTS ===")
print(f"Queries tested: {len(results)}")
print(f"Average latency: {avg_latency}s")
print(f"Average quality score: {avg_score}/10")