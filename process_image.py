from PIL import Image, ImageEnhance
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
    return np.array([int(hex_color[i:i+2], 16) for i in (1, 3, 5)], dtype=np.float32)

def process_image(image_path, brightness=2.5, contrast=0.9, saturation=1.0, blue_boost=4.5, blend_alpha=0.3, output_name="processed_image.png"):
    """Applies Figma-style blue branding while preserving whites."""
    ensure_output_folder()

    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale (extract luminosity)
    img_gray = img.convert("L")

    # Apply brightness & contrast
    img_gray = ImageEnhance.Brightness(img_gray).enhance(brightness)
    img_gray = ImageEnhance.Contrast(img_gray).enhance(contrast)

    # Convert grayscale image to NumPy array
    img_gray_np = np.array(img_gray) / 255.0  # Normalize to [0,1]

    # Create solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)

    # Apply color correction
    correction_factors = np.array([1.2, 1.3, blue_boost])  # Boost blue while keeping red/green visible

    # Apply grayscale as luminosity
    corrected_rgb = blue_rgb * correction_factors
    corrected_rgb = np.clip(corrected_rgb, 0, 255)  # Ensure valid values

    # Apply grayscale intensity to RGB channels
    final_img_np = np.zeros((height, width, 3), dtype=np.uint8)
    for c in range(3):
        final_img_np[..., c] = (img_gray_np * corrected_rgb[c]).astype(np.uint8)

    # Convert back to PIL image
    final_img = Image.fromarray(final_img_np)

    # Ensure old output file is removed before saving new one
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    if os.path.exists(output_path):
        os.remove(output_path)
    
    final_img.save(output_path)

    return output_path  # Return new processed image path
