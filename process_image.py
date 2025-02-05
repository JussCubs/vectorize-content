from PIL import Image, ImageEnhance
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
    """Applies the Figma-style blue branding process."""
    ensure_output_folder()
    
    # Open image and get dimensions
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale (Desaturation)
    img_gray = img.convert("L").convert("RGB")

    # Increase contrast slightly to enhance the effect
    enhancer = ImageEnhance.Contrast(img_gray)
    img_gray = enhancer.enhance(1.5)  # Increase contrast by 1.5x

    # Create solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # Apply "Multiply" blend mode effect
    blended = Image.composite(img_gray, blue_bg, img_gray)

    # Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return output_path  # Return the final image path
