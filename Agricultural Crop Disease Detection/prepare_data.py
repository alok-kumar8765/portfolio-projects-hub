import os
import shutil
import random

# Path where you cloned the repository
SOURCE_DIR = "PlantVillage-Dataset/raw/color"  # Adjust if your folder path differs
OUTPUT_DIR = "dataset_directory"

TRAIN_DIR = os.path.join(OUTPUT_DIR, "train")
VAL_DIR = os.path.join(OUTPUT_DIR, "validation")

SPLIT_RATIO = 0.8  # 80% train, 20% validation

if not os.path.exists(SOURCE_DIR):
    print(f"Error: Source directory {SOURCE_DIR} not found. Check your folder path.")
    exit()

os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VAL_DIR, exist_ok=True)

classes = os.listdir(SOURCE_DIR)

for cls in classes:
    cls_path = os.path.join(SOURCE_DIR, cls)
    if not os.path.isdir(cls_path):
        continue
        
    images = os.listdir(cls_path)
    random.shuffle(images)
    
    split_index = int(len(images) * SPLIT_RATIO)
    train_images = images[:split_index]
    val_images = images[split_index:]
    
    os.makedirs(os.path.join(TRAIN_DIR, cls), exist_ok=True)
    os.makedirs(os.path.join(VAL_DIR, cls), exist_ok=True)
    
    for img in train_images:
        shutil.copy(os.path.join(cls_path, img), os.path.join(TRAIN_DIR, cls, img))
        
    for img in val_images:
        shutil.copy(os.path.join(cls_path, img), os.path.join(VAL_DIR, cls, img))

print("Dataset successfully split into train and validation folders!")