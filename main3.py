import cv2
import os

def stitch_screenshots(screenshot_folder, output_file):
    screenshots = []

    try:
        stitcher = cv2.createStitcher()
    except:
        stitcher = cv2.Stitcher_create()

    for screenshot_file in os.listdir(screenshot_folder):
        screenshot = cv2.imread(os.path.join(screenshot_folder, screenshot_file))
        screenshots.append(screenshot)
    
    (status, stitched) = stitcher.stitch(screenshots)
    
    if status == 0:
        cv2.imwrite(output_file, stitched)
        return True
    else:
        return False

if stitch_screenshots("G:/OneDrive/Archive/Flight Network Dispute/final live chat/equal width", "G:/OneDrive/Archive/Flight Network Dispute/final live chat/equal width/stitched.jpg"):
    print("Stitching successful")
else:
    print("Stitching failed")
