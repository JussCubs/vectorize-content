from PIL import Image, ImageEnhance
import os
from io import BytesIO

BLUE_HEX = "#0100FF"

def hex_to_rgb(hex_color):
    """Convert HEX to RGB tuple."""
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def process_image(image_path):
    """Processes the image to match Figma's blue branding process."""
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale (Desaturation)
    img_gray = img.convert("L").convert("RGB")

    # Create solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # Blend using "luminosity" effect
    blended = Image.blend(blue_bg, img_gray, alpha=1.0)

    # Save to bytes for direct download
    img_bytes = BytesIO()
    blended.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return img_bytes, blended  # Return both for display and download
