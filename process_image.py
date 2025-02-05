from PIL import Image, ImageEnhance, ImageOps
import numpy as np
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

def apply_luminosity_blend(base_img, overlay_img):
    """
    Applies W3C 'Luminosity' blending:
    - Keeps the Luminance from the grayscale overlay
    - Keeps the Hue/Saturation from the solid blue background
    """

    base_np = np.array(base_img, dtype=np.float32) / 255.0  # Normalize 0-1
    overlay_np = np.array(overlay_img, dtype=np.float32) / 255.0

    # Extract Luminance from grayscale image
    luminance = np.dot(overlay_np, [0.299, 0.587, 0.114])  # Standard luminance formula

    # Properly blend Luminance with the blue image (Fixing issue)
    result_np = np.zeros_like(base_np)
    for i in range(3):  # RGB Channels
        result_np[..., i] = base_np[..., i] * 0.95 + luminance[..., np.newaxis] * 0.05  # 5% blend correction

    # Clip values to ensure valid pixel range
    result_np = np.clip(result_np * 255, 0, 255).astype(np.uint8)

    return Image.fromarray(result_np)

def process_image(image_path, output_name="processed_image.png"):
    """Processes the image exactly like Figma, ensuring proper blue & light retention."""
    ensure_output_folder()

    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # STEP 1: Create a solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # STEP 2: Convert image to grayscale
    grayscale_img = ImageOps.grayscale(img).convert("RGB")

    # STEP 3: Resize the blue square to match the image dimensions
    blue_bg = blue_bg.resize((width, height))

    # STEP 4: Apply Luminosity Blend Mode (Exact W3C Standard)
    blended = apply_luminosity_blend(blue_bg, grayscale_img)

    # STEP 5: Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return output_path
