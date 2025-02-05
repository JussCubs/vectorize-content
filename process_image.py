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
    return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

def process_image(image_path, output_name="processed_image.png"):
    """Applies the exact Figma-style blue branding process."""
    ensure_output_folder()

    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale (Desaturation)
    grayscale_img = img.convert("L").convert("RGB")

    # Apply final brightness boost (+5%) for Figma accuracy
    enhancer = ImageEnhance.Brightness(grayscale_img)
    grayscale_img = enhancer.enhance(1.05)  # Corrected brightness based on math

    enhancer = ImageEnhance.Contrast(grayscale_img)
    grayscale_img = enhancer.enhance(1.6)  # Keep contrast sharp

    # Convert to NumPy for per-channel fine-tuning
    img_np = np.array(grayscale_img, dtype=np.float32)

    # Apply per-channel brightness fix (+5%) and blue boost (+10%)
    img_np[..., 0] *= 1.05  # Red
    img_np[..., 1] *= 1.05  # Green
    img_np[..., 2] *= 1.1   # Blue (now matches Figma)

    # Clip values to ensure they stay in valid image range
    img_np = np.clip(img_np, 0, 255).astype(np.uint8)

    # Convert back to PIL image
    img_gray_adjusted = Image.fromarray(img_np)

    # Create solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # Use "Screen" blending mode with final opacity adjustment
    blended = Image.blend(blue_bg, img_gray_adjusted, alpha=0.62)

    # Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return output_path
