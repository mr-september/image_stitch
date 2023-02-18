import os
import cv2
import numpy as np

# def equalize_dimensions(img1, img2):
#     rows1, cols1 = img1.shape[:2]
#     rows2, cols2 = img2.shape[:2]
    
#     if rows1 < rows2:
#         img1 = np.pad(img1, ((0, rows2 - rows1), (0, 0)), mode='constant')
#     elif rows2 < rows1:
#         img2 = np.pad(img2, ((0, rows1 - rows2), (0, 0)), mode='constant')
        
#     if cols1 < cols2:
#         img1 = np.pad(img1, ((0, 0), (0, cols2 - cols1)), mode='constant')
#     elif cols2 < cols1:
#         img2 = np.pad(img2, ((0, 0), (0, cols1 - cols2)), mode='constant')
    
#     return img1, img2


def calculate_overlap(img1, img2):
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]
    
    rows = max(rows1, rows2)
    cols = max(cols1, cols2)
    
    if rows1 < rows:
        img1 = np.pad(img1, ((0, rows - rows1), (0, 0)), mode='constant')
    if rows2 < rows:
        img2 = np.pad(img2, ((0, rows - rows2), (0, 0)), mode='constant')
    if cols1 < cols:
        img1 = np.pad(img1, ((0, 0), (0, cols - cols1)), mode='constant')
    if cols2 < cols:
        img2 = np.pad(img2, ((0, 0), (0, cols - cols2)), mode='constant')
    
    intersection = np.logical_and(img1, img2)
    union = np.logical_or(img1, img2)
    overlap = np.sum(intersection) / np.sum(union)
    
    return overlap

def scan_folder_for_images(folder_path):
    images = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".png"):
                file_path = os.path.join(root, file)
                image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                images.append(image)
    return images

def phase_correlation(img1, img2):
    img1 = np.float32(img1)
    img2 = np.float32(img2)

    if img1.shape != img2.shape:
        rows1, cols1 = img1.shape
        rows2, cols2 = img2.shape

        if rows1 > rows2:
            padding = np.zeros((rows1-rows2, cols2), dtype=np.float32)
            img2 = np.vstack((img2, padding))
        elif rows2 > rows1:
            padding = np.zeros((rows2-rows1, cols1), dtype=np.float32)
            img1 = np.vstack((img1, padding))

        if cols1 > cols2:
            padding = np.zeros((rows1, cols1-cols2), dtype=np.float32)
            img2 = np.hstack((img2, padding))
        elif cols2 > cols1:
            padding = np.zeros((rows2, cols2-cols1), dtype=np.float32)
            img1 = np.hstack((img1, padding))

    fft1 = np.fft.fft2(img1)
    fft2 = np.fft.fft2(img2)

    fft_mult = fft1 * fft2
    fft_mult /= np.abs(fft_mult)

    corr = np.fft.ifft2(fft_mult)
    corr = np.abs(corr)

    y, x = np.unravel_index(np.argmax(corr), corr.shape)

    return x, y

def align_images(img1, img2):
    x, y = phase_correlation(img1, img2)
    rows, cols = img2.shape
    M = np.float32([[1, 0, x], [0, 1, y]])
    img2 = cv2.warpAffine(img2, M, (cols, rows))
    return img2

def main(folder_path):
    images = scan_folder_for_images(folder_path)
    overlap_matrix = np.zeros((len(images), len(images)))
    for i in range(len(images)):
        for j in range(i+1, len(images)):
            img1 = images[i]
            img2 = images[j]
            img2 = align_images(img1, img2)
            overlap = calculate_overlap(img1, img2)
            overlap_matrix[i][j] = overlap
            overlap_matrix[j][i] = overlap
    
    print(overlap_matrix)


if __name__ == "__main__":
    folder_path = "G:/OneDrive/Archive/Flight Network Dispute/final live chat"
    main(folder_path)
