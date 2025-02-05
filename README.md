# 🔵 Vectorizer - Meme Branding Tool  

This **Streamlit app** allows you to **upload an image** and applies the **Figma-style blue branding process** automatically. It adds a **blue background (`#0100FF`)**, **grayscales the image**, and **blends them together** to match the marketing branding standard. 🚀  

---

## 📂 Folder Structure
```
vectorizer_tool/
│── app.py             # Streamlit UI
│── process_image.py   # Image processing logic
│── requirements.txt   # Dependencies
│── output/            # Folder to store processed images
```

---

## 🛠 Installation & Setup
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/vectorizer-tool.git
cd vectorizer-tool
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Run the App
```sh
streamlit run app.py
```

---

## 🎨 How It Works
1. **Upload an image** (PNG/JPG/JPEG).  
2. The app **desaturates** it (grayscale).  
3. A **blue background (#0100FF)** is applied.  
4. The image and blue layer are **blended (luminosity effect)**.  
5. The final **vectorized image is displayed** and available for **download**.  

---

## 📜 Example Usage
- **Marketing memes with consistent branding** 🔵  
- **Social media graphics** 🖼️  
- **Custom blue-tinted content** 🎨  

---

## 📝 Dependencies
```txt
streamlit
pillow
```

Install via:
```sh
pip install -r requirements.txt
```

---

## 📜 `app.py`
```python
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
```

---

## 📜 `process_image.py`
```python
from PIL import Image, ImageEnhance
import os

OUTPUT_FOLDER = "output"
BLUE_HEX = "#0100FF"

def ensure_output_folder():
    """Ensure the output folder exists."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

def hex_to_rgb(hex_color):
    """Convert HEX color to RGB tuple."""
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def process_image(image_path, output_name="processed_image.png"):
    """Applies the Figma-style blue branding process correctly."""
    ensure_output_folder()
    
    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale (Desaturation)
    img_gray = img.convert("L").convert("RGB")

    # Create solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # Blend images using proper opacity (Figma-like Luminosity effect)
    blended = Image.blend(blue_bg, img_gray, alpha=0.65)  # Adjusted for best visibility

    # Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return output_path  # Return the final image path
```

---

## 🚀 Future Improvements
- Add support for **batch processing** 📂  
- Allow **custom branding colors** 🎨  
- Optimize **image processing speed** ⏩  

---

## 🏆 Credits
⚡ Created by **CUBS**  

🔥 **Enjoy vectorizing your memes!** 🚀
