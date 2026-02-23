import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# =========================
# CONFIG
# =========================
IMG_SIZE = 224
BATCH_SIZE = 16
INITIAL_EPOCHS = 8
FINE_TUNE_EPOCHS = 5

DATASET_PATH = "disease_dataset/tomato/train"

# =========================
# DATA GENERATOR
# =========================
datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# =========================
# BASE MODEL (MobileNetV2)
# =========================
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

# Freeze base model initially
base_model.trainable = False

# =========================
# MODEL BUILDING
# =========================
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    Dense(train_data.num_classes, activation="softmax")
])

# =========================
# COMPILE (PHASE 1)
# =========================
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =========================
# TRAINING (TRANSFER LEARNING)
# =========================
print("🚀 Training MobileNetV2 (frozen base)...")

model.fit(
    train_data,
    validation_data=val_data,
    epochs=INITIAL_EPOCHS
)

# =========================
# FINE-TUNING
# =========================
print("🔓 Fine-tuning last 30 layers of MobileNetV2...")

for layer in base_model.layers[-30:]:
    layer.trainable = True

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=FINE_TUNE_EPOCHS
)

# =========================
# SAVE MODEL
# =========================
model.save("tomato_disease_model.h5")

print("✅ Tomato disease detection model trained & fine-tuned successfully.")
