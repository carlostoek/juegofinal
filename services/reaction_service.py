class ReactionService:
    """Simple in-memory storage for message reactions."""

    def __init__(self) -> None:
        self._data: dict[int, dict[str, int]] = {}

    def add_reaction(self, message_id: int, reaction: str) -> None:
        counts = self._data.setdefault(message_id, {"👍": 0, "👎": 0})
        counts[reaction] = counts.get(reaction, 0) + 1

    def get_counts(self, message_id: int) -> dict[str, int]:
        return self._data.get(message_id, {"👍": 0, "👎": 0})


reaction_service = ReactionService()
