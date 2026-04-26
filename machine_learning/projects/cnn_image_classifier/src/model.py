"""
model.py

Defines the CNN architecture for CIFAR-10 classification.

Key fixes vs. original:
  - ACCURACY FIX: Increased Dense bottleneck from 128 → 512 units.
    The Flatten() output after Block 3 is (4*4*128) = 2048 features.
    Compressing 2048 → 128 in a single step (16x reduction) discards
    most discriminative information before the softmax layer.
    512 units is a more appropriate intermediate representation.
  - ACCURACY FIX: Added a second Dense(256) layer to give the classifier
    more capacity to combine spatial features before the output.
"""

from tensorflow.keras import layers, models
from config import INPUT_SHAPE, NUM_CLASSES


def create_model(input_shape=INPUT_SHAPE, num_classes=NUM_CLASSES):
    """
    Creates a CNN for CIFAR-10 classification targeting 80%+ test accuracy.

    Architecture: 3 convolutional blocks (VGG-style double conv) with
    BatchNorm, MaxPooling, and Dropout — followed by two Dense layers
    sized proportionally to the upstream feature dimensionality.
    """
    model = models.Sequential([
        # ── Block 1: 32 filters ──────────────────────────────────────────
        layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # ── Block 2: 64 filters ──────────────────────────────────────────
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.35),

        # ── Block 3: 128 filters ─────────────────────────────────────────
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.45),

        # ── Classifier Head ───────────────────────────────────────────────
        # Flatten output: 4*4*128 = 2048 features
        layers.Flatten(),

        # FIX: 512 units (was 128 — a 16x bottleneck, losing too much info)
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),

        # Added second Dense layer for deeper feature combination
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.4),

        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


if __name__ == "__main__":
    m = create_model()
    m.summary()
