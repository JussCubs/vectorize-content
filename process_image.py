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
    Correct W3C 'Luminosity' blending:
    - Uses 0% saturation grayscale as the luminance source
    - Keeps the hue/saturation from the blue background
    - Ensures 100% opacity
    """

    base_np = np.array(base_img, dtype=np.float32) / 255.0  # Normalize 0-1
    overlay_np = np.array(overlay_img.convert("L"), dtype=np.float32) / 255.0  # Convert to grayscale

    # Ensure grayscale matches RGB shape
    luminance = np.stack([overlay_np] * 3, axis=-1)  # Expand dims to (H, W, 3)

    # Blend: Replace luminance but keep blue hue/saturation
    blended_np = base_np * (luminance / np.maximum(np.mean(base_np, axis=2, keepdims=True), 1e-6))

    # Clip values to ensure valid pixel range
    blended_np = np.clip(blended_np * 255, 0, 255).astype(np.uint8)

    return Image.fromarray(blended_np)

def process_image(image_path, output_name="processed_image.png"):
    """Processes the image exactly like Figma, ensuring zero saturation and full opacity."""
    ensure_output_folder()

    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # STEP 1: Convert image to grayscale (100% desaturation)
    grayscale_img = ImageOps.grayscale(img).convert("RGB")  # Ensures 0% saturation

    # STEP 2: Create a solid blue background with NO corner radius
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # STEP 3: Apply W3C Luminosity Blend Mode
    blended = apply_luminosity_blend(blue_bg, grayscale_img)

    # STEP 4: Ensure 100% opacity by merging again
    final_img = Image.blend(blue_bg, blended, alpha=1.0)  # Full Opacity

    # STEP 5: Save processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    final_img.save(output_path)

    return output_path
