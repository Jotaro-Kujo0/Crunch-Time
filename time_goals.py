"""
time_goals.py

Simple time goal tracker. Define goals (daily/weekly/monthly) and check progress
against TotalTimeTracker and habit calendars.
"""
from typing import Dict, Any, List
from datetime import date, timedelta
from project_utils import safe_load_json
import calendar


def add_goal(goals_file: str, goal_id: str, name: str, kind: str, seconds_target: float) -> None:
    """Persist a simple goal. kind in {'daily','weekly','monthly'}"""
    data = safe_load_json(goals_file) or {}
    data.setdefault('goals', {})
    data['goals'][goal_id] = {'id': goal_id, 'name': name, 'kind': kind, 'target_seconds': seconds_target}
    from project_utils import atomic_write_json
    atomic_write_json(goals_file, data)


def get_goals(goals_file: str) -> Dict[str, Any]:
    return safe_load_json(goals_file) or {}


def progress_for_goal(goal: Dict[str, Any], total_tracker: Any, year: int, month: int) -> float:
    """Return completion percent (0..1) for the given goal using the total_tracker
    which must expose total_seconds and be queryable for date ranges (approx).
    This is a lightweight function and expects goal kinds 'daily','weekly','monthly'."""
    kind = goal.get('kind')
    target = float(goal.get('target_seconds', 0.0))
    if kind == 'monthly':
        # approximate: use total_tracker.total_seconds for now
        return min(1.0, total_tracker.total_seconds / target) if target > 0 else 0.0
    # for daily/weekly we'd integrate with more detailed per-day data
    return 0.0
