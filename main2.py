import cv2
import os
import numpy as np

def stitch_images(imgs, max_size=None):
    try:
        stitcher = cv2.createStitcher()
    except:
        stitcher = cv2.Stitcher_create()

    result = None
    h = 0
    for img in imgs:
        if max_size and img.shape[0] > max_size[1]:
            new_imgs = [img[i:i+max_size[1], :, :] for i in range(0, img.shape[0], max_size[1])]
            for new_img in new_imgs:
                print("stitching:", new_img.shape)
                if result is None:
                    result = new_img
                else:
                    if result.shape[1] != new_img.shape[1]:
                        raise Exception("All images should have the same number of columns")
                    result = cv2.vconcat([result, new_img])
        else:
            if result is None:
                result = img
            else:
                if result.shape[1] != img.shape[1]:
                    raise Exception("All images should have the same number of columns")
                result = cv2.vconcat([result, img])

    return result
if __name__ == '__main__':
    # input folder
    folder = 'G:/OneDrive/Archive/Flight Network Dispute/final live chat'
    imgs = [cv2.imread(os.path.join(folder, f)) for f in sorted(os.listdir(folder)) if f.endswith('.jpg')]

    result = stitch_images(imgs, max_size=(32766, 32766))

    cv2.imwrite('result.jpg', result)