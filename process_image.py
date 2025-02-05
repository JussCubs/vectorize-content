import streamlit as st
import os
from process_image import process_image

st.set_page_config(page_title="🔵 Vectorizer", layout="centered")

st.title("🔵 Vectorizer")
st.write("Upload a meme and let the **blue magic** happen.")

uploaded_file = st.file_uploader("🔥 PICK A MEME, MFER... 🔥", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Save uploaded image in the output folder
    file_path = os.path.join("output", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process Image
    output_path = process_image(file_path, output_name=f"vectorized_{uploaded_file.name}")

    # Show Processed Image
    st.image(output_path, caption="🔵 Your Meme, but BLUE 🔵", use_column_width=True)

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
