import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path


def generate_model_performance_visualizations():
    """Generate performance comparison visualizations"""

    OUTPUT_DIR = Path("model_visualizations")
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Model comparison data (from your report)
    models = ['Logistic Regression', 'Random Forest', 'Support Vector Machine',
              'Proposed Neural Network', 'Neural Network (Kaggle)']

    # Metrics for each model
    metrics_data = {
        'Accuracy': [76.3, 82.7, 79.8, 87.4, 88.0],  # Percentage
        'Precision': [75.1, 83.2, 78.5, 88.2, 87.8],
        'Recall': [77.8, 81.9, 80.2, 86.7, 87.5],
        'F1-Score': [76.4, 82.5, 79.3, 87.4, 87.6],
        'AUC-ROC': [0.834, 0.896, 0.867, 0.934, 0.880]
    }

    # Create comprehensive comparison figure
    fig = plt.figure(figsize=(18, 12))

    # 1. Radar Chart for Model Comparison
    ax1 = plt.subplot(2, 3, 1, projection='polar')

    # Normalize metrics for radar chart
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    num_vars = len(metrics)

    # Calculate angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Close the loop

    # Plot each model
    for i, model in enumerate(models):
        values = [metrics_data[m][i] / 100 if m != 'AUC-ROC' else metrics_data[m][i]
                  for m in metrics]
        values += values[:1]  # Close the loop

        # Scale AUC-ROC to percentage for consistent scaling
        if metrics_data['AUC-ROC'][i] < 1:
            values[-1] = metrics_data['AUC-ROC'][i] * 100

        ax1.plot(angles, values, 'o-', linewidth=2, label=model, alpha=0.7)
        ax1.fill(angles, values, alpha=0.1)

    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(metrics, fontsize=10)
    ax1.set_ylim(70, 100)
    ax1.set_title('Model Performance Radar Chart', fontsize=12, fontweight='bold', pad=20)
    ax1.grid(True)
    ax1.legend(bbox_to_anchor=(1.1, 1.05), fontsize=9)

    # 2. Bar Chart: Accuracy Comparison
    ax2 = plt.subplot(2, 3, 2)

    bars = ax2.bar(models, metrics_data['Accuracy'],
                   color=['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2'],
                   edgecolor='black', alpha=0.8)

    # Add value labels
    for bar, acc in zip(bars, metrics_data['Accuracy']):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                 f'{acc}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_ylabel('Accuracy (%)', fontsize=11)
    ax2.set_title('Model Accuracy Comparison', fontsize=12, fontweight='bold')
    ax2.set_ylim(70, 95)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')

    # Highlight best model
    best_idx = metrics_data['Accuracy'].index(max(metrics_data['Accuracy']))
    bars[best_idx].set_edgecolor('red')
    bars[best_idx].set_linewidth(2)

    # 3. Precision-Recall Trade-off
    ax3 = plt.subplot(2, 3, 3)

    colors = plt.cm.viridis(np.linspace(0, 1, len(models)))
    for i, model in enumerate(models):
        ax3.scatter(metrics_data['Precision'][i], metrics_data['Recall'][i],
                    s=200, c=[colors[i]], alpha=0.7, edgecolors='black',
                    label=model)

    ax3.set_xlabel('Precision (%)', fontsize=11)
    ax3.set_ylabel('Recall (%)', fontsize=11)
    ax3.set_title('Precision-Recall Trade-off', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(70, 95)
    ax3.set_ylim(70, 95)

    # Add diagonal line (perfect balance)
    ax3.plot([70, 95], [70, 95], 'k--', alpha=0.3, label='Perfect Balance')
    ax3.legend(fontsize=9)

    # 4. F1-Score Comparison
    ax4 = plt.subplot(2, 3, 4)

    x_pos = np.arange(len(models))
    width = 0.6

    bars_f1 = ax4.bar(x_pos, metrics_data['F1-Score'], width,
                      color=plt.cm.Set3(np.linspace(0, 1, len(models))),
                      edgecolor='black', alpha=0.8)

    ax4.set_xlabel('Model', fontsize=11)
    ax4.set_ylabel('F1-Score', fontsize=11)
    ax4.set_title('F1-Score Comparison (Harmonic Mean)', fontsize=12, fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels([m.split()[0] for m in models], fontsize=10)
    ax4.set_ylim(70, 95)
    ax4.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, f1 in zip(bars_f1, metrics_data['F1-Score']):
        ax4.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 0.5,
                 f'{f1:.1f}', ha='center', va='bottom', fontsize=9)

    # 5. AUC-ROC Comparison
    ax5 = plt.subplot(2, 3, 5)

    # Convert AUC to percentage for consistency
    auc_percentage = [auc * 100 for auc in metrics_data['AUC-ROC']]

    bars_auc = ax5.bar(models, auc_percentage,
                       color=plt.cm.coolwarm(np.linspace(0, 1, len(models))),
                       edgecolor='black', alpha=0.8)

    ax5.set_ylabel('AUC-ROC (%)', fontsize=11)
    ax5.set_title('Area Under ROC Curve Comparison', fontsize=12, fontweight='bold')
    ax5.set_ylim(80, 100)
    plt.setp(ax5.xaxis.get_majorticklabels(), rotation=45, ha='right')
    ax5.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, auc in zip(bars_auc, metrics_data['AUC-ROC']):
        ax5.text(bar.get_x() + bar.get_width() / 2., auc * 100 + 0.5,
                 f'{auc:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 6. Performance Improvement Table
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('tight')
    ax6.axis('off')

    # Calculate improvements over baseline
    baseline_accuracy = metrics_data['Accuracy'][0]  # Logistic Regression
    improvements = []

    for i, model in enumerate(models):
        if i == 0:
            improvement = "Baseline"
        else:
            improvement = f"+{metrics_data['Accuracy'][i] - baseline_accuracy:.1f}%"
        improvements.append(improvement)

    table_data = list(zip(models, [f"{acc}%" for acc in metrics_data['Accuracy']], improvements))
    table_data.insert(0, ('Model', 'Accuracy', 'Improvement'))

    table = ax6.table(cellText=table_data, cellLoc='center',
                      loc='center', colWidths=[0.4, 0.3, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    # Style the table
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # Header
            cell.set_text_props(fontweight='bold', color='white')
            cell.set_facecolor('#2E5984')
        elif 'Neural' in table_data[i][0]:  # Highlight neural networks
            cell.set_facecolor('#E6F3FF')
            if j == 2 and '+' in table_data[i][2]:
                cell.set_text_props(fontweight='bold', color='green')
        else:
            cell.set_facecolor('#F0F0F0' if i % 2 == 0 else '#FFFFFF')

    plt.suptitle('Comprehensive Model Performance Analysis',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'model_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("✓ Generated: model_performance_comparison.png")

    return metrics_data


# Run the function
if __name__ == "__main__":
    generate_model_performance_visualizations()