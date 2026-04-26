"""
train.py

Handles the full training loop, callbacks, and output saving.

Key fixes vs. original:
  - BUG FIX: EarlyStopping and ModelCheckpoint now both monitor 'val_accuracy'.
    Previously EarlyStopping monitored 'val_loss' and ModelCheckpoint monitored
    'val_accuracy'. This caused the saved .keras file and the in-memory model
    after fit() to potentially represent DIFFERENT model states.
  - BUG FIX: validation_data now uses (x_val, y_val), a proper held-out slice
    of the training set. It no longer passes (x_test, y_test) to model.fit(),
    which was test-set leakage invalidating all reported metrics.
  - ACCURACY FIX: Epochs raised from 20 → 75. Augmented data converges more
    slowly; a hard 20-epoch cap was cutting training short before EarlyStopping
    (patience=10) could determine a real plateau.
  - ACCURACY FIX: Added ReduceLROnPlateau to decay learning rate on stagnation,
    typically squeezing an extra 1-2% accuracy after the initial plateau.
"""

import os
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from data_loader import load_data, get_augmented_generator
from model import create_model
from config import EPOCHS, PATIENCE, BATCH_SIZE, PATHS


def plot_and_save_history(history, save_dir):
    """Saves accuracy and loss curves to outputs/plots/."""
    os.makedirs(save_dir, exist_ok=True)

    # Accuracy
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['accuracy'],     label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Val Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.savefig(os.path.join(save_dir, 'accuracy.png'), dpi=150)
    plt.close()

    # Loss
    plt.figure(figsize=(8, 6))
    plt.plot(history.history['loss'],     label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend(loc='upper right')
    plt.savefig(os.path.join(save_dir, 'loss.png'), dpi=150)
    plt.close()

    print(f"  Training plots saved to: {save_dir}")


def train():
    """Trains the CNN with a clean val split, augmentation, and fixed callbacks."""

    # 1. Load data — three-way split: train / val / test
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_data()

    # 2. Build model
    print("\nInitializing model...")
    model = create_model()

    # 3. Callbacks — FIX: all three monitor the same metric ('val_accuracy')
    os.makedirs(os.path.dirname(PATHS["model"]), exist_ok=True)

    callbacks = [
        # FIX: was monitoring 'val_loss' — now aligned with ModelCheckpoint
        EarlyStopping(
            monitor='val_accuracy',
            patience=PATIENCE,           # 10 epochs (was 5 — too tight for augmented data)
            restore_best_weights=True,
            verbose=1
        ),
        ModelCheckpoint(
            filepath=PATHS["model"],
            monitor='val_accuracy',      # unchanged — kept consistent
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_accuracy',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        ),
    ]

    # 4. Augmented data generator (training only — val/test are NOT augmented)
    train_generator = get_augmented_generator(x_train, y_train)
    steps_per_epoch = len(x_train) // BATCH_SIZE

    # 5. Train
    print(f"\nStarting training (max {EPOCHS} epochs, early stopping patience={PATIENCE})...")
    history = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=EPOCHS,
        # FIX: was (x_test, y_test) — now a proper held-out validation split
        validation_data=(x_val, y_val),
        callbacks=callbacks,
        verbose=1
    )

    # 6. Save plots
    plot_and_save_history(history, PATHS["plots"])

    # 7. Final sanity check on the untouched test set
    print("\nFinal evaluation on untouched test set:")
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"  Test Accuracy : {test_acc:.4f}")
    print(f"  Test Loss     : {test_loss:.4f}")
    print("\nTraining complete. Best model saved to:", PATHS["model"])


if __name__ == "__main__":
    train()
