#!/usr/bin/env python3
"""
Medsim GUI Launcher
A simple launcher script to run the medical simulation GUI.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from medsim.gui.app import main
    
    if __name__ == "__main__":
        print("Starting Medsim GUI...")
        main()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install PySide6")
    sys.exit(1)
    
except Exception as e:
    print(f"Error starting GUI: {e}")
    sys.exit(1) 