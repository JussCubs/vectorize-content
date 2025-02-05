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
    return np.array([int(hex_color[i:i+2], 16) for i in (1, 3, 5)], dtype=np.float32)

def process_image(image_path, brightness=1.6, contrast=1.4, saturation=1.0, blend_alpha=0.75, output_name="processed_image.png"):
    """Corrects the image to match Figma's Luminosity mode using precise adjustments."""
    ensure_output_folder()
    
    # Open and resize image (for performance)
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale (extract luminance)
    img_gray = img.convert("L")

    # Adjust brightness & contrast dynamically
    img_gray = ImageEnhance.Brightness(img_gray).enhance(brightness)
    img_gray = ImageEnhance.Contrast(img_gray).enhance(contrast)

    # Convert grayscale image to NumPy array
    img_gray_np = np.array(img_gray) / 255.0  # Normalize luminance to [0,1]

    # Create a solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)

    # Apply correction factors to match Figma (based on computed values)
    correction_factors = np.array([1.2, 1.3, 3.0])  # Boost blue more, restore red/green

    # Blend grayscale as luminosity while applying color correction
    corrected_rgb = blue_rgb * correction_factors  # Boost blue, restore red/green
    corrected_rgb = np.clip(corrected_rgb, 0, 255)  # Ensure valid RGB values

    # Apply grayscale luminance to the corrected color
    final_img_np = np.zeros((height, width, 3), dtype=np.uint8)
    for c in range(3):
        final_img_np[..., c] = (img_gray_np * corrected_rgb[c]).astype(np.uint8)

    # Convert back to PIL image
    final_img = Image.fromarray(final_img_np)

    # Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    final_img.save(output_path)

    return output_path  # Return the final image path
