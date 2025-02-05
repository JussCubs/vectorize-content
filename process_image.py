from PIL import Image, ImageEnhance
import numpy as np
import os
import random

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
    Applies W3C 'Luminosity' blending:
    - Keeps the Luminance from the grayscale overlay
    - Keeps the Hue/Saturation from the solid blue background
    """

    base_np = np.array(base_img, dtype=np.float32) / 255.0  # Normalize 0-1
    overlay_np = np.array(overlay_img, dtype=np.float32) / 255.0

    # Convert to HSL color space (to extract luminance)
    def rgb_to_hsl(r, g, b):
        max_c, min_c = max(r, g, b), min(r, g, b)
        l = (max_c + min_c) / 2
        if max_c == min_c:
            return 0, 0, l  # No saturation
        d = max_c - min_c
        s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        return (0, s, l)  # Ignore hue, only use luminance

    def hsl_to_rgb(h, s, l):
        def f(n):
            k = (n + h * 12) % 12
            a = s * min(l, 1 - l)
            return l - a * max(-1, min(k - 3, 9 - k, 1))

        return f(0), f(8), f(4)

    # Apply Luminosity blending per pixel
    result_np = np.zeros_like(base_np)
    for y in range(base_np.shape[0]):
        for x in range(base_np.shape[1]):
            # Get Base Image (Blue)
            base_r, base_g, base_b = base_np[y, x]
            _, base_s, _ = rgb_to_hsl(base_r, base_g, base_b)

            # Get Overlay Image (Grayscale)
            overlay_r, overlay_g, overlay_b = overlay_np[y, x]
            _, _, overlay_l = rgb_to_hsl(overlay_r, overlay_g, overlay_b)

            # Apply Luminosity Blend Mode
            new_r, new_g, new_b = hsl_to_rgb(0, base_s, overlay_l)  # Hue=0 (Keep Blue)

            result_np[y, x] = [new_r, new_g, new_b]

    # Convert back to 8-bit RGB
    result_np = np.clip(result_np * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(result_np)

def process_image(image_path, output_name="processed_image.png"):
    """Processes the image using Figma steps and W3C Luminosity Blend Mode."""
    ensure_output_folder()

    # Open input image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # STEP 1: Create a random blue square & paste it at a random position
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_bg = Image.new("RGB", (width, height), blue_rgb)
    
    # Generate random position for the initial blue square (for effect)
    rand_x = random.randint(0, width // 2)
    rand_y = random.randint(0, height // 2)
    blue_bg.paste(blue_bg.crop((0, 0, width // 2, height // 2)), (rand_x, rand_y))

    # STEP 2: Paste the Meme (Overlay Image)
    grayscale_img = img.convert("L").convert("RGB")  # Convert to Grayscale

    # STEP 3: Resize the blue square to match the image dimensions
    blue_bg = blue_bg.resize((width, height))

    # STEP 4: Apply Luminosity Blend Mode
    blended = apply_luminosity_blend(blue_bg, grayscale_img)

    # STEP 5: Save processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    blended.save(output_path)

    return output_path
