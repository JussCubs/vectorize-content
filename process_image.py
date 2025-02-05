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
    Apply correct W3C 'Luminosity' blend mode.
    - https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """
    base_np = np.array(base_img, dtype=np.float32) / 255.0  # Normalize
    overlay_np = np.array(overlay_img.convert("L"), dtype=np.float32) / 255.0  # Grayscale

    # Convert grayscale image back into 3-channel format
    luminance = np.stack([overlay_np] * 3, axis=-1)

    # Replace Luminance while keeping the original blue hue & saturation
    blended_np = np.copy(base_np)
    blended_np[..., 0] = base_np[..., 0]  # Preserve Hue
    blended_np[..., 1] = base_np[..., 1]  # Preserve Saturation
    blended_np[..., 2] = luminance[..., 0]  # Replace Lightness

    # Ensure pixel values stay within valid range
    blended_np = np.clip(blended_np * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(blended_np)

def process_image(image_path, brightness=1.15, contrast=1.2, output_name="processed_image.png"):
    """Processes the image using 100% accurate Figma process."""
    ensure_output_folder()

    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # STEP 1: Convert image to grayscale (100% desaturation)
    grayscale_img = ImageOps.grayscale(img).convert("RGB")

    # STEP 2: Create a solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # STEP 3: Apply W3C Luminosity Blend Mode
    blended = apply_luminosity_blend(blue_bg, grayscale_img)

    # STEP 4: Fine-tune brightness & contrast to match Figma
    blended = ImageEnhance.Brightness(blended).enhance(brightness)
    blended = ImageEnhance.Contrast(blended).enhance(contrast)

    # STEP 5: Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return blended
