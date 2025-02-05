from PIL import Image, ImageEnhance, ImageChops
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

def process_image(image_path, brightness=1.2, contrast=1.5, saturation=0.0, blend_alpha=0.65, output_name="processed_image.png"):
    """Replicates Figma's Luminosity blend mode with full customization."""
    ensure_output_folder()
    
    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale (FULL desaturation)
    img_gray = img.convert("L")  

    # Apply brightness, contrast, and saturation adjustments
    img_gray = ImageEnhance.Brightness(img_gray).enhance(brightness)
    img_gray = ImageEnhance.Contrast(img_gray).enhance(contrast)

    # Convert grayscale image back to RGB
    img_gray = img_gray.convert("RGB")

    # Adjust saturation (default is full grayscale)
    img_gray = ImageEnhance.Color(img_gray).enhance(saturation)

    # Create solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # Blend using the adjusted grayscale image over the blue background
    blended = Image.blend(blue_bg, img_gray, alpha=blend_alpha)

    # Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return output_path  # Return the final image path
