import chromadb
import os

class VectorMemory:
    def __init__(self):
       
        self.client = chromadb.PersistentClient(path="chroma_db")
        
        
        self.collection = self.client.get_or_create_collection(
            name="agent_memory",
            metadata={"heuristic": "cosine"}
        )

    def save(self, topic: str, response: str):
        """Save topic and response to vector database"""
        print(f"[VectorMemory]  Saving to vector DB: {topic}")
        
        
        existing = self.collection.get(ids=[topic])
        
        if existing["ids"]:
       
            self.collection.update(
                ids=[topic],
                documents=[response],
                metadatas=[{"topic": topic}]
            )
        else:
           
            self.collection.add(
                ids=[topic],
                documents=[response],
                metadatas=[{"topic": topic}]
            )
        
        print(f"[VectorMemory]  Saved successfully")

    def recall(self, topic: str) -> str:
        """Find most similar past research using semantic search"""
        print(f"[VectorMemory]  Searching vector DB for: {topic}")
        
        try:
      
            results = self.collection.query(
                query_texts=[topic],
                n_results=1
            )
            
            if results["documents"] and results["documents"][0]:
                print(f"[VectorMemory]  Found similar past research")
                return results["documents"][0][0]
            
            return "No memory found"
        
        except Exception as e:
            print(f"[VectorMemory] ✗ Error: {e}")
            return "No memory found"

    def get_all(self) -> dict:
        """Return all stored memories"""
        return self.collection.get()