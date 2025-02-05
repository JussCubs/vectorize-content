import streamlit as st
import os
from process_image import process_image

st.set_page_config(page_title="🔵 Vectorizer - Figma Luminosity", layout="centered")

st.title("🔵 Vectorizer - Figma Luminosity Blend")
st.write("Upload an image and tweak settings until it's **exactly** like Figma!")

# User-adjustable parameters
brightness = st.slider("Brightness Boost", 1.0, 3.0, 2.2, 0.1)  # More brightness control
contrast = st.slider("Contrast Adjustment", 0.8, 1.5, 1.0, 0.1)  # Lower contrast to avoid darkness
saturation = st.slider("Saturation (0 = grayscale, 1 = normal, 2+ = oversaturated)", 0.0, 2.5, 1.0, 0.1)
blue_boost = st.slider("Blue Boost Intensity", 2.0, 5.0, 4.0, 0.1)  # Blue correction factor
blend_alpha = st.slider("Blend Alpha (Lower = more white, Higher = more blue)", 0.3, 0.7, 0.4, 0.05)

uploaded_file = st.file_uploader("🔥 PICK A MEME, MFER... 🔥", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save uploaded image
    file_path = os.path.join("output", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process Image with user settings
    output_path = process_image(
        file_path, brightness, contrast, saturation, blend_alpha, output_name=f"vectorized_{uploaded_file.name}"
    )

    # Show Processed Image
    st.image(output_path, caption="🔵 Your Meme, but BLUE 🔵", use_container_width=True)

    # Provide Browser Download
    with open(output_path, "rb") as f:
        st.download_button(
            label="🚀 DOWNLOAD YOUR VECTORIZED MEME 🚀",
            data=f,
            file_name=f"vectorized_{uploaded_file.name}",
            mime="image/png"
        )

st.markdown("---")
st.write("⚡ Created by CUBS")
