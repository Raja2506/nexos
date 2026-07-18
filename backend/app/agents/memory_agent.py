from app.agents.base_agent import BaseAgent
from app.memory.short_term import set_session_data, get_session_data
from app.memory.vector_store import add_memory, search_memory
import uuid


class MemoryAgent(BaseAgent):
    """
    Unified interface for both short-term (Redis) and long-term
    (ChromaDB) memory. Other agents call THIS agent instead of
    talking to Redis/ChromaDB directly.
    """

    def __init__(self):
        super().__init__(name="MemoryAgent")

    async def run(self, input_data: dict) -> dict:
        action = input_data["action"]

        if action == "remember_short":
            return self._remember_short(input_data)
        elif action == "remember_long":
            return self._remember_long(input_data)
        elif action == "recall_short":
            return self._recall_short(input_data)
        elif action == "recall_long":
            return self._recall_long(input_data)
        else:
            raise ValueError(f"Unknown memory action: {action}")

    def _remember_short(self, input_data: dict) -> dict:
        session_id = input_data["session_id"]
        key = input_data["key"]
        value = input_data["value"]
        set_session_data(session_id, key, value)
        self.log(f"Stored short-term: {key} for session {session_id}")
        return {"stored": True}

    def _recall_short(self, input_data: dict) -> dict:
        session_id = input_data["session_id"]
        key = input_data["key"]
        value = get_session_data(session_id, key)
        self.log(f"Recalled short-term: {key} -> {'found' if value else 'not found'}")
        return {"value": value}

    def _remember_long(self, input_data: dict) -> dict:
        text = input_data["text"]
        metadata = input_data.get("metadata", {})
        memory_id = f"mem_{uuid.uuid4().hex[:8]}"
        add_memory(memory_id, text, metadata)
        self.log(f"Stored long-term memory: {memory_id}")
        return {"memory_id": memory_id}

    def _recall_long(self, input_data: dict) -> dict:
        query = input_data["query"]
        n_results = input_data.get("n_results", 3)
        results = search_memory(query, n_results)
        self.log(f"Recalled {len(results['documents'][0])} long-term memories")
        return {"memories": results["documents"][0]}