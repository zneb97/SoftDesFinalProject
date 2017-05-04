import cv2
import numpy as np

from PIL import Image
import pyscreenshot as ImageGrab
import time
from matplotlib import pyplot as plt


def detect_food(image):
    print("detecting food..")
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 10,
                               param1=10, param2=20, minRadius=10, maxRadius=30)
    if circles is not None:
        circles = np.uint16(np.around(circles))
    print("detecting complete!")
    return circles


def detect_enemy(image):
    print("detecting enemy..")
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1, 60,
                               param1=10, param2=32, minRadius=30)
    if circles is not None:
        circles = np.uint16(np.around(circles))
    print("detecting complete!")
    return circles
# def get_self_mass():


if __name__ == '__main__':

    framecount = 0
    time_elapsed = 0
    while(True):
        start = time.time()
        # img = ImageGrab.grab()
        #
        # img_np = np.array(img)
        raw_img = cv2.imread('sample.png', 0)

        cimg = raw_img
        cimg = cv2.cvtColor(cimg, cv2.COLOR_GRAY2BGR)
        # ret, cimg = cv2.threshold(cimg, 130, 255, cv2.THRESH_BINARY)
        cimg = cv2.GaussianBlur(cimg, (7, 7), 0)
        cimg = cv2.medianBlur(cimg, 5)
        cimg = cv2.Canny(cimg, 50, 100)
        # cv2.imshow("detected circles", cimg)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite("processed_image.png", cimg)
        print("image loaded")

        foods = detect_food(cimg)
        enemies = detect_enemy(cimg)

        end = time.time()
        time_elpased = round(end - start, 1)
        print("Time Elapsed : " + str(time_elpased) + "sec")
        for i in foods[0, :]:
            # draw the outer circle
            cv2.circle(raw_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(raw_img, (i[0], i[1]), 2, (0, 0, 255), 3)

        for i in enemies[0, :]:
            # draw the outer circle
            cv2.circle(raw_img, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(raw_img, (i[0], i[1]), 2, (0, 0, 255), 3)
        cv2.imwrite("detected circles.png", raw_img)


        try:
            # framecount += 1
            # print(framecount)
            # time.sleep(0.1)
            break
        except KeyboardInterrupt:
            break
