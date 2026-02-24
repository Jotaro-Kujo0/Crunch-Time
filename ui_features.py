"""
ui_features.py

Placeholders and helpers for UI features and layout configuration.
- centralize sizes, margins, and theme options
- helper to move widgets between containers
"""
from typing import Any
import tkinter as tk


THEME = {
    'bg': '#ffffff',
    'fg': '#2e7d32',
    'accent': '#4caf50',
}


def move_widget(widget: tk.Widget, new_parent: tk.Widget, pack_args: dict = None, grid_args: dict = None):
    # detach from old layout
    try:
        widget.pack_forget()
    except Exception:
        pass
    try:
        widget.grid_forget()
    except Exception:
        pass
    # add to new parent
    widget.master = new_parent
    if pack_args is not None:
        widget.pack(**pack_args)
    elif grid_args is not None:
        widget.grid(**grid_args)
    else:
        widget.pack()


# helper to compute a darker/lighter color
def adjust_color(hex_color: str, factor: float) -> str:
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
