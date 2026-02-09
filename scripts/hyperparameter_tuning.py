import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path


def generate_hyperparameter_tuning_visualizations():
    """Visualize Keras Tuner hyperparameter optimization results"""

    OUTPUT_DIR = Path("model_visualizations")
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Simulated hyperparameter tuning results (replace with actual tuner.results)
    # Based on your Hyperband tuner configuration
    trials_data = [
        {'num_layers': 2, 'units_0': 192, 'units_1': 128, 'dropout_rate': 0.3,
         'learning_rate': 0.001, 'val_accuracy': 0.874, 'score': 0.874},
        {'num_layers': 3, 'units_0': 160, 'units_1': 96, 'units_2': 64, 'dropout_rate': 0.4,
         'learning_rate': 0.0001, 'val_accuracy': 0.862, 'score': 0.862},
        {'num_layers': 1, 'units_0': 256, 'dropout_rate': 0.2,
         'learning_rate': 0.01, 'val_accuracy': 0.845, 'score': 0.845},
        {'num_layers': 2, 'units_0': 128, 'units_1': 64, 'dropout_rate': 0.5,
         'learning_rate': 0.001, 'val_accuracy': 0.868, 'score': 0.868},
        {'num_layers': 2, 'units_0': 224, 'units_1': 160, 'dropout_rate': 0.3,
         'learning_rate': 0.0005, 'val_accuracy': 0.871, 'score': 0.871},
    ]

    # Convert to DataFrame for easier plotting
    df_trials = pd.DataFrame(trials_data)

    # Create visualization figure
    fig = plt.figure(figsize=(16, 12))

    # 1. Hyperparameter Importance Heatmap
    ax1 = plt.subplot(2, 2, 1)

    # Create correlation matrix
    params_to_correlate = ['num_layers', 'dropout_rate', 'learning_rate']
    if all(p in df_trials.columns for p in params_to_correlate):
        corr_matrix = df_trials[params_to_correlate + ['val_accuracy']].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax1)
        ax1.set_title('Hyperparameter Correlation with Accuracy', fontsize=12, fontweight='bold')

    # 2. Learning Rate vs Accuracy
    ax2 = plt.subplot(2, 2, 2)
    if 'learning_rate' in df_trials.columns:
        scatter = ax2.scatter(df_trials['learning_rate'], df_trials['val_accuracy'],
                              c=df_trials['num_layers'], s=200, alpha=0.7,
                              cmap='viridis', edgecolors='black')
        ax2.set_xscale('log')
        ax2.set_xlabel('Learning Rate (log scale)', fontsize=11)
        ax2.set_ylabel('Validation Accuracy', fontsize=11)
        ax2.set_title('Learning Rate Optimization', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        # Add colorbar for number of layers
        cbar = plt.colorbar(scatter, ax=ax2)
        cbar.set_label('Number of Layers', fontsize=10)

    # 3. Dropout Rate vs Accuracy
    ax3 = plt.subplot(2, 2, 3)
    if 'dropout_rate' in df_trials.columns:
        colors = plt.cm.RdYlGn(df_trials['val_accuracy'] / df_trials['val_accuracy'].max())
        bars = ax3.bar(range(len(df_trials)), df_trials['dropout_rate'],
                       color=colors, edgecolor='black', alpha=0.8)
        ax3.set_xlabel('Trial Index', fontsize=11)
        ax3.set_ylabel('Dropout Rate', fontsize=11)
        ax3.set_title('Dropout Rate by Trial (Colored by Accuracy)', fontsize=12, fontweight='bold')
        ax3.set_xticks(range(len(df_trials)))
        ax3.set_xticklabels([f'T{i + 1}' for i in range(len(df_trials))])

        # Add accuracy values on top
        for i, (bar, acc) in enumerate(zip(bars, df_trials['val_accuracy'])):
            ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                     f'{acc:.3f}', ha='center', va='bottom', fontsize=9)

    # 4. Validation Accuracy Distribution
    ax4 = plt.subplot(2, 2, 4)
    if 'val_accuracy' in df_trials.columns:
        # Box plot
        box = ax4.boxplot(df_trials['val_accuracy'], patch_artist=True,
                          boxprops=dict(facecolor='lightblue', alpha=0.7))

        # Add individual points
        for i, acc in enumerate(df_trials['val_accuracy']):
            ax4.scatter(1, acc, color='red', s=50, alpha=0.6, zorder=3)

        # Highlight best trial
        best_acc = df_trials['val_accuracy'].max()
        ax4.scatter(1, best_acc, color='green', s=100, marker='*',
                    label=f'Best: {best_acc:.3f}', zorder=4)

        ax4.set_ylabel('Validation Accuracy', fontsize=11)
        ax4.set_title('Accuracy Distribution Across Trials', fontsize=12, fontweight='bold')
        ax4.set_xticks([])
        ax4.legend()
        ax4.grid(True, alpha=0.3, axis='y')

    plt.suptitle('Keras Tuner Hyperparameter Optimization Results',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'hyperparameter_tuning.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Create optimal hyperparameters table
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('tight')
    ax.axis('off')

    # Optimal hyperparameters from your model
    optimal_params = [
        ['Parameter', 'Search Range', 'Optimal Value'],
        ['Hidden Layers', '1-3', '2'],
        ['Layer 1 Units', '32-256', '192'],
        ['Layer 2 Units', '32-256', '128'],
        ['Dropout Rate', '0.1-0.5', '0.3'],
        ['Learning Rate', '[1e-2, 1e-3, 1e-4]', '1e-3'],
        ['Optimizer', 'Adam', 'Adam'],
        ['Batch Size', '32', '32'],
        ['Epochs', '20 (Early Stopping)', 'Converged at 15']
    ]

    table = ax.table(cellText=optimal_params, cellLoc='center',
                     loc='center', colWidths=[0.3, 0.4, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)

    # Style the table
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # Header row
            cell.set_text_props(fontweight='bold', color='white')
            cell.set_facecolor('#4F81BD')
        else:
            cell.set_facecolor('#D9E1F2' if i % 2 == 0 else '#FFFFFF')

    plt.title('Optimal Hyperparameters from Keras Tuner', fontsize=14, fontweight='bold', pad=20)
    plt.savefig(OUTPUT_DIR / 'optimal_hyperparameters.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("✓ Generated: hyperparameter_tuning.png")
    print("✓ Generated: optimal_hyperparameters.png")

    return df_trials


# Run the function
if __name__ == "__main__":
    generate_hyperparameter_tuning_visualizations()