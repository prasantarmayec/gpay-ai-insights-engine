"""
Main entry point for GPay AI Insights Engine.

Usage:
    python app/main.py data/My\ Activity.html
"""

import sys
import os
from insights import load_and_analyze

def main():
    if len(sys.argv) < 2:
        print("Usage: python app/main.py <path_to_My_Activity.html or .csv>")
        sys.exit(1)
    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        sys.exit(1)
    load_and_analyze(input_path)

if __name__ == "__main__":
    main()
