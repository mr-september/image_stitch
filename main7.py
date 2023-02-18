
# pip install Pillow
import os
from PIL import Image

input_dir = 'G:/OneDrive/Archive/Flight Network Dispute/final live chat'
output_dir = 'G:/OneDrive/Archive/Flight Network Dispute/final live chat/equal size'
padding_color = (0, 0, 0)  # white padding

# get list of image files in input directory
image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')]

# find highest x and y dimensions
max_x, max_y = 0, 0
for img_file in image_files:
    with Image.open(img_file) as img:
        x, y = img.size
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

# create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# add padding to images and save to output directory
for img_file in image_files:
    with Image.open(img_file) as img:
        x, y = img.size
        new_img = Image.new(mode='RGB', size=(max_x, max_y), color=padding_color)
        new_img.paste(img, box=(0, 0, x, y))
        output_file = os.path.join(output_dir, os.path.basename(img_file))
        new_img.save(output_file)