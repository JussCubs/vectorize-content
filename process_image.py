from PIL import Image
import numpy as np
import cv2
import os

BLUE_HEX = "#0100FF"

def get_downloads_folder():
    """Gets the user's Downloads directory dynamically."""
    home = os.path.expanduser("~")
    return os.path.join(home, "Downloads")

def process_image(image_path, output_name="vectorized_image.png"):
    """Processes the image and saves it in the user's Downloads folder."""
    downloads_folder = get_downloads_folder()
    output_path = os.path.join(downloads_folder, output_name)
    
    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert to grayscale (Desaturate)
    img_gray = img.convert("L")

    # Convert blue hex to RGB
    blue_rgb = tuple(int(BLUE_HEX[i:i+2], 16) for i in (1, 3, 5))

    # Create solid blue background
    blue_bg = Image.new("RGB", (width, height), blue_rgb)

    # Blend images using "luminosity" effect
    img_gray_np = np.array(img_gray)
    blue_np = np.array(blue_bg)
    blended = cv2.addWeighted(blue_np, 1.0, np.stack([img_gray_np]*3, axis=-1), 1.0, 0)

    # Convert back to PIL image
    final_img = Image.fromarray(blended)

    # Save processed image in Downloads
    final_img.save(output_path)

    return output_path