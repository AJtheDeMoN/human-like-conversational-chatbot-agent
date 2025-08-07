import chromadb
import uuid

class MemoryManager:
    def __init__(self, path="kai_memory_db"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name="kai_chat_history")
        print("🧠 ChromaDB memory is ready.")

    def add_to_memory(self, session_id: str, text_chunk: str, embedding: list):
        doc_id = str(uuid.uuid4())
        self.collection.add(
            embeddings=[embedding],
            documents=[text_chunk],
            metadatas=[{"session_id": session_id}],
            ids=[doc_id]
        )
        print(f"   🧠 Memorized for session {session_id}: '{text_chunk[:50]}...'")

    def search_memory(self, session_id: str, query_embedding: list, k: int = 5) -> str:
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=k,
                where={"session_id": session_id}
            )
            retrieved_chunks = results['documents'][0]
            unique_chunks = list(dict.fromkeys(retrieved_chunks))
            context = "\n".join(unique_chunks)
            print(f"\n   🔍 Recalling context for session {session_id}:\n   ---\n   {context}\n   ---")
            return context
        except Exception as e:
            print(f"Error searching memory: {e}")
            return ""

    def get_history(self, session_id: str) -> list:
        """Retrieves all documents for a given session_id."""
        try:
            history = self.collection.get(where={"session_id": session_id})
            # The 'get' method doesn't sort by time, but this gives us the raw data.
            # For true chronological order, a timestamp would need to be stored in metadata.
            return history['documents']
        except Exception as e:
            print(f"Error retrieving history: {e}")
            return []
