"""
account_manager.py

Simple local account manager storing users in a JSON file under the project root.
Stores salted PBKDF2 password hashes and per-user settings (timezone, clock_format).
"""
import os
import hashlib
import secrets
from typing import Optional, Dict, Any
from project_utils import safe_load_json, atomic_write_json


class AccountManager:
    def __init__(self, path: str):
        self.path = path
        self.data = safe_load_json(path) or {}
        if 'users' not in self.data:
            self.data['users'] = []
            atomic_write_json(self.path, self.data)

    def _hash(self, password: str, salt: bytes) -> str:
        h = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 200_000)
        return h.hex()

    def create_user(self, username: str, password: str) -> bool:
        username = username.strip()
        if not username or not password:
            return False
        if any(u.get('username') == username for u in self.data.get('users', [])):
            return False
        salt = secrets.token_bytes(16)
        user = {
            'id': username.lower().replace(' ', '_'),
            'username': username,
            'salt': salt.hex(),
            'pw_hash': self._hash(password, salt),
            'settings': {'timezone': 'UTC', 'clock_24h': True, 'show_seconds': True}
        }
        self.data.setdefault('users', []).append(user)
        atomic_write_json(self.path, self.data)
        return True

    def verify(self, username: str, password: str) -> bool:
        u = next((x for x in self.data.get('users', []) if x.get('username') == username), None)
        if not u:
            return False
        salt = bytes.fromhex(u.get('salt', ''))
        return self._hash(password, salt) == u.get('pw_hash')

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        return next((x for x in self.data.get('users', []) if x.get('username') == username), None)

    def update_settings(self, username: str, settings: Dict[str, Any]) -> None:
        u = self.get_user(username)
        if not u:
            return
        u.setdefault('settings', {}).update(settings)
        atomic_write_json(self.path, self.data)

    def list_users(self):
        return [u.get('username') for u in self.data.get('users', [])]
