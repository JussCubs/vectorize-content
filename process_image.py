from PIL import Image
import colorsys
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

def apply_luminosity_blend(base_image, overlay_image):
    """Applies the Figma-style 'Luminosity' blend mode."""
    base_array = np.array(base_image, dtype=np.float32) / 255.0
    overlay_array = np.array(overlay_image, dtype=np.float32) / 255.0

    result_array = np.zeros_like(base_array)

    for y in range(base_array.shape[0]):
        for x in range(base_array.shape[1]):
            # Get base color (blue background)
            base_r, base_g, base_b = base_array[y, x]
            base_h, base_l, base_s = colorsys.rgb_to_hls(base_r, base_g, base_b)

            # Get overlay color (grayscale)
            overlay_r, overlay_g, overlay_b = overlay_array[y, x]
            overlay_h, overlay_l, overlay_s = colorsys.rgb_to_hls(overlay_r, overlay_g, overlay_b)

            # Replace luminance of the base with the overlay
            new_r, new_g, new_b = colorsys.hls_to_rgb(base_h, overlay_l, base_s)

            result_array[y, x] = [new_r, new_g, new_b]

    return Image.fromarray((result_array * 255).astype(np.uint8))

def process_image(image_path, output_name="processed_image.png"):
    """Processes the image using the Figma Luminosity blend mode."""
    ensure_output_folder()

    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale (Desaturation)
    grayscale_img = img.convert("L").convert("RGB")

    # Create solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # Apply correct Figma-style luminosity blend
    blended = apply_luminosity_blend(blue_bg, grayscale_img)

    # Save processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return output_path
