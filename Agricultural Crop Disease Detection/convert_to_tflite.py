import tensorflow as tf

def export_tflite_quantized(keras_model_path, tflite_output_path="crop_model_quantized.tflite"):
    model = tf.keras.models.load_model(keras_model_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Apply post-training INT8 dynamic range quantization
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_model = converter.convert()

    with open(tflite_output_path, "wb") as f:
        f.write(tflite_model)
    print(f"Quantized TFLite model saved to {tflite_output_path}")

if __name__ == "__main__":
    export_tflite_quantized("saved_crop_model.h5")