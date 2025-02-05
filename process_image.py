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

def process_image(image_path, output_name="processed_image.png"):
    """Processes the image exactly like Figma, ensuring the blue square is placed properly."""
    ensure_output_folder()

    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # STEP 1: Create the blue square (Background)
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # STEP 2: Paste the Meme (Overlay Image)
    grayscale_img = ImageOps.grayscale(img).convert("RGB")  # Convert to Grayscale

    # STEP 3: Resize the blue square to match the image dimensions
    blue_bg = blue_bg.resize((width, height))

    # STEP 4: Apply W3C Luminosity Blend Mode
    blended = Image.blend(blue_bg, grayscale_img, alpha=1.0)  # Full Luminosity effect

    # STEP 5: Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return output_path
