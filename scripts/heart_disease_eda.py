import pandas as pd
import matplotlib

# Set backend to 'Agg' to avoid display issues
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from pathlib import Path
import sys


def setup_plotting():
    """Setup matplotlib with proper configuration"""
    plt.rcParams['figure.figsize'] = [12, 8]
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    sns.set_style("whitegrid")

    # Disable interactive mode
    plt.ioff()


def clean_target_column(df):
    """Clean the target column exactly as in train_model.py"""
    target_col = "Heart Disease"

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    target_clean = target_col.lower().replace(' ', '_')

    if target_clean not in df.columns:
        print(f"Warning: Target column '{target_clean}' not found in dataset")
        print(f"Available columns: {list(df.columns)}")
        # Try to find similar column
        for col in df.columns:
            if 'heart' in col.lower() or 'disease' in col.lower():
                target_clean = col
                print(f"Using column: {target_clean}")
                break

    # Clean target values
    df[target_clean] = df[target_clean].astype(str).str.strip().str.lower()

    mapping = {
        'presence': 1,
        'absence': 0,
        'yes': 1,
        'no': 0,
        '1': 1,
        '0': 0,
        'true': 1,
        'false': 0,
        '1.0': 1,
        '0.0': 0,
        'positive': 1,
        'negative': 0
    }

    df[target_clean] = df[target_clean].map(mapping)

    # Convert to integer
    df[target_clean] = pd.to_numeric(df[target_clean], errors='coerce')

    return df, target_clean


def load_and_prepare_data():
    """Load and prepare the dataset"""
    # Get the script's directory
    script_dir = Path(__file__).parent.absolute()

    # Based on your folder structure: script is in HeartDisease/scripts/
    # Data is in HeartDisease/dataset/
    # So go up one level (to HeartDisease), then into dataset
    base_dir = script_dir.parent  # This is the HeartDisease directory

    # Try multiple possible locations for the dataset
    possible_paths = [
        base_dir / "train.csv",  # Directly in HeartDisease
        base_dir / "dataset" / "train.csv",  # In HeartDisease/dataset/
        script_dir / "train.csv",  # In scripts directory
        script_dir / "dataset" / "train.csv",  # In scripts/dataset/
        Path.cwd() / "train.csv",  # Current working directory
        Path.cwd() / "dataset" / "train.csv",  # Current working directory's dataset
    ]

    data_path = None
    for path in possible_paths:
        if path.exists():
            data_path = path
            print(f"Found dataset at: {data_path}")
            break

    if data_path is None:
        print("Error: Could not find train.csv")
        print("Current working directory:", Path.cwd())
        print("Script directory:", script_dir)
        print("Base directory:", base_dir)
        print("Please place train.csv in one of these locations:")
        for path in possible_paths:
            print(f"  - {path}")
        return None

    try:
        df = pd.read_csv(data_path)
        print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None


