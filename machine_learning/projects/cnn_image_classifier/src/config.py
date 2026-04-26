"""
config.py

Single source of truth for class names, paths, and hyperparameters.
All other scripts import from here — never redefine these elsewhere.
"""

import os

# ── CIFAR-10 Class Labels ──────────────────────────────────────────────────────
CLASSES = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]
NUM_CLASSES = len(CLASSES)

# ── Directory Paths ────────────────────────────────────────────────────────────
# Resolves correctly whether you run from /src or the project root.
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(_SRC_DIR, '..'))

PATHS = {
    "model":   os.path.join(BASE_DIR, 'models', 'final_model', 'cifar10_cnn_model.keras'),
    "plots":   os.path.join(BASE_DIR, 'outputs', 'plots'),
    "results": os.path.join(BASE_DIR, 'outputs', 'results'),
}

# ── Training Hyperparameters ───────────────────────────────────────────────────
BATCH_SIZE      = 64
EPOCHS          = 75    # High ceiling — EarlyStopping will halt well before this
PATIENCE        = 10    # Enough runway for augmented data to show real improvement
VAL_SPLIT       = 0.1   # 10% of training set reserved as a clean validation set
INPUT_SHAPE     = (32, 32, 3)
