from ddgs import DDGS

ddgs = DDGS()
results = ddgs.text("artificial intelligence 2025", max_results=3)

for r in results:
    print(r["title"])
    print(r["body"])
    print(r["href"])
    print("---")