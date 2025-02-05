from PIL import Image, ImageEnhance
import numpy as np
import cv2
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
    """Applies Figma-style blue branding while preserving white highlights."""
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
    img_gray_np = np.array(img_gray, dtype=np.float32) / 255.0  # Normalize to [0,1]

    # Create solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = np.full((height, width, 3), blue_rgb, dtype=np.float32)  # Solid blue image

    # Expand grayscale to 3-channel format
    img_gray_np = np.stack([img_gray_np] * 3, axis=-1)  # Convert single-channel grayscale to RGB

    # Apply color correction factors
    correction_factors = np.array([1.2, 1.3, blue_boost])  # Boost blue, restore red/green
    img_corrected = img_gray_np * correction_factors
    img_corrected = np.clip(img_corrected, 0, 255)  # Ensure valid RGB values

    # Convert to uint8
    img_corrected = img_corrected.astype(np.uint8)

    # Apply proper blending with `blend_alpha`
    final_img_np = cv2.addWeighted(blue_bg.astype(np.uint8), (1 - blend_alpha), img_corrected, blend_alpha, 0)

    # Convert back to PIL image
    final_img = Image.fromarray(final_img_np)

    # Ensure old output file is removed before saving new one
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    if os.path.exists(output_path):
        os.remove(output_path)

    final_img.save(output_path)

    return output_path  # Return new processed image path
