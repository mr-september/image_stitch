import os
from PIL import Image

def add_blank_pixels(input_folder, output_folder):
    # Check output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all images in the input folder
    images = [img for img in os.listdir(input_folder) if img.endswith(".jpg") or img.endswith(".png")]
    
    # Find the widest image
    max_width = 0
    for image in images:
        img = Image.open(os.path.join(input_folder, image))
        width, _ = img.size
        max_width = max(width, max_width)
    
    # Add blank pixels to the right column of all less wide images
    for image in images:
        img = Image.open(os.path.join(input_folder, image))
        width, height = img.size
        if width < max_width:
            blank_pixels = Image.new("RGB", (max_width - width, height), (255, 255, 255))
            img = Image.new("RGB", (max_width, height), (255, 255, 255))
            img.paste(blank_pixels, (width, 0))
        img.save(os.path.join(output_folder, image))

input_folder = "G:/OneDrive/Archive/Flight Network Dispute/final live chat"
output_folder = "G:/OneDrive/Archive/Flight Network Dispute/final live chat/equal width"
add_blank_pixels(input_folder, output_folder)