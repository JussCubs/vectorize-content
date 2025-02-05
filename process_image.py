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
    return np.array([int(hex_color[i:i+2], 16) for i in (1, 3, 5)], dtype=np.uint8)

def rgb_to_hsl(rgb):
    """Convert an entire RGB NumPy array to HSL at once."""
    rgb = rgb / 255.0
    max_c = np.max(rgb, axis=-1)
    min_c = np.min(rgb, axis=-1)
    l = (max_c + min_c) / 2

    delta = max_c - min_c
    s = np.where(l > 0.5, delta / (2.0 - max_c - min_c), delta / (max_c + min_c))
    s[delta == 0] = 0  # If delta is zero, saturation is zero

    h = np.zeros_like(l)
    mask = (delta != 0)

    # Hue calculations
    mask_r = (max_c == rgb[..., 0]) & mask
    mask_g = (max_c == rgb[..., 1]) & mask
    mask_b = (max_c == rgb[..., 2]) & mask

    h[mask_r] = (rgb[mask_r, 1] - rgb[mask_r, 2]) / delta[mask_r] % 6
    h[mask_g] = (rgb[mask_g, 2] - rgb[mask_g, 0]) / delta[mask_g] + 2
    h[mask_b] = (rgb[mask_b, 0] - rgb[mask_b, 1]) / delta[mask_b] + 4
    h = (h / 6) % 1  # Normalize to [0,1]

    return np.stack([h * 360, s, l], axis=-1)

def hsl_to_rgb(hsl):
    """Convert an entire HSL NumPy array to RGB at once."""
    h, s, l = hsl[..., 0] / 360.0, hsl[..., 1], hsl[..., 2]

    q = np.where(l < 0.5, l * (1 + s), l + s - l * s)
    p = 2 * l - q
    t = np.stack([h + 1/3, h, h - 1/3], axis=-1)
    t = np.where(t < 0, t + 1, t)
    t = np.where(t > 1, t - 1, t)

    def hue_to_rgb(p, q, t):
        return np.where(t < 1/6, p + (q - p) * 6 * t,
                        np.where(t < 1/2, q,
                        np.where(t < 2/3, p + (q - p) * (2/3 - t) * 6, p)))

    rgb = np.stack([hue_to_rgb(p, q, t[..., 0]),
                    hue_to_rgb(p, q, t[..., 1]),
                    hue_to_rgb(p, q, t[..., 2])], axis=-1)

    return (rgb * 255).astype(np.uint8)

def process_image(image_path, brightness=1.2, contrast=1.5, saturation=1.0, blend_alpha=0.65, output_name="processed_image.png"):
    """Replicates Figma's Luminosity blend mode with a blue background (FAST version)."""
    ensure_output_folder()
    
    # Open and resize image (for performance)
    img = Image.open(image_path).convert("RGB")
    img = img.resize((img.width // 2, img.height // 2))  # Resize to 50% to speed up processing

    width, height = img.size

    # Convert image to grayscale (extract luminance)
    img_gray = img.convert("L")

    # Adjust brightness & contrast dynamically
    img_gray = ImageEnhance.Brightness(img_gray).enhance(brightness)
    img_gray = ImageEnhance.Contrast(img_gray).enhance(contrast)

    # Convert grayscale image to NumPy array
    img_gray_np = np.array(img_gray) / 255.0  # Normalize luminance to [0,1]

    # Create a solid blue background (as HSL)
    blue_rgb = hex_to_rgb(BLUE_HEX)
    blue_h, blue_s, _ = rgb_to_hsl(blue_rgb)

    # Apply the grayscale luminance to the blue hue/saturation
    hsl_values = np.full((height, width, 3), [blue_h, blue_s, 0], dtype=np.float32)
    hsl_values[..., 2] = img_gray_np  # Apply grayscale as lightness (L)

    # Convert back to RGB
    final_img_np = hsl_to_rgb(hsl_values)

    # Convert back to PIL image
    final_img = Image.fromarray(final_img_np)

    # Save the processed image
    output_path = os.path.join(OUTPUT_FOLDER, output_name)
    final_img.save(output_path)

    return output_path  # Return the final image path
