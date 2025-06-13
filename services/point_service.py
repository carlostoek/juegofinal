import math
from typing import Dict


class PointService:
    """Service for managing user points and levels."""

    REGISTRATION_BONUS = 10
    DAILY_BONUS = 1

    def __init__(self) -> None:
        # Map user identifiers to their point totals
        self._points: Dict[str, int] = {}

    def register_user(self, user_id: str) -> None:
        """Register a user and award registration bonus points."""
        self._points[user_id] = self._points.get(user_id, 0) + self.REGISTRATION_BONUS

    def add_daily_points(self, user_id: str, days: int = 1) -> None:
        """Add daily bonus points for the given number of days."""
        if days < 0:
            raise ValueError("days must be non-negative")
        self._points[user_id] = self._points.get(user_id, 0) + self.DAILY_BONUS * days

    def get_points(self, user_id: str) -> int:
        """Return the current point total for a user."""
        return self._points.get(user_id, 0)

    def get_level(self, user_id: str) -> int:
        """Return the user's level based on their points."""
        points = self.get_points(user_id)
        return math.floor(points / 100)

    def get_rewards(self, user_id: str) -> int:
        """Return number of rewards earned based on points."""
        return self.get_points(user_id) // 50

    def get_budget(self, user_id: str) -> int:
        """Simple budget calculation derived from points."""
        return self.get_points(user_id) // 10

    def get_leaderboard(self, limit: int = 10) -> list[tuple[str, int]]:
        """Return top users sorted by points."""
        return sorted(
            self._points.items(), key=lambda x: x[1], reverse=True
        )[:limit]

    def get_position(self, user_id: str) -> int:
        """Return the ranking position for a user (1-indexed)."""
        sorted_users = sorted(
            self._points.items(), key=lambda x: x[1], reverse=True
        )
        for index, (uid, _) in enumerate(sorted_users, start=1):
            if uid == user_id:
                return index
        return len(sorted_users) + 1


# Shared instance used across handlers
point_service = PointService()
