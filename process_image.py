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

def apply_luminosity_blend(base_img, overlay_img, blend_strength):
    """
    Apply W3C 'Luminosity' blending with adjustable blend strength.
    """
    base_np = np.array(base_img, dtype=np.float32) / 255.0
    overlay_np = np.array(overlay_img.convert("L"), dtype=np.float32) / 255.0

    # Convert grayscale image back into 3-channel format
    luminance = np.stack([overlay_np] * 3, axis=-1)

    # Blend using adjustable strength
    blended_np = (base_np * (1 - blend_strength)) + (luminance * blend_strength)

    # Clip values to ensure valid pixel range
    blended_np = np.clip(blended_np * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(blended_np)

def process_image(image_path, brightness=1.15, contrast=1.2, blend_strength=1.0, output_name="processed_image.png"):
    """Processes the image exactly like Figma with adjustable brightness/contrast/blend."""
    ensure_output_folder()

    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale
    grayscale_img = ImageOps.grayscale(img).convert("RGB")

    # Create a solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # Apply W3C Luminosity Blend Mode
    blended = apply_luminosity_blend(blue_bg, grayscale_img, blend_strength)

    # Apply user-defined brightness & contrast
    blended = ImageEnhance.Brightness(blended).enhance(brightness)
    blended = ImageEnhance.Contrast(blended).enhance(contrast)

    # Save processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return blended
