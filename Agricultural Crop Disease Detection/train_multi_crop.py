import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Point directly to your pre-split folders
TRAIN_DIR = "PlantVillage-Dataset/data_distribution_for_SVM/train"
VAL_DIR = "PlantVillage-Dataset/data_distribution_for_SVM/test"

# Data augmentation for real field variations
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Save class mapping so the API knows the label names
class_indices = train_generator.class_indices
inverse_map = {v: k for k, v in class_indices.items()}
with open("class_indices.json", "w") as f:
    json.dump(inverse_map, f)

# Build EfficientNetB0 Backbone
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = True

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(len(class_indices), activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer=tf.keras.optimizers.Adam(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10
)

# Save as .h5 for backend integration
model.save("saved_crop_model.h5")
print("Model training complete and saved as saved_crop_model.h5!")