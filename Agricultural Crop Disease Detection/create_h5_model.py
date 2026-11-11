import tensorflow as tf

base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=True, weights=None)
base_model.save("saved_crop_model.h5")
print("Successfully generated saved_crop_model.h5!")