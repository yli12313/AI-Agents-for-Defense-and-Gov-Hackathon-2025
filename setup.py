#!/usr/bin/env python3
"""
Setup script for the Port City Vulnerability Scanner
Ensures that all required directories exist in the project structure
"""
import os
import shutil


def ensure_dir(directory):
    """
    Create directory if it doesn't exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")


def create_project_structure():
    """
    Create the project directory structure
    """
    # Define the base directories
    dirs = [
        "src",
        "src/data",
        "src/data/shodan",
        "src/data/shodan/samples",
        "src/utils",
    ]

    # Create each directory
    for directory in dirs:
        ensure_dir(directory)

    print("\nProject structure setup complete!")


if __name__ == "__main__":
    print("Setting up Port City Vulnerability Scanner project structure...")
    create_project_structure()
    print("\nSetup complete! You can now run the application with:\n")
    print("streamlit run src/app.py") 