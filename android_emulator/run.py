#!/usr/bin/env python3
"""Standalone entry point; this entire directory may be copied elsewhere."""
import sys
from pathlib import Path

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from android_emulator.cli import main

if __name__ == '__main__':
    sys.exit(main())
