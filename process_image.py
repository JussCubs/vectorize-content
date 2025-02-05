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

def rgb_to_hsl(r, g, b):
    """Convert RGB to HSL color space."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    l = (max_c + min_c) / 2

    if max_c == min_c:
        h = s = 0  # Achromatic (gray)
    else:
        d = max_c - min_c
        s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        if max_c == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_c == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    return (h * 360, s, l)  # Convert hue to degrees

def hsl_to_rgb(h, s, l):
    """Convert HSL back to RGB."""
    def hue_to_rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p

    h /= 360
    if s == 0:
        r = g = b = l  # Achromatic
    else:
        q = l + s - l * s if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)

    return (int(r * 255), int(g * 255), int(b * 255))

def process_image(image_path, brightness=1.2, contrast=1.5, blend_alpha=0.65, output_name="processed_image.png"):
    """Replicates Figma's Luminosity blend mode with a blue background."""
    ensure_output_folder()
    
    # Open image
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Convert image to grayscale (extract luminance)
    img_gray = img.convert("L")

    # Adjust brightness & contrast dynamically
    img_gray = ImageEnhance.Brightness(img_gray).enhance(brightness)
    img_gray = ImageEnhance.Contrast(img_gray).enhance(contrast)

    # Convert grayscale image to NumPy array
    img_gray_np = np.array(img_gray)

    # Create a solid blue background
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_h, blue_s, _ = rgb_to_hsl(*blue_rgb)  # Extract hue & saturation from blue color

    # Apply the grayscale luminance to the blue hue/saturation
    final_img_np = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            l = img_gray_np[y, x] / 255.0  # Normalize luminance
            final_img_np[y, x] = hsl_to_rgb(blue_h, blue_s, l)

    # Convert back to PIL image
    final_img = Image.fromarray(final_img_np)

    # Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    final_img.save(output_path)

    return output_path  # Return the final image path
