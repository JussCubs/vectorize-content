import streamlit as st
import os
from process_image import process_image

st.set_page_config(page_title="🔵 Vectorizer", layout="centered")

st.title("🔵 Vectorizer")
st.write("DROP MEME FOR **BLUE MAGIC**.")

uploaded_file = st.file_uploader("PICK A MEME, MFER... ", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save uploaded image temporarily
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process Image (Fix: Unpack tuple)
    img_bytes, processed_image = process_image(file_path)

    # Display Processed Image
    st.image(processed_image, caption="🔵 Your Meme, but BLUE 🔵", use_column_width=True)

    # Provide Browser Download
    st.download_button(
        label="DOWNLOAD YOUR VECTORIZED MEME 🚀",
        data=img_bytes,
        file_name=f"vectorized_{uploaded_file.name}",
        mime="image/png"
    )

    # Cleanup temp file
    os.remove(file_path)
