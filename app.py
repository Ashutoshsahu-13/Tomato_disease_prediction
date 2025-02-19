import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import warnings
warnings.filterwarnings("ignore")
st.set_page_config(
    page_title="Tomato Leaf Disease Prediction",
    page_icon="🍅",
    initial_sidebar_state="auto",
    layout='wide'
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Load Model Fhide_streamlit_style,irst
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('model.h5')

with st.spinner('Model is being loaded...'):
    model = load_model()
# Define Class Labels
index_to_class = {
    0: "Tomato_Bacterial_spot",
    1: "Tomato_Early_blight",
    2: "Tomato_Late_blight",
    3: "Tomato_Leaf_Mold",
    4: "Tomato_Septoria_leaf_spot",
    5: "Tomato_Spider_mites_Two_spotted_spider_mite",
    6: "Tomato__Target_Spot",
    7: "Tomato__Tomato_YellowLeaf__Curl_Virus",
    8: "Tomato__Tomato_mosaic_virus",
    9: "Tomato_healthy"
}

# Sidebar Content
with st.sidebar:
    st.image("image/tomato.png",width=200)  # Provide a valid image file path
    st.title('Tomato Disease Detector')
    
st.write("# Tomato Leaf Disease Prediction")
file = st.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg'])

def predict_image(image, model):
    image = image.convert("RGB")  # Ensure it is in RGB format
    image = image.resize((224, 224))  # Resize to match model input
    img_array = np.asarray(image) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction, axis=-1)[0]
    return index_to_class.get(predicted_class, "Unknown")

if file is None:
    st.text('Please upload an image file.')
   
else:
    image = Image.open(file)
    #image=image.resize((200,200))
    st.image(image, width=300)
    
    prediction = predict_image(image, model)
    st.sidebar.success(f"Detected Disease: {prediction}")
    
    # Display Remedy Information
    remedies = {
        "Tomato_Bacterial_spot": "Prevent bacterial spot by using disease-free seeds.",
        "Tomato_Early_blight": "Prevent early blight by practicing good garden hygiene.",
        "Tomato_Late_blight": "Prevent late blight by ensuring good air circulation.",
        "Tomato_Leaf_Mold": "Prevent leaf mold by spacing plants and improving air circulation.",
        "Tomato_Septoria_leaf_spot": "Prevent Septoria leaf spot by maintaining good garden hygiene.",
        "Tomato_Spider_mites_Two_spotted_spider_mite": "Check plants regularly for mite infestations.",
        "Tomato__Target_Spot": "Ensure proper plant spacing to prevent target spot.",
        "Tomato__Tomato_YellowLeaf__Curl_Virus": "Use virus-free tomato plants to prevent TYLCV.",
        "Tomato__Tomato_mosaic_virus": "Use disease-resistant seeds to prevent tomato mosaic virus.",
        "Tomato_healthy": "Your plant is healthy! Keep up the good care."
    }
    
    st.markdown("## Remedy")
    st.info(remedies.get(prediction, "No specific remedy available."))