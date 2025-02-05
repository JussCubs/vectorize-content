import streamlit as st
import os
from process_image import process_image

st.set_page_config(page_title="🔵 Vectorizer - Figma Luminosity", layout="centered")

st.title("🔵 Vectorizer - Figma Luminosity Blend")
st.write("Upload an image and tweak settings to match Figma **EXACTLY**!")

# Force-clear Streamlit cache every time to ensure updates
st.cache_resource.clear()
st.cache_data.clear()

# User-adjustable parameters
brightness = st.slider("Brightness Boost", 1.0, 3.0, 2.5, 0.1)
contrast = st.slider("Contrast Adjustment", 0.8, 1.5, 0.9, 0.1)
saturation = st.slider("Saturation (0 = grayscale, 1 = normal, 2+ = oversaturated)", 0.0, 2.5, 1.0, 0.1)
blue_boost = st.slider("Blue Boost Intensity", 2.0, 5.0, 4.5, 0.1)
blend_alpha = st.slider("Blend Alpha (Lower = more white, Higher = more blue)", 0.3, 0.7, 0.3, 0.05)

uploaded_file = st.file_uploader("🔥 PICK A MEME, MFER... 🔥", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save uploaded image
    file_path = os.path.join("output", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Debugging: Log settings to ensure they update
    st.write(f"🔍 **Processing Image with:** Brightness={brightness}, Contrast={contrast}, Blue Boost={blue_boost}, Blend Alpha={blend_alpha}")

    # Process Image with user settings
    output_path = process_image(
        file_path, brightness, contrast, saturation, blue_boost, blend_alpha, output_name=f"vectorized_{uploaded_file.name}"
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
