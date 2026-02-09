from pathlib import Path
import os


def setup_project_structure():
    """Create proper project directory structure"""

    directories = [
        "artifacts_nn",
        "eda_charts",
        "model_visualizations",
        "dataset",
        "backend",
        "frontend/src",
        "logs",
        "reports"
    ]

    print("Setting up project directory structure...")

    # Create all directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}/")

    # Create __init__.py files
    init_files = [
        "backend/__init__.py",
        "frontend/__init__.py"
    ]

    for init_file in init_files:
        Path(init_file).touch()
        print(f"✓ Created: {init_file}")

    print("\nProject structure ready!")
    print("Place your train.csv file in the 'dataset/' folder.")


if __name__ == "__main__":
    setup_project_structure()