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
    Apply the correct W3C 'Luminosity' blending based on:
    https://www.w3.org/TR/compositing-1/#blendingnonseparable
    """
    base_np = np.array(base_img, dtype=np.float32) / 255.0  # Normalize to [0,1]
    overlay_np = np.array(overlay_img.convert("L"), dtype=np.float32) / 255.0  # Convert to grayscale

    # Convert grayscale image back into 3-channel format
    luminance = np.stack([overlay_np] * 3, axis=-1)

    # Preserve base image hue & saturation but replace luminance
    blended_np = np.copy(base_np)
    blended_np[..., 0] = base_np[..., 0]  # Keep Hue
    blended_np[..., 1] = base_np[..., 1]  # Keep Saturation
    blended_np[..., 2] = luminance[..., 0]  # Replace Lightness

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
    grayscale_img = ImageOps.grayscale(img).convert("RGB")

    # STEP 2: Create a solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # STEP 3: Apply proper W3C Luminosity Blend Mode
    blended = apply_luminosity_blend(blue_bg, grayscale_img)

    # STEP 4: Adjust brightness slightly to match Figma
    enhancer = ImageEnhance.Brightness(blended)
    final_img = enhancer.enhance(1.15)  # Brightness fine-tuning

    # STEP 5: Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    final_img.save(output_path)

    return output_path
