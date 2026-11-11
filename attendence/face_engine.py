import numpy as np
import cv2
import base64

# Use InsightFace or face_recognition library for embeddings
# Example helper to decode base64 frame from frontend client camera:

def decode_base64_image(image_data_str: str):
    """Decodes base64 string sent from client browser."""
    if "," in image_data_str:
        image_data_str = image_data_str.split(",")[1]
    image_bytes = base64.b64decode(image_data_str)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return frame

def extract_face_embedding(frame):
    """
    Extract facial embeddings.
    In production, pass frame into ArcFace/InsightFace network.
    Returns: (bounding_box, 512_d_embedding_vector)
    """
    # Placeholder for InsightFace inference
    # app = InsightFaceApp(name='buffalov_l')
    # faces = app.get(frame)
    # return faces[0].embedding if faces else None
    pass