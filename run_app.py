#!/usr/bin/env python3
import os
import sys
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
CANDIDATES = [os.path.join(ROOT, 'Files', 'Crunch_Tİme_UI.py'), os.path.join(ROOT, 'Crunch_Tİme_UI.py')]


def find_ui():
    for p in CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def main():
    ui = find_ui()
    if ui is None:
        print('No UI file found. Checked:')
        for c in CANDIDATES:
            print('  -', c)
        sys.exit(1)

    print(f'Launching {os.path.relpath(ui, ROOT)} using {sys.executable}')
    # run the UI file as a new process so it has a clean interpreter state
    subprocess.run([sys.executable, ui], cwd=ROOT)


if __name__ == '__main__':
    main()
