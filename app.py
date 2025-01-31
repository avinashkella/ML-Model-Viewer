import streamlit as st
import textwrap
import traceback
import tensorflow as tf
from tensorflow.keras import models, layers
from tensorflow.keras.utils import plot_model
import torch
import torch.nn as nn
import torchsummary
import visualkeras
from PIL import Image
import os
from dotenv import load_dotenv
from config import *
from utils import *

load_dotenv()


# Function to visualize Keras model
def visualize_keras_model(model):
    image_path = "keras_visual.png"
    try:
        img = visualkeras.layered_view(model, to_file=image_path, legend=True, spacing=30)
        return image_path
    except Exception as e:
        st.error(f"Error in Keras model visualization: {e}")
        return None
    

# Streamlit App Layout
st.set_page_config(layout="wide")

# Custom CSS to inject
st.markdown("""
<style>
    .stColumn {
        border: 2px solid #010;
        padding: 5px;
    }
    .stHorizontalBlock{
        gap: 0.5rem    
    }
    [data-testid="stColumn"] {
        overflow-x:scroll;
    }
    .stColumn {
        max-height: 700px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "generated_model_code" not in st.session_state:
    st.session_state.generated_model_code = ""  # Stores latest model response



# Create three columns
col1, col2, col3 = st.columns([1, 2, 2])

# 1️⃣ Left Grid (Chatbot)
with col1:
    st.header("🤖 ML Model Generator")

    user_input = st.text_input("Mention your model:", key="user_input")
    if st.button("Send", key="chat_button"):
        if user_input:
            st.session_state.chat_history.clear()
            # Get the response from OpenAI (which should be model code)
            response = generate_code(user_input)
            
            # Append the user input and AI response to chat history
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", response))

            # Store the latest model code for the middle column
            st.session_state.generated_model_code = response

    # Display chat history
    for sender, message in st.session_state.chat_history:
        if sender == "AI":
            st.text_area(f"**{sender}:**", message, height=400)
        else:    
            st.write(f"**{sender}:** {message}")

# 2️⃣ Middle Grid (Code Editor)
with col2:
    st.header("📝 Model Code")

    # Select Model Type (Keras or PyTorch)
    model_type = st.radio("Choose Model Type:", ("Keras", "PyTorch"))

    # Determine the default code: AI-generated or fallback to default template
    default_code = st.session_state.generated_model_code if st.session_state.generated_model_code else (
        DEFAULT_CODE_KERAS if model_type == "Keras" else DEFAULT_CODE_PYTORCH
    )

    # User can modify this code
    user_code = st.text_area("Modify your model code:", default_code, height=400)

    if st.button("Run Model"):
        st.session_state.model = extract_model_from_code(user_code)
        st.session_state.model_type = model_type


# 3️⃣ Right Grid (Model Visualization)
with col3:
    st.header("🔍 Model Visualization")

    if "model" in st.session_state and st.session_state.model is not None:
        model = st.session_state.model
        model_type = st.session_state.model_type

        st.success(f"✅ {model_type} Model Loaded Successfully!")

        # Keras Model Visualization
        if model_type == "Keras":
            st.subheader("🖼️ Model Architecture:")
            image_path = visualize_keras_model(model)
            if image_path and os.path.exists(image_path):
                st.image(Image.open(image_path), caption="Keras Model Architecture")
            
            st.subheader("📜 Model Summary:")
            summary = []
            model.summary(print_fn=lambda x: summary.append(x))
            st.text("\n".join(summary))

        # PyTorch Model Visualization
        elif model_type == "PyTorch":
            st.subheader("📜 PyTorch Model Summary:")
            try:
                st.text(torchsummary.summary(model, input_size=(3, 32, 32), device="cpu"))
            except Exception as e:
                st.error(f"Error in PyTorch model summary: {e}")

            st.subheader("🖼️ Model Layers:")
            for name, module in model.named_children():
                st.write(f"**Layer:** {name}")
                st.write(f"Type: {module.__class__.__name__}")
                st.write("---")
    else:
        st.warning("⚠️ No model available. Run the model to visualize.")
