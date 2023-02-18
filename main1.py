import cv2
import numpy as np
import os

def detect_overlap(img1, img2):
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append([m])
    if len(good_matches) > 4:
        src_pts = np.float32([kp1[m[0].queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m[0].trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        overlap = cv2.warpPerspective(img1, H, (img1.shape[1] + img2.shape[1], img2.shape[0]))
        overlap[0:img2.shape[0], 0:img2.shape[1]] = img2
        return overlap
    return None

def stitch_images(image_list):
    stitched = image_list[0]
    for i in range(1, len(image_list)):
        overlap = detect_overlap(stitched, image_list[i])
        if overlap is None:
            continue
        height = overlap.shape[0]
        stitched = overlap
    return stitched

def main():
    folder = "G:/OneDrive/Archive/Flight Network Dispute/final live chat"
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg"):
            file_path = os.path.join(folder, filename)
            img = cv2.imread(file_path)
            images.append(img)
    stitched = stitch_images(images)
    cv2.imwrite("stitched.jpg", stitched)

if __name__ == "__main__":
    main()