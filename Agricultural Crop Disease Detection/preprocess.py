import cv2
import numpy as np

def preprocess_leaf_image(image_path, target_size=(224, 224)):
    """
    Reads an image, removes background noise using color masking (HSV),
    resizes to target dimensions, and normalizes pixel values.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(True, f"Image at {image_path} could not be loaded.")

    # Convert to HSV for green background enhancement (leaf isolation)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Masking green leaf region to filter out background soil/sky noise
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(img, img, mask=mask)
    
    # If green masking is too aggressive (non-green diseased parts), fall back to original image
    processed_img = res if cv2.countNonZero(mask) > (img.shape[0] * img.shape[1] * 0.1) else img

    # Resize to standard MobileNet input shape
    resized = cv2.resize(processed_img, target_size)
    normalized = resized.astype(np.float32) / 255.0
    
    return np.expand_dims(normalized, axis=0)