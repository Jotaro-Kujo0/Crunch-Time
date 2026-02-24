"""
i18n_strings.py

Simple string catalog for UI localization. Stores translations in JSON files
under a `locales/` directory. This is intentionally minimal.
"""
import os
import json
from typing import Dict

LOCALES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locales')
DEFAULT_LOCALE = 'en'


def load_locale(locale: str) -> Dict[str, str]:
    path = os.path.join(LOCALES_DIR, f'{locale}.json')
    if not os.path.exists(path):
        path = os.path.join(LOCALES_DIR, f'{DEFAULT_LOCALE}.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


# Example usage: strings = load_locale('en'); strings.get('add_habit', 'Add Habit')
