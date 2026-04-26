# 🧠 CNN Image Classifier — CIFAR-10

## 📝 Overview
A production-quality Deep Learning project demonstrating Convolutional Neural Networks (CNNs) for image classification. Trains a robust model to recognize 10 object categories from the CIFAR-10 dataset. Target accuracy: **80%+** with a clean, leakage-free training pipeline.

## 🛠️ Tech Stack
| Tool | Purpose |
|---|---|
| TensorFlow / Keras | Model building & training |
| NumPy | Numerical operations |
| Matplotlib | Training curves & confusion matrix |
| Scikit-learn | Classification metrics |
| Pillow | Image loading for inference |

## 🗂️ Project Structure
```text
cnn_image_classifier/
│
├── data/                   # Raw & processed datasets (git-ignored)
├── notebooks/
│   └── CNN_CIFAR10.ipynb   # Self-contained Google Colab notebook
├── src/
│   ├── config.py           # ⭐ Single source of truth: classes, paths, hyperparams
│   ├── data_loader.py      # Loads CIFAR-10 with proper train/val/test split + augmentation
│   ├── model.py            # CNN architecture (3 conv blocks + proportional dense head)
│   ├── train.py            # Training loop with aligned callbacks & ReduceLROnPlateau
│   ├── evaluate.py         # Accuracy, classification report, confusion matrix heatmap
│   └── predict.py          # Single-image inference (top-3 predictions with confidence)
├── models/
│   └── final_model/        # Saved best model (cifar10_cnn_model.keras)
├── outputs/
│   ├── plots/              # accuracy.png, loss.png, confusion_matrix.png
│   └── results/            # evaluation_report.txt
├── requirements.txt
├── README.md
└── .gitignore
```

## ✅ Training Pipeline — What's Fixed

| Issue | Old Behaviour | Fixed Behaviour |
|---|---|---|
| **Data Leakage** | `validation_data=(x_test, y_test)` in `model.fit()` | Proper `(x_val, y_val)` split carved from training set |
| **Callback Conflict** | EarlyStopping→`val_loss`, ModelCheckpoint→`val_accuracy` | All callbacks monitor `val_accuracy` |
| **Dense Bottleneck** | `Flatten(2048) → Dense(128)` — 16× compression | `Dense(512) → Dense(256)` — proportional reduction |
| **Epoch Cap** | Hard `epochs=20`, `patience=5` cuts off augmented training | `epochs=75`, `patience=10` — EarlyStopping decides |
| **No Augmentation** | Normalize only — severe overfitting | Horizontal flip, shift, zoom (~+6% test accuracy) |
| **No LR Decay** | Fixed Adam learning rate | `ReduceLROnPlateau` decays on stagnation |
| **CLASSES scattered** | Redefined in `evaluate.py` only | Centralized in `config.py`, imported everywhere |

## 📊 Expected Output
- **Test Accuracy:** ~80–85% (GPU) / ~75–78% (CPU, fewer epochs via EarlyStopping)
- **Outputs generated:**
  - `outputs/plots/accuracy.png` — Training vs. validation accuracy curve
  - `outputs/plots/loss.png` — Training vs. validation loss curve
  - `outputs/plots/confusion_matrix.png` — Labeled heatmap
  - `outputs/results/evaluation_report.txt` — Full classification report

## 🚀 How to Run

### Prerequisites
```bash
cd cnn_image_classifier
pip install -r requirements.txt
```

### Option A: Local — Step by Step
```bash
# 1. Train the model (creates best checkpoint in models/final_model/)
python src/train.py

# 2. Evaluate on the untouched test set (generates plots + report)
python src/evaluate.py

# 3. Run inference on any image
python src/predict.py path/to/your/image.jpg
```

### Option B: Google Colab (GPU Recommended)
1. Upload the `cnn_image_classifier/` folder to **Google Drive**.
2. Open `notebooks/CNN_CIFAR10.ipynb` from [Google Colab](https://colab.research.google.com/).
3. Enable GPU: **Runtime → Change runtime type → GPU**.
4. Update `PROJECT_PATH` in Cell 1 and run all cells.

## 📈 Model Architecture
```
Input (32×32×3)
  → Conv2D(32) × 2 + BN + MaxPool + Dropout(0.25)   [Block 1]
  → Conv2D(64) × 2 + BN + MaxPool + Dropout(0.35)   [Block 2]
  → Conv2D(128) × 2 + BN + MaxPool + Dropout(0.45)  [Block 3]
  → Flatten → Dense(512) + BN + Dropout(0.5)
            → Dense(256) + BN + Dropout(0.4)
            → Dense(10, softmax)
```

## 🔮 Single Image Inference
```bash
python src/predict.py my_photo.jpg
```
```
Image: my_photo.jpg
────────────────────────────────────────
  #1  cat           72.31%
  #2  dog           15.44%
  #3  deer           8.12%
────────────────────────────────────────
  Prediction: CAT
```
