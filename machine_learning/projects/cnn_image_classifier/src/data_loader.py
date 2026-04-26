"""
data_loader.py

Loads, normalizes, and augments the CIFAR-10 dataset.

Key fixes vs. original:
  - BUG FIX: Returns a proper (x_val, y_val) split carved from x_train so that
    train.py never touches x_test during training. Previously validation_data
    in model.fit() was (x_test, y_test), which is test-set leakage.
  - ACCURACY FIX: Adds a Keras ImageDataGenerator for on-the-fly augmentation
    (horizontal flips, ±10% width/height shifts, ±10% zoom). On CIFAR-10,
    augmentation is typically worth +5–8% final test accuracy.
"""

import numpy as np
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from config import VAL_SPLIT, BATCH_SIZE


def load_data():
    """
    Returns
    -------
    (x_train, y_train) : np.ndarray  — normalized, full training split
    (x_val,   y_val)   : np.ndarray  — 10% of training, held-out validation
    (x_test,  y_test)  : np.ndarray  — untouched test split (never seen during training)
    """
    print("Loading CIFAR-10 dataset...")
    (x_train_full, y_train_full), (x_test, y_test) = cifar10.load_data()

    # Normalize all pixel values to [0, 1]
    x_train_full = x_train_full.astype('float32') / 255.0
    x_test       = x_test.astype('float32')       / 255.0

    # Carve out a clean validation split from training data
    # (FIX: x_test must NOT be used as validation_data in model.fit)
    n_val       = int(len(x_train_full) * VAL_SPLIT)
    x_val       = x_train_full[:n_val]
    y_val       = y_train_full[:n_val]
    x_train     = x_train_full[n_val:]
    y_train     = y_train_full[n_val:]

    print(f"  Train : {x_train.shape[0]} samples")
    print(f"  Val   : {x_val.shape[0]} samples  (held-out from train, never seen by test)")
    print(f"  Test  : {x_test.shape[0]} samples  (untouched)")

    return (x_train, y_train), (x_val, y_val), (x_test, y_test)


def get_augmented_generator(x_train, y_train):
    """
    Returns a Keras ImageDataGenerator fitted on training data.
    Augmentations applied on-the-fly per batch during training.

    Without augmentation: model typically overfits by epoch 10-15 on CIFAR-10.
    With augmentation: effective dataset size is multiplied, reducing overfitting
    and typically improving final test accuracy by 5-8 percentage points.
    """
    datagen = ImageDataGenerator(
        horizontal_flip=True,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
    )
    datagen.fit(x_train)
    return datagen.flow(x_train, y_train, batch_size=BATCH_SIZE)


if __name__ == "__main__":
    (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_data()
    print(f"\nTraining data shape : {x_train.shape}")
    print(f"Validation data shape: {x_val.shape}")
    print(f"Test data shape      : {x_test.shape}")