def generate_eda_charts(df):
    """Generate EDA charts for heart disease dataset"""
    # Get the script's directory
    script_dir = Path(__file__).parent.absolute()
    base_dir = script_dir.parent  # HeartDisease directory

    # Setup output directory - use base_dir to save in HeartDisease/eda_charts
    output_dir = base_dir / "eda_charts"
    output_dir.mkdir(exist_ok=True)

    # Clean target column
    df, target_col = clean_target_column(df)

    # Check if cleaning was successful
    if df[target_col].isnull().any():
        print(f"Warning: {df[target_col].isnull().sum()} null values in target column")
        df = df.dropna(subset=[target_col])

    print(f"Target column: {target_col}")
    print(f"Class distribution:\n{df[target_col].value_counts()}")

    # 1. Target Distribution
    print("\nGenerating Chart 1: Target Distribution...")
    plt.figure(figsize=(10, 6))
    target_counts = df[target_col].value_counts()
    colors = ['#4CAF50', '#F44336']
    bars = plt.bar(['No Heart Disease (0)', 'Heart Disease (1)'],
                   target_counts.values, color=colors, alpha=0.8)

    for bar, count in zip(bars, target_counts.values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                 f'{count} ({count / len(df) * 100:.1f}%)',
                 ha='center', va='bottom')

    plt.title('Distribution of Heart Disease Cases', fontweight='bold')
    plt.xlabel('Diagnosis')
    plt.ylabel('Number of Patients')
    plt.ylim(0, max(target_counts.values) * 1.15)
    plt.tight_layout()
    plt.savefig(output_dir / '1_target_distribution.png')
    plt.close()

    # 2. Correlation Heatmap
    print("Generating Chart 2: Correlation Heatmap...")

    # Select numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # Remove target from correlation matrix
    if target_col in numeric_cols:
        numeric_cols.remove(target_col)

    if len(numeric_cols) > 1:
        plt.figure(figsize=(12, 10))
        corr_matrix = df[numeric_cols].corr()

        # Create mask for upper triangle
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm',
                    fmt='.2f', linewidths=0.5, square=True, cbar_kws={"shrink": 0.8})

        plt.title('Correlation Matrix of Clinical Features', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_dir / '2_correlation_heatmap.png')
        plt.close()

    # 3. Age Distribution
    if 'age' in df.columns:
        print("Generating Chart 3: Age Distribution...")
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Histogram
        for diagnosis, color, label in [(0, '#4CAF50', 'No Disease'), (1, '#F44336', 'Disease')]:
            subset = df[df[target_col] == diagnosis]['age']
            ax1.hist(subset, bins=20, alpha=0.6, color=color, label=label, edgecolor='black')

        ax1.set_title('Age Distribution by Heart Disease Status', fontweight='bold')
        ax1.set_xlabel('Age (Years)')
        ax1.set_ylabel('Count')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Box plot
        box_data = [df[df[target_col] == 0]['age'], df[df[target_col] == 1]['age']]
        bp = ax2.boxplot(box_data, labels=['No Disease', 'Disease'], patch_artist=True)

        colors_box = ['#4CAF50', '#F44336']
        for patch, color in zip(bp['boxes'], colors_box):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax2.set_title('Age Distribution Comparison', fontweight='bold')
        ax2.set_ylabel('Age (Years)')
        ax2.grid(True, alpha=0.3)

        plt.suptitle('Age Analysis in Relation to Heart Disease', fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_dir / '3_age_distribution.png')
        plt.close()

    # 4. Feature Distributions
    print("Generating Chart 4: Feature Distributions...")

    # Select top features
    features_to_plot = ['age', 'bp', 'cholesterol', 'max_hr', 'st_depression']
    available_features = [f for f in features_to_plot if f in df.columns]

    if len(available_features) >= 2:
        n_cols = 2
        n_rows = (len(available_features) + 1) // 2
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 4))

        if n_rows == 1:
            axes = axes.reshape(1, -1)

        axes = axes.flatten()

        for idx, feature in enumerate(available_features):
            if idx < len(axes):
                ax = axes[idx]

                for diagnosis, color, label in [(0, '#4CAF50', 'No Disease'), (1, '#F44336', 'Disease')]:
                    subset = df[df[target_col] == diagnosis][feature]
                    if len(subset) > 0:
                        ax.hist(subset.dropna(), bins=20, alpha=0.5, color=color,
                                label=label, edgecolor='black')

                ax.set_title(f'{feature.replace("_", " ").title()}', fontweight='bold')
                ax.set_xlabel(feature.replace('_', ' ').title())
                ax.set_ylabel('Count')
                ax.legend()
                ax.grid(True, alpha=0.3)

        # Hide empty subplots
        for idx in range(len(available_features), len(axes)):
            axes[idx].set_visible(False)

        plt.suptitle('Clinical Feature Distributions by Heart Disease Status', fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_dir / '4_feature_distributions.png')
        plt.close()

    # 5. Summary Statistics
    print("\nGenerating Summary Statistics...")

    # Save summary statistics
    summary_path = output_dir / 'summary_statistics.csv'
    df.describe().to_csv(summary_path)

    # Create text summary
    with open(output_dir / 'dataset_summary.txt', 'w') as f:
        f.write("HEART DISEASE DATASET SUMMARY\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Records: {len(df)}\n")
        f.write(f"Features: {len(df.columns)}\n")
        f.write(f"Target Variable: {target_col}\n")
        f.write(f"Positive Cases (Heart Disease): {df[target_col].sum()} ({df[target_col].mean() * 100:.1f}%)\n")
        f.write(
            f"Negative Cases (No Disease): {len(df) - df[target_col].sum()} ({100 - df[target_col].mean() * 100:.1f}%)\n\n")

        f.write("MISSING VALUES:\n")
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if len(missing) == 0:
            f.write("  No missing values found\n")
        else:
            for col, count in missing.items():
                f.write(f"  {col}: {count} missing ({count / len(df) * 100:.1f}%)\n")

    print(f"\n✓ All EDA charts saved in: {output_dir}")
    print("\nGenerated files:")
    for file in sorted(output_dir.glob('*.png')):
        print(f"  - {file.name}")


def main():
    """Main function"""
    print("=" * 60)
    print("HEART DISEASE EDA - FIXED VERSION")
    print("=" * 60)

    # Setup plotting
    setup_plotting()

    # Load data
    df = load_and_prepare_data()
    if df is None:
        return

    # Generate charts
    generate_eda_charts(df)

    print("\n" + "=" * 60)
    print("EDA COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    main()