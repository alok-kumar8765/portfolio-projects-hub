from fastapi import FastAPI, File, UploadFile, HTTPException
import tensorflow as tf
import numpy as np
import cv2

app = FastAPI(title="Crop Disease Detection API", version="1.0")

# Load model safely on startup
MODEL_PATH = "saved_crop_model.h5"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    print(f"Warning: Model could not be loaded: {e}")
    model = None

LABELS = [
    "Tomato___Late_blight",
    "Tomato___Healthy",
    "Potato___Early_blight"
]

TREATMENT_DB = {
    "Tomato___Late_blight": {
        "crop": "Tomato",
        "disease": "Late Blight",
        "severity": "High",
        "organic_remedy": "Remove infected leaves immediately. Spray copper-based fungicide or neem oil.",
        "prevention": "Ensure good air circulation and avoid overhead watering."
    },
    "Tomato___Healthy": {
        "crop": "Tomato",
        "disease": "None",
        "severity": "None",
        "organic_remedy": "Crop looks healthy. Continue standard maintenance.",
        "prevention": "Maintain regular monitoring."
    },
    "Potato___Early_blight": {
        "crop": "Potato",
        "disease": "Early Blight",
        "severity": "Medium",
        "organic_remedy": "Apply bio-fungicides containing Bacillus subtilis.",
        "prevention": "Rotate crops and use certified disease-free seeds."
    }
}

@app.post("/predict")
async def predict_crop_disease(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded on the server.")
    
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file format.")

        resized = cv2.resize(img, (224, 224))
        normalized = resized.astype(np.float32) / 255.0
        input_data = np.expand_dims(normalized, axis=0)

        predictions = model.predict(input_data)
        predicted_index = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]))
        
        label_key = LABELS[predicted_index] if predicted_index < len(LABELS) else "Unknown"
        treatment_info = TREATMENT_DB.get(label_key, {
            "crop": "Unknown", "disease": label_key, "severity": "Unknown",
            "organic_remedy": "Consult local agricultural extension officer.", "prevention": "N/A"
        })

        return {
            "status": "success",
            "prediction": label_key,
            "confidence": round(confidence * 100, 2),
            "details": treatment_info
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))