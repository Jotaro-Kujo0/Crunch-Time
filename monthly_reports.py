"""
monthly_reports.py

Functions to produce simple monthly reports from habit calendars and total time tracker.
"""
from typing import Dict, Any
import calendar
from datetime import datetime
import csv
import os
from project_utils import safe_load_json


def generate_habit_month_report(persist_file: str, habit_id: str, year: int, month: int) -> Dict[str, Any]:
    """Return a summary for the given habit/month.
    Reads the same JSON used by the HabitCalendar (top-level 'calendars').
    """
    data = safe_load_json(persist_file) or {}
    key = f"{year:04d}-{month:02d}"
    month_data = data.get('calendars', {}).get(habit_id, {}).get(key, {})

    ndays = calendar.monthrange(year, month)[1]
    filled = 0
    partial = 0
    total_score = 0.0
    for d in range(1, ndays + 1):
        v = float(month_data.get(str(d), 0.0))
        total_score += v
        if v >= 0.99:
            filled += 1
        elif v > 0.0:
            partial += 1

    avg_completion = (total_score / ndays) if ndays else 0.0
    return {
        'habit_id': habit_id,
        'year': year,
        'month': month,
        'days': ndays,
        'full_days': filled,
        'partial_days': partial,
        'avg_completion': avg_completion,
    }


def export_habit_report_csv(report: Dict[str, Any], persist_file: str, out_path: str) -> str:
    """Export a CSV with per-day values for the month and a small summary header.
    Returns the output path on success.
    """
    data = safe_load_json(persist_file) or {}
    key = f"{report['year']:04d}-{report['month']:02d}"
    month_data = data.get('calendars', {}).get(report['habit_id'], {}).get(key, {})

    with open(out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Habit', report['habit_id']])
        writer.writerow(['Year', report['year']])
        writer.writerow(['Month', report['month']])
        writer.writerow([])
        writer.writerow(['Day', 'Completion'])
        ndays = report['days']
        for d in range(1, ndays + 1):
            writer.writerow([d, month_data.get(str(d), 0.0)])
        writer.writerow([])
        writer.writerow(['Full days', report['full_days']])
        writer.writerow(['Partial days', report['partial_days']])
        writer.writerow(['Average completion', report['avg_completion']])
    return out_path
