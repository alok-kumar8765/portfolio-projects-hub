import tensorflow as tf
import numpy as np

def verify_tflite_model(tflite_path="crop_model_quantized.tflite"):
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print("--- TFLite Model Validation ---")
    print("Input Shape:", input_details[0]['shape']) # Should be [1, 224, 224, 3]
    print("Input Type:", input_details[0]['dtype'])  # Usually float32 or int8
    print("Output Shape:", output_details[0]['shape'])
    
    # Test with a dummy image tensor
    dummy_input = np.random.rand(*input_details[0]['shape']).astype(input_details[0]['dtype'])
    interpreter.set_tensor(input_details[0]['index'], dummy_input)
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    print("Inference test passed! Output probabilities shape:", output_data.shape)

if __name__ == "__main__":
    verify_tflite_model()