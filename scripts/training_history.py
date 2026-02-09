import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path


def generate_training_history_visualization():
    """Generate training history visualization from your model training"""

    # Configuration
    OUTPUT_DIR = Path("../model_visualizations")
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Simulated training history (replace with your actual history from model.fit())
    # In practice, you should capture history = model.fit(...) and save history.history
    epochs = 20
    training_history = {
        'loss': [0.693, 0.642, 0.612, 0.583, 0.554, 0.528, 0.503, 0.481, 0.461, 0.443,
                 0.426, 0.411, 0.397, 0.385, 0.374, 0.364, 0.355, 0.347, 0.340, 0.334],
        'accuracy': [0.512, 0.584, 0.624, 0.658, 0.689, 0.712, 0.732, 0.749, 0.763, 0.775,
                     0.786, 0.795, 0.803, 0.810, 0.816, 0.821, 0.826, 0.830, 0.834, 0.837],
        'val_loss': [0.691, 0.652, 0.625, 0.598, 0.572, 0.548, 0.525, 0.504, 0.485, 0.468,
                     0.453, 0.440, 0.429, 0.420, 0.413, 0.408, 0.404, 0.401, 0.399, 0.398],
        'val_accuracy': [0.520, 0.592, 0.638, 0.672, 0.701, 0.724, 0.743, 0.758, 0.771, 0.782,
                         0.791, 0.799, 0.805, 0.810, 0.814, 0.817, 0.820, 0.822, 0.823, 0.824]
    }

    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    # Plot 1: Training & Validation Loss
    ax1.plot(range(1, epochs + 1), training_history['loss'], 'b-', linewidth=2, label='Training Loss')
    ax1.plot(range(1, epochs + 1), training_history['val_loss'], 'r-', linewidth=2, label='Validation Loss')
    ax1.set_title('Training vs Validation Loss', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Binary Crossentropy Loss', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(range(1, epochs + 1, 2))

    # Highlight the best epoch (minimum validation loss)
    best_epoch = np.argmin(training_history['val_loss']) + 1
    ax1.axvline(x=best_epoch, color='green', linestyle='--', alpha=0.7, label=f'Best Epoch: {best_epoch}')
    ax1.legend()

    # Plot 2: Training & Validation Accuracy
    ax2.plot(range(1, epochs + 1), training_history['accuracy'], 'b-', linewidth=2, label='Training Accuracy')
    ax2.plot(range(1, epochs + 1), training_history['val_accuracy'], 'r-', linewidth=2, label='Validation Accuracy')
    ax2.set_title('Training vs Validation Accuracy', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Accuracy', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xticks(range(1, epochs + 1, 2))
    ax2.set_ylim(0.5, 0.9)

    # Highlight final validation accuracy
    final_val_acc = training_history['val_accuracy'][-1]
    ax2.annotate(f'Final Val Acc: {final_val_acc:.3f}',
                 xy=(epochs, final_val_acc),
                 xytext=(epochs - 5, final_val_acc - 0.05),
                 arrowprops=dict(arrowstyle='->', color='red'),
                 fontsize=11, fontweight='bold', color='red')

    # Plot 3: Learning Rate Decay (if applicable)
    # Simulated learning rate schedule
    learning_rates = [1e-3] * 5 + [5e-4] * 5 + [1e-4] * 5 + [5e-5] * 5
    ax3.semilogy(range(1, epochs + 1), learning_rates, 'g-', linewidth=2, marker='o', markersize=4)
    ax3.set_title('Learning Rate Schedule', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Epoch', fontsize=12)
    ax3.set_ylabel('Learning Rate (log scale)', fontsize=12)
    ax3.grid(True, alpha=0.3, which='both')
    ax3.set_xticks(range(1, epochs + 1, 2))

    # Plot 4: Early Stopping Monitoring
    patience = 5
    val_loss = training_history['val_loss']
    min_val_loss = min(val_loss)
    min_epoch = val_loss.index(min_val_loss) + 1

    ax4.plot(range(1, epochs + 1), val_loss, 'purple', linewidth=2, marker='s', markersize=4)
    ax4.axhline(y=min_val_loss + 0.01, color='orange', linestyle='--', alpha=0.5, label='Stopping threshold')
    ax4.axvline(x=min_epoch, color='red', linestyle=':', alpha=0.7, label=f'Min loss at epoch {min_epoch}')

    # Show early stopping region
    if min_epoch + patience <= epochs:
        ax4.axvspan(min_epoch, min_epoch + patience, alpha=0.2, color='yellow', label='Early stopping patience')

    ax4.set_title('Early Stopping Monitoring', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Epoch', fontsize=12)
    ax4.set_ylabel('Validation Loss', fontsize=12)
    ax4.legend()
    ax4.grid(True, alpha=0.3)

    plt.suptitle('Neural Network Training History - Heart Disease Prediction',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'training_history.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("✓ Generated: training_history.png")
    return training_history


# Run the function
if __name__ == "__main__":
    generate_training_history_visualization()