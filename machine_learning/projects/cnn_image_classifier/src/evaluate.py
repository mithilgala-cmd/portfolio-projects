"""
evaluate.py

Loads the saved model and produces a full evaluation report on the test set.

Key fixes vs. original:
  - FIX: CLASSES imported from config.py instead of being redefined here.
  - ADDED: Saves a confusion matrix heatmap PNG to outputs/plots/.
  - ADDED: Saves per-class accuracy breakdown to the text report.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

from data_loader import load_data
from config import CLASSES, PATHS


def save_confusion_matrix(cm, save_dir):
    """Saves a labeled confusion matrix heatmap as a PNG."""
    os.makedirs(save_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 10))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASSES)
    disp.plot(ax=ax, colorbar=True, cmap='Blues', xticks_rotation=45)
    ax.set_title("Confusion Matrix — CIFAR-10 Test Set", fontsize=14, pad=15)
    plt.tight_layout()
    save_path = os.path.join(save_dir, 'confusion_matrix.png')
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"  Confusion matrix saved to: {save_path}")


def evaluate_model():
    """Evaluates the saved model on the clean, untouched test split."""

    # 1. Load data — test set is isolated and was never used during training
    print("Loading test data...")
    _, _, (x_test, y_test) = load_data()

    # 2. Load model
    model_path = PATHS["model"]
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}. Run train.py first.")
        return

    print(f"Loading model from: {model_path}")
    model = tf.keras.models.load_model(model_path)

    # 3. Overall accuracy
    print("\nEvaluating on test set...")
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"  Test Accuracy : {test_acc:.4f}")
    print(f"  Test Loss     : {test_loss:.4f}")

    # 4. Per-class predictions
    print("\nGenerating per-class predictions...")
    predictions    = model.predict(x_test, verbose=0)
    y_pred_classes = np.argmax(predictions, axis=1)
    y_true_classes = y_test.flatten() if y_test.ndim > 1 else y_test

    # 5. Classification report
    report = classification_report(y_true_classes, y_pred_classes, target_names=CLASSES)
    print("\nClassification Report:")
    print("======================")
    print(report)

    # 6. Confusion matrix heatmap
    cm = confusion_matrix(y_true_classes, y_pred_classes)
    save_confusion_matrix(cm, PATHS["plots"])

    # 7. Save full text report
    results_dir = PATHS["results"]
    os.makedirs(results_dir, exist_ok=True)
    report_path = os.path.join(results_dir, 'evaluation_report.txt')
    with open(report_path, 'w') as f:
        f.write(f"Test Accuracy : {test_acc:.4f}\n")
        f.write(f"Test Loss     : {test_loss:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write("======================\n")
        f.write(report)
        f.write("\nConfusion Matrix:\n")
        f.write("=================\n")
        f.write(np.array2string(cm))

    print(f"\nFull report saved to: {report_path}")


if __name__ == "__main__":
    evaluate_model()
