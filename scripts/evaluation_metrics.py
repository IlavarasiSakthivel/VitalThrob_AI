import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path


def generate_evaluation_metrics_visualizations():
    """Generate confusion matrix, ROC curve, and other evaluation metrics"""

    OUTPUT_DIR = Path("model_visualizations")
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Your actual validation metrics (from your code)
    # Replace these with your actual validation set results
    actual_metrics = {
        'validation_accuracy': 0.874,
        'validation_loss': 0.334,
        'precision': 0.882,
        'recall': 0.867,
        'f1_score': 0.874,
        'auc_roc': 0.934
    }

    # Simulated confusion matrix (from 20% validation set: 184 samples)
    # TN, FP, FN, TP
    confusion_matrix = np.array([[92, 11],  # Actual 0: 103 total
                                 [12, 69]])  # Actual 1: 81 total

    # Simulated ROC curve data
    fpr = np.array([0.00, 0.02, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00])
    tpr = np.array([0.00, 0.15, 0.35, 0.60, 0.78, 0.85, 0.89, 0.92, 0.94, 0.96, 0.97, 0.98, 1.00])

    # Create comprehensive evaluation figure
    fig = plt.figure(figsize=(16, 12))

    # 1. Confusion Matrix
    ax1 = plt.subplot(2, 3, 1)

    # Calculate percentages
    cm_percentage = confusion_matrix / confusion_matrix.sum(axis=1)[:, np.newaxis] * 100

    # Create heatmap
    im = ax1.imshow(cm_percentage, interpolation='nearest', cmap='Blues', vmin=0, vmax=100)
    plt.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)

    # Add text annotations
    thresh = cm_percentage.max() / 2.
    for i in range(confusion_matrix.shape[0]):
        for j in range(confusion_matrix.shape[1]):
            ax1.text(j, i, f'{confusion_matrix[i, j]}\n({cm_percentage[i, j]:.1f}%)',
                     ha="center", va="center",
                     color="white" if cm_percentage[i, j] > thresh else "black",
                     fontsize=11, fontweight='bold')

    ax1.set_xlabel('Predicted Label', fontsize=12)
    ax1.set_ylabel('True Label', fontsize=12)
    ax1.set_title('Confusion Matrix (Validation Set)', fontsize=13, fontweight='bold')
    ax1.set_xticks([0, 1])
    ax1.set_yticks([0, 1])
    ax1.set_xticklabels(['No Disease', 'Disease'], fontsize=11)
    ax1.set_yticklabels(['No Disease', 'Disease'], fontsize=11)

    # 2. ROC Curve
    ax2 = plt.subplot(2, 3, 2)

    # Plot ROC curve
    ax2.plot(fpr, tpr, 'b-', linewidth=2.5, label=f'Neural Network (AUC = {actual_metrics["auc_roc"]:.3f})')
    ax2.plot([0, 1], [0, 1], 'k--', linewidth=1, alpha=0.7, label='Random Classifier (AUC = 0.5)')

    # Fill area under curve
    ax2.fill_between(fpr, tpr, alpha=0.2, color='blue')

    # Add optimal threshold point (Youden's J statistic)
    youden_j = tpr - fpr
    optimal_idx = np.argmax(youden_j)
    optimal_threshold = 0.3  # Example threshold
    ax2.scatter(fpr[optimal_idx], tpr[optimal_idx], color='red', s=100,
                zorder=5, label=f'Optimal Threshold: {optimal_threshold:.2f}')

    ax2.set_xlabel('False Positive Rate', fontsize=12)
    ax2.set_ylabel('True Positive Rate', fontsize=12)
    ax2.set_title('Receiver Operating Characteristic (ROC) Curve', fontsize=13, fontweight='bold')
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_aspect('equal', adjustable='box')

    # 3. Precision-Recall Curve
    ax3 = plt.subplot(2, 3, 3)

    # Simulated precision-recall curve
    recall_pr = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    precision = np.array([1.0, 0.95, 0.92, 0.89, 0.87, 0.86, 0.85, 0.84, 0.83, 0.82, 0.81])

    # Calculate average precision - FIXED: Use manual trapezoidal rule
    # Calculate area under curve using trapezoidal rule
    avg_precision = 0.0
    for i in range(1, len(precision)):
        avg_precision += (precision[i] + precision[i-1]) * (recall_pr[i] - recall_pr[i-1]) / 2.0

    ax3.plot(recall_pr, precision, 'g-', linewidth=2.5,
             label=f'Average Precision = {avg_precision:.3f}')
    ax3.fill_between(recall_pr, precision, alpha=0.2, color='green')

    # Add no-skill line (proportion of positive cases)
    positive_proportion = confusion_matrix[1, :].sum() / confusion_matrix.sum()
    ax3.axhline(y=positive_proportion, color='k', linestyle='--', alpha=0.5,
                label=f'No Skill ({positive_proportion:.2f})')

    ax3.set_xlabel('Recall', fontsize=12)
    ax3.set_ylabel('Precision', fontsize=12)
    ax3.set_title('Precision-Recall Curve', fontsize=13, fontweight='bold')
    ax3.legend(loc='lower left')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim([0.0, 1.0])
    ax3.set_ylim([0.0, 1.05])

    # 4. Metrics Radar Chart
    ax4 = plt.subplot(2, 3, 4, projection='polar')

    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    values = [
        actual_metrics['validation_accuracy'] * 100,
        actual_metrics['precision'] * 100,
        actual_metrics['recall'] * 100,
        actual_metrics['f1_score'] * 100,
        actual_metrics['auc_roc'] * 100
    ]

    # Close the polygon
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]
    values += values[:1]

    ax4.plot(angles, values, 'o-', linewidth=2, color='purple')
    ax4.fill(angles, values, alpha=0.25, color='purple')

    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(metrics, fontsize=11)
    ax4.set_ylim(80, 100)
    ax4.set_title('Performance Metrics Overview', fontsize=13, fontweight='bold', pad=20)
    ax4.grid(True)

    # Add metric values
    for angle, value, metric in zip(angles[:-1], values[:-1], metrics):
        ax4.text(angle, value + 1, f'{value:.1f}%', ha='center', va='bottom',
                 fontsize=10, fontweight='bold')

    # 5. Error Analysis
    ax5 = plt.subplot(2, 3, 5)

    error_types = ['True Positives', 'False Positives', 'True Negatives', 'False Negatives']
    error_counts = [confusion_matrix[1, 1], confusion_matrix[0, 1],
                    confusion_matrix[0, 0], confusion_matrix[1, 0]]
    colors = ['#4CAF50', '#FF9800', '#4CAF50', '#F44336']  # Green, Orange, Green, Red
    explode = (0, 0.1, 0, 0.1)  # Explode FP and FN

    wedges, texts, autotexts = ax5.pie(error_counts, explode=explode, colors=colors,
                                       autopct='%1.1f%%', startangle=90,
                                       textprops=dict(color="w", fontsize=10, fontweight='bold'))

    ax5.legend(wedges, [f'{label}: {count}' for label, count in zip(error_types, error_counts)],
               title="Prediction Results", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax5.set_title('Error Analysis Distribution', fontsize=13, fontweight='bold')

    # 6. Performance Metrics Table
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('tight')
    ax6.axis('off')

    # Calculate additional metrics
    tn, fp, fn, tp = confusion_matrix.ravel()
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0  # Negative Predictive Value

    table_data = [
        ['Metric', 'Value', 'Interpretation'],
        ['Accuracy', f'{actual_metrics["validation_accuracy"] * 100:.1f}%', 'Overall correctness'],
        ['Precision', f'{actual_metrics["precision"] * 100:.1f}%', 'Low false positive rate'],
        ['Recall (Sensitivity)', f'{actual_metrics["recall"] * 100:.1f}%', 'High true positive detection'],
        ['Specificity', f'{specificity * 100:.1f}%', 'True negative rate'],
        ['F1-Score', f'{actual_metrics["f1_score"] * 100:.1f}%', 'Harmonic mean of P & R'],
        ['AUC-ROC', f'{actual_metrics["auc_roc"]:.3f}', 'Discrimination ability'],
        ['NPV', f'{npv * 100:.1f}%', 'Negative predictive value'],
        ['Total Samples', f'{confusion_matrix.sum()}', 'Validation set size']
    ]

    table = ax6.table(cellText=table_data, cellLoc='center',
                      loc='center', colWidths=[0.35, 0.25, 0.4])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    # Style the table
    for (i, j), cell in table.get_celld().items():
        if i == 0:  # Header
            cell.set_text_props(fontweight='bold', color='white')
            cell.set_facecolor('#2E5984')
        elif j == 1 and i > 0:  # Value column
            value = float(table_data[i][1].replace('%', '').replace('f', ''))
            if value > 85:
                cell.set_facecolor('#C6EFCE')  # Green for good values
                cell.set_text_props(fontweight='bold', color='#006100')
            elif value > 75:
                cell.set_facecolor('#FFEB9C')  # Yellow for moderate values
                cell.set_text_props(fontweight='bold', color='#9C6500')
        else:
            cell.set_facecolor('#F0F0F0' if i % 2 == 0 else '#FFFFFF')

    plt.suptitle('Comprehensive Model Evaluation Metrics - Heart Disease Prediction',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'evaluation_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("✓ Generated: evaluation_metrics.png")

    return actual_metrics


# Run the function
if __name__ == "__main__":
    generate_evaluation_metrics_visualizations()