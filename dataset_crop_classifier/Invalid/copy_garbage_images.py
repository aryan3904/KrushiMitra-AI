import os
import random
import shutil

# 🔁 UPDATE THIS PATH TO YOUR Roboflow 'train' folder
SOURCE_DIR = "D:/garbage/train"

# 🔁 UPDATE THIS PATH TO your final dataset folder
DEST_DIR = "D:/civicindia/civicnow-dataset/garbage"

NUM_IMAGES = 600  # You can change this as needed

os.makedirs(DEST_DIR, exist_ok=True)

images = [img for img in os.listdir(SOURCE_DIR) if img.lower().endswith((".jpg", ".png"))]
selected = random.sample(images, NUM_IMAGES)

for img in selected:
    shutil.copy(os.path.join(SOURCE_DIR, img), os.path.join(DEST_DIR, img))

print(f"✅ Copied {NUM_IMAGES} images to: {DEST_DIR}")
