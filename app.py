import streamlit as st
import os
from process_image import process_image, get_downloads_folder

st.set_page_config(page_title="🔵 Vectorizer Tool", layout="centered")

st.title("🔵 Vectorizer Branding Tool")
st.write("Upload an image to apply the blue branding process.")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save uploaded image temporarily
    file_path = os.path.join(get_downloads_folder(), uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process Image
    output_path = process_image(file_path, output_name=f"vectorized_{uploaded_file.name}")

    # Show Results
    st.image(output_path, caption="Processed Image", use_column_width=True)

    st.success(f"✅ Image saved to Downloads: {output_path}")