import streamlit as st
import os
from process_image import process_image

st.set_page_config(page_title="🔵 Vectorizer - Figma Luminosity", layout="centered")

st.title("🔵 Vectorizer - Figma Luminosity Blend")
st.write("Upload an image and tweak settings until it's **exactly** like Figma!")

# User-adjustable parameters
brightness = st.slider("Brightness Boost", 0.5, 3.0, 1.2, 0.1)
contrast = st.slider("Contrast Boost", 0.5, 3.0, 1.5, 0.1)
blend_alpha = st.slider("Blend Alpha (0 = full gray, 1 = full blue)", 0.0, 1.0, 0.65, 0.05)

uploaded_file = st.file_uploader("🔥 PICK A MEME, MFER... 🔥", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Save uploaded image in the output folder
    file_path = os.path.join("output", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process Image with user settings
    output_path = process_image(file_path, brightness, contrast, blend_alpha, output_name=f"vectorized_{uploaded_file.name}")

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
