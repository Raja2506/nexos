from app.memory.vector_store import add_memory, search_memory

# Add a few sample memories
add_memory("mem_001", "How do I reset my password?", {"topic": "account"})
add_memory("mem_002", "What is the capital of France?", {"topic": "geography"})
add_memory("mem_003", "I forgot my login credentials", {"topic": "account"})

# Search using DIFFERENT words but SAME meaning
results = search_memory("having trouble logging into my account", n_results=2)

print("Query: 'having trouble logging into my account'")
print("Top matches:")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"  - {doc}  (topic: {meta['topic']})")