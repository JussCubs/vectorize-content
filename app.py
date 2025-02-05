import streamlit as st
import os
from process_image import process_image

st.set_page_config(page_title="🔵 Vectorizer", layout="centered")

st.title("🔵 Vectorizer")
st.write("Drop a meme and let the **blue magic** happen.")

# Sliders for user adjustments
brightness_factor = st.slider("Brightness", 0.5, 2.0, 1.15, 0.01)
contrast_factor = st.slider("Contrast", 0.5, 2.0, 1.2, 0.01)
blend_strength = st.slider("Blend Strength", 0.0, 1.0, 1.0, 0.01)

uploaded_file = st.file_uploader("PICK A MEME, MFER... ", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save uploaded image temporarily
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process Image with user adjustments
    processed_image = process_image(file_path, brightness_factor, contrast_factor, blend_strength)

    # Convert to Bytes for Download
    from io import BytesIO
    img_bytes = BytesIO()
    processed_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # Display Processed Image
    st.image(processed_image, caption="🔵 Your Meme, but BLUE 🔵", use_container_width=True)

    # Provide Browser Download
    st.download_button(
        label="DOWNLOAD YOUR VECTORIZED MEME 🚀",
        data=img_bytes,
        file_name=f"vectorized_{uploaded_file.name}",
        mime="image/png"
    )

    # Cleanup temp file
    os.remove(file_path)
