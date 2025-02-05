from PIL import Image, ImageEnhance
import os

BLUE_HEX = "#0100FF"

def process_image(image_path):
    """Processes the image and returns a modified PIL image."""
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert to grayscale (Desaturate)
    img_gray = img.convert("L").convert("RGB")

    # Convert blue hex to RGB
    blue_rgb = tuple(int(BLUE_HEX[i:i+2], 16) for i in (1, 3, 5))

    # Create solid blue background
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # Blend images using 'luminosity' effect
    blended = Image.blend(blue_bg, img_gray, alpha=1.0)

    return blended
