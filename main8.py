# Used after main7.py

from PIL import Image
import os

def calculate_overlap_percentages(input_dir):
    image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')]

    # Load all images and calculate their bounding boxes
    images = []
    bounding_boxes = []
    for image_file in image_files:
        with Image.open(image_file) as img:
            images.append(img)
            bounding_boxes.append(img.getbbox())

    # Calculate pairwise overlap percentages using bounding boxes
    overlap_percentages = []
    for i in range(len(images)):
        for j in range(i+1, len(images)):
            x_overlap = max(0, min(bounding_boxes[i][2], bounding_boxes[j][2]) - max(bounding_boxes[i][0], bounding_boxes[j][0]))
            y_overlap = max(0, min(bounding_boxes[i][3], bounding_boxes[j][3]) - max(bounding_boxes[i][1], bounding_boxes[j][1]))
            intersection = x_overlap * y_overlap
            area_i = (bounding_boxes[i][2] - bounding_boxes[i][0]) * (bounding_boxes[i][3] - bounding_boxes[i][1])
            area_j = (bounding_boxes[j][2] - bounding_boxes[j][0]) * (bounding_boxes[j][3] - bounding_boxes[j][1])
            union = area_i + area_j - intersection
            overlap_percentage = intersection / union
            overlap_percentages.append((image_files[i], image_files[j], overlap_percentage))

    return overlap_percentages

results = calculate_overlap_percentages('G:/OneDrive/Archive/Flight Network Dispute/final live chat/equal size')

print(results)