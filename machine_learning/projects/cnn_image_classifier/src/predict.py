"""
predict.py

Single-image inference script.

Usage:
    python src/predict.py <path_to_image>

Example:
    python src/predict.py my_cat.jpg

The script loads the saved model, resizes any image to 32x32 (CIFAR-10 input),
normalizes it, and prints the top-3 predicted classes with confidence scores.
"""

import sys
import os
import numpy as np
import tensorflow as tf
from PIL import Image

from config import CLASSES, PATHS, INPUT_SHAPE


def predict(image_path: str):
    """Runs inference on a single image file and prints ranked predictions."""

    # Validate file
    if not os.path.exists(image_path):
        print(f"ERROR: File not found — {image_path}")
        sys.exit(1)

    # Load model
    model_path = PATHS["model"]
    if not os.path.exists(model_path):
        print(f"ERROR: No trained model found at {model_path}. Run train.py first.")
        sys.exit(1)

    print(f"Loading model from: {model_path}")
    model = tf.keras.models.load_model(model_path)

    # Preprocess image — resize to 32x32 and normalize to [0, 1]
    h, w = INPUT_SHAPE[0], INPUT_SHAPE[1]
    img        = Image.open(image_path).convert('RGB').resize((w, h))
    img_array  = np.array(img, dtype='float32') / 255.0
    img_batch  = np.expand_dims(img_array, axis=0)   # shape: (1, 32, 32, 3)

    # Predict
    probs      = model.predict(img_batch, verbose=0)[0]
    top3_idx   = np.argsort(probs)[::-1][:3]

    print(f"\nImage: {image_path}")
    print("─" * 40)
    for rank, idx in enumerate(top3_idx, start=1):
        print(f"  #{rank}  {CLASSES[idx]:<12}  {probs[idx]*100:.2f}%")
    print("─" * 40)
    print(f"  Prediction: {CLASSES[top3_idx[0]].upper()}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/predict.py <path_to_image>")
        sys.exit(1)
    predict(sys.argv[1])
