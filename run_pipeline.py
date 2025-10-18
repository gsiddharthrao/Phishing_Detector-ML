#!/usr/bin/env python3
"""
Full pipeline script to preprocess data, train model, and run the Flask app.
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(e.stderr)
        sys.exit(1)

def main():
    print("Starting PhishShield: AI Guardian Pipeline...")

    # Step 1: Generate demo data (optional)
    print("\nStep 1: Generating demo data...")
    run_command("python src/demo_data.py")

    # Step 2: Preprocess data
    print("\nStep 2: Preprocessing data...")
    run_command("python src/preprocess.py")

    # Step 3: Train model
    print("\nStep 3: Training model...")
    run_command("python src/train.py")

    # Step 4: Run Flask app
    print("\nStep 4: Starting Flask web application...")
    print("Open your browser and go to http://127.0.0.1:5000/")
    run_command("python requirements/app.py")

if __name__ == "__main__":
    main()
