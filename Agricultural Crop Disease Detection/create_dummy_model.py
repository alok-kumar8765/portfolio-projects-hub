import tensorflow as tf

# Create a MobileNetV2 structure and convert it to a quantized TFLite file
print("Generating model file...")
base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=True, weights=None)
converter = tf.lite.TFLiteConverter.from_keras_model(base_model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open("crop_model_quantized.tflite", "wb") as f:
    f.write(tflite_model)
print("Successfully created crop_model_quantized.tflite!")