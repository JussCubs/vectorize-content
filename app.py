import streamlit as st
import os
from process_image import process_image

st.set_page_config(page_title="🔵 Vectorizer", layout="centered")

st.title("🔵 Vectorizer")
st.write("UPLOAD AN IMAGE TO VECTORIZE IT BLUE")

uploaded_file = st.file_uploader("CHOOSE A MEME MFER...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save uploaded image temporarily
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Process Image
    processed_image = process_image(file_path)

    # Convert to Bytes for Download
    from io import BytesIO
    img_bytes = BytesIO()
    processed_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # Display Processed Image
    st.image(processed_image, caption="Processed Image", use_column_width=True)

    # Provide Browser Download
    st.download_button(
        label="⬇ DOWNLOAD THE VECTORIZEDMEME MFER",
        data=img_bytes,
        file_name=f"vectorized_{uploaded_file.name}",
        mime="image/png"
    )

    # Cleanup temp file
    os.remove(file_path)
