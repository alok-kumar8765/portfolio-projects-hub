import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Crop Disease Detector", page_icon="🌿", layout="centered")

st.title("🌿 Agricultural Crop Disease Detection System")
st.markdown("Upload a crop leaf image to detect diseases, analyze severity, and get immediate organic treatment recommendations.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Leaf Sample", use_container_width=True)
    
    if st.button("Run Disease Detection", type="primary"):
        with st.spinner("Analyzing leaf patterns via backend API..."):
            try:
                # Prepare image bytes for FastAPI multi-part form upload
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format if image.format else 'JPEG')
                img_byte_arr.seek(0)
                
                files = {"file": ("leaf.jpg", img_byte_arr, "image/jpeg")}
                
                # Send POST request to FastAPI backend
                response = requests.post("http://127.0.0.1:8000/predict", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Analysis Complete!")
                    
                    # Metrics display
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Detected Condition", value=data["prediction"])
                    with col2:
                        st.metric(label="Confidence Score", value=f"{data['confidence']}%")
                        
                    # Actionable Treatment Details
                    details = data.get("details", {})
                    st.markdown("---")
                    st.subheader("📋 Field Advisory & Treatment Plan")
                    st.warning(f"**Severity Level:** {details.get('severity')}")
                    st.markdown(f"**Organic Remedy:** {details.get('organic_remedy')}")
                    st.markdown(f"**Prevention Strategy:** {details.get('prevention')}")
                else:
                    st.error(f"Server Error: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Connection failed! Make sure your FastAPI backend (`python main.py`) is running in another terminal window.")