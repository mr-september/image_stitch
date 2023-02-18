import os
import cv2
import numpy as np

def stitch_screenshots(screenshot_folder, batch_size=1, output_folder=None):
    # Get list of all screenshots in folder
    screenshot_files = [f for f in os.listdir(screenshot_folder) if f.endswith(".png") or f.endswith(".jpg")]
    screenshot_files.sort()
    
    # Check if there are enough screenshots to stitch
    if len(screenshot_files) < 2:
        print("Error: Not enough screenshots to stitch.")
        return False
    
    # Create output folder if it does not exist
    if output_folder is not None and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load all screenshots into a list of arrays
    screenshots = []
    for i, screenshot_file in enumerate(screenshot_files):
        screenshot = cv2.imread(os.path.join(screenshot_folder, screenshot_file))
        screenshots.append(screenshot)
        
    # Stitch screenshots in batches
    batch_count = len(screenshots) // batch_size
    for i in range(batch_count):
        batch_start = i * batch_size
        batch_end = min((i + 1) * batch_size, len(screenshots))
        batch = screenshots[batch_start:batch_end]
        
        # Find the most likely next screenshot to stitch
        most_likely_next_screenshot = None
        overlap_value, _ = calculate_overlap(screenshot1, screenshot2)
        for j in range(batch_start, len(screenshots)):
            overlap = calculate_overlap(batch[-1], screenshots[j])
            if overlap_value > max_overlap:
                max_overlap = overlap_value
                screenshot_to_stitch = screenshot2
        
        # Stitch the most likely next screenshot to the batch
        status, stitched_screenshot = stitch_two_screenshots(batch[-1], most_likely_next_screenshot)
        if status == 0:
            batch.append(most_likely_next_screenshot)
        
        # Save stitched screenshot
        if output_folder is not None:
            output_file = os.path.join(output_folder, "stitched_batch_{}.png".format(i+1))
            cv2.imwrite(output_file, stitched_screenshot)
        
        print("Stitching batch {} of {}...".format(i+1, batch_count))
        
    return True


def stitch_two_screenshots(screenshot1, screenshot2):
    screenshots = [screenshot1, screenshot2]
    
    stitcher = cv2.createStitcher() if cv2.__version__.startswith('4') else cv2.createStitcher_create()
    status, stitched = stitcher.stitch(screenshots)

    if status != 0:
        print("Stitching failed with error code {}".format(status))
        return None

    return stitched


def calculate_overlap(screenshot1, screenshot2):
    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(screenshot1, None)
    kp2, des2 = sift.detectAndCompute(screenshot2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)

    if len(good) > 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        h, w = screenshot1.shape[:2]
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        overlap_x = max(0, -min(dst[:, 0, 0]))
        overlap_y = max(0, -min(dst[:, 0, 1]))
        overlap_w = min(w, w + max(dst[:, 0, 0])) - overlap_x
        overlap_h = min(h, h + max(dst[:, 0, 1])) - overlap_y

        return (overlap_x, overlap_y, overlap_w, overlap_h)

    return None


if stitch_screenshots(screenshot_folder="G:/OneDrive/Archive/Flight Network Dispute/final live chat/equal width", batch_size=5, output_folder="G:/OneDrive/Archive/Flight Network Dispute/final live chat/equal width/stitched.jpg"):
    print("Stitching successful")
else:
    print("Stitching failed")
