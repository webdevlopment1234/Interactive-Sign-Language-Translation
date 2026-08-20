"""Train a CNN from the archive image train/test folders."""

import os
import json
from pathlib import Path
import numpy as np
import tensorflow as tf
import cv2
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from keras.callbacks import TensorBoard, EarlyStopping, ReduceLROnPlateau
from keras.optimizers import Adam

# --- Paths -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / 'static' / 'archive (3)'
TRAIN_DIR = DATASET_DIR / 'asl_alphabet_train' / 'asl_alphabet_train'
TEST_DIR = DATASET_DIR / 'asl_alphabet_test' / 'asl_alphabet_test'

IMG_SIZE   = 28   # Sign MNIST images are 28x28 pixels
NUM_EPOCHS = 30   # Adjust up for higher accuracy (e.g. 50)
BATCH_SIZE = 64

gpus = tf.config.list_physical_devices('GPU')
if not gpus:
    raise RuntimeError(
        "No GPU detected by TensorFlow!\n"
        "GPU requirement is strictly enforced. Native Windows TensorFlow 2.11+ does not support native GPU.\n"
        "To enable GPU on Windows for your NVIDIA RTX 3050, you must either:\n"
        "1) Use WSL2 (Windows Subsystem for Linux) with nvidia-cuda-toolkit, or\n"
        "2) Install tensorflow==2.10.0 with CUDA 11.2 and cuDNN 8.1."
    )

for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
print('Training on GPU: %s' % ', '.join(device.name for device in gpus))

if not TRAIN_DIR.is_dir() or not TEST_DIR.is_dir():
    raise FileNotFoundError('Archive train/test folders were not found: %s' % DATASET_DIR)

class_names = sorted(path.name for path in TRAIN_DIR.iterdir() if path.is_dir())
label_to_compact = {label: index for index, label in enumerate(class_names)}
num_classes = len(class_names)

def load_images(paths):
    images = []
    labels = []
    for label, path in paths:
        image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError('Unable to read image: %s' % path)
        image = cv2.resize(image, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)
        images.append(image.astype('float32') / 255.0)
        labels.append(label_to_compact[label])
    X = np.asarray(images, dtype='float32').reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y = to_categorical(labels, num_classes=num_classes).astype('float32')
    return X, y

train_paths = [(label, image) for label in class_names for image in sorted((TRAIN_DIR / label).glob('*'))]
test_paths = []
for image in sorted(TEST_DIR.glob('*')):
    label = image.name.removesuffix('_test' + image.suffix)
    if label in label_to_compact:
        test_paths.append((label, image))

print('Loading %d training images and %d test images...' % (len(train_paths), len(test_paths)))
X_train_full, y_train_full = load_images(train_paths)
X_test, y_test = load_images(test_paths)
print('\nDiscovered %d classes: %s' % (num_classes, ', '.join(class_names)))

# Split training set to also create a validation split
X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full,
    test_size=0.1,
    stratify=np.argmax(y_train_full, axis=1),
    random_state=42
)

print("\nDataset splits:")
print("  Train : %d samples" % X_train.shape[0])
print("  Val   : %d samples" % X_val.shape[0])
print("  Test  : %d samples" % X_test.shape[0])

# --- Model architecture ------------------------------------------------------
# CNN sized for 28x28 grayscale archive images.
# Dense layer widths (64 -> 32) kept the same as the existing LSTM model.
model = Sequential([
    # Block 1
    Conv2D(64,  (3, 3), activation='relu', padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    BatchNormalization(),
    Conv2D(64,  (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    # Block 2
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    MaxPooling2D((2, 2)),
    Dropout(0.25),

    # Dense head (same widths as existing LSTM model: 64 -> 32 -> softmax)
    Flatten(),
    Dense(64,  activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(32,  activation='relu'),
    Dense(num_classes, activation='softmax'),
], name='sign_mnist_cnn')

model.compile(
    optimizer=Adam(learning_rate=1e-3),
    loss='categorical_crossentropy',
    metrics=['categorical_accuracy']
)

model.summary()

# --- Callbacks ---------------------------------------------------------------
log_dir     = BASE_DIR / 'Logs' / 'cnn'
tb_callback = TensorBoard(log_dir=log_dir)
early_stop  = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)
reduce_lr   = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)

# --- Train -------------------------------------------------------------------
print("\nStarting training...")
history = model.fit(
    X_train, y_train,
    epochs=NUM_EPOCHS,
    batch_size=BATCH_SIZE,
    validation_data=(X_val, y_val),
    callbacks=[tb_callback, early_stop, reduce_lr]
)

# --- Evaluate on test set ----------------------------------------------------
print("\nEvaluating on held-out test set...")
test_loss, test_acc = model.evaluate(X_test, y_test, verbose=1)
print("Test accuracy: %.2f%%" % (test_acc * 100))

# --- Save model --------------------------------------------------------------
model_json = model.to_json()
with open(BASE_DIR / 'model_cnn.json', 'w') as f:
    f.write(model_json)
model.save(BASE_DIR / 'model_cnn.h5')

# Save the label map so app.py / inference code can resolve predictions
# to characters without any hardcoded list.
# Format: { "compact_index": "character", ... }  (keys are strings for JSON)
labels_map = {str(index): label for label, index in label_to_compact.items()}
with open(BASE_DIR / 'model_cnn_labels.json', 'w') as f:
    json.dump(labels_map, f, indent=2)

print("\nSaved:")
print("  model_cnn.json        -- model architecture")
print("  model_cnn.h5          -- model weights")
print("  model_cnn_labels.json -- class index -> character map (no hardcoded labels)")
print("\nDone.")