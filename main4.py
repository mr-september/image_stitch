import cv2
import os

def stitch_screenshots(screenshot_folder, output_file, images_per_stitch=None):
    screenshots = []
    for screenshot_file in os.listdir(screenshot_folder):
        screenshot = cv2.imread(os.path.join(screenshot_folder, screenshot_file))
        screenshots.append(screenshot)
    
    try:
        stitcher = cv2.createStitcher()
    except:
        stitcher = cv2.Stitcher_create()
    
    if images_per_stitch is None:
        print("Stitching all images in a single batch...")
        (status, stitched) = stitcher.stitch(screenshots)

        if status != 0:
            print("Stitching failed with error code {}".format(status))
            return False
        
        cv2.imwrite(output_file, stitched)
        return True
    else:
        batch_count = len(screenshots) // images_per_stitch + 1
        for i in range(batch_count):
            start = i * images_per_stitch
            end = min((i+1) * images_per_stitch, len(screenshots))
            batch = screenshots[start:end]
            print(f"Stitching batch {i+1} of {batch_count}...")
            (status, stitched) = stitcher.stitch(batch)
            
            if status != 0:
                print("Stitching batch {} failed with error code {}".format(i+1, status))
                return False
            
            cv2.imwrite(f"{output_file}_{i}.jpg", stitched)
        
        print("Stitching successful")
        return True

    
if stitch_screenshots("G:/OneDrive/Archive/Flight Network Dispute/final live chat/equal width", "G:/OneDrive/Archive/Flight Network Dispute/final live chat/equal width/stitched.jpg", images_per_stitch=5):
    print("Stitching successful")
else:
    print("Stitching failed")
