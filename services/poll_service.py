from typing import Optional


class PollService:
    """Track polls created by the bot."""

    def __init__(self) -> None:
        self._polls: dict[str, int] = {}

    def add_poll(self, poll_id: str, message_id: int) -> None:
        self._polls[poll_id] = message_id

    def get_message_id(self, poll_id: str) -> Optional[int]:
        return self._polls.get(poll_id)

    def remove_poll(self, poll_id: str) -> None:
        self._polls.pop(poll_id, None)


poll_service = PollService()
