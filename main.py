# Importing all necessary libraries
import cv2
import os
import pytesseract
import numpy as np


# Read the video from webcam
cam = cv2.VideoCapture(0)
# frame size
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pytesseract.pytesseract.tesseract_cmd = 'F:\\tesserant\\tesseract.exe'
image = cv2.imread("Task_2.png") # read the image task2


#separating dots based on colour
imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret1, thresh1 = cv2.threshold(imgray, 90, 255, cv2.THRESH_BINARY)  # output will be only blue dots
ret2, thresh2 = cv2.threshold(imgray, 120, 255, cv2.THRESH_BINARY) # output will be blue and red dots
ret3, thresh3 = cv2.threshold(imgray, 130, 255, cv2.THRESH_BINARY) # output will br blue ,green and red dots
# xor removes dots in common
# grayscale image is turned into black and white(binary) to get center of the dots perfectly
G = cv2.bitwise_xor(thresh2, thresh3, mask=None)
R = cv2.bitwise_xor(thresh2, thresh1, mask=None)
ret4, B = cv2.threshold(imgray, 90, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("image",image)


try:

    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')

# if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0
con = 8

while (True):

    # reading from frame
    ret, frame = cam.read()
    cv2.imshow("Webcam", frame)
    cv2.waitKey(2000)

    while con == 8:
        # if video is still left continue creating images
        name = './data/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name)

        # writing the extracted images
        adaptive_threshold = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,85,11)
        print(pytesseract.image_to_string(adaptive_threshold))
        text = pytesseract.image_to_string(adaptive_threshold)
  # according to my idea in place of B here i planned to put text but for some reason it is not detecting text
        detected_circles = cv2.HoughCircles(B, cv2.HOUGH_GRADIENT, 1, 10, param1=10, param2=10, minRadius=1, maxRadius=30)


        detected_circles = np.uint16(np.around(detected_circles))
        dot_x = []  # x co-ordinate of a particular colour dots
        dot_y = []  # y co-ordinate of a particular colour dots
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            dot_x.append(a)
            dot_y.append(b)
        print(dot_x, dot_y)

        h = 200
        k = 200

        #x  co-ordinate
        X_center = [] # collecting all the center values in array to make ease of bot movement
        # y co-ordinate
        Y_center = [] # dot will be drawn in these centers
        for i in range(0, len(dot_x), 1):
            print("R O U N D ", i)
            H = 0
            K = 0
            j = 0
            i1 = 0
            i2 = 0
            p = 0
            q = 0
            # if bot attains steady state loop stops
            while H != h or K != k: # if e1 is 0 H = h and if e2 = 0 K = 0
                ex = dot_x[i] - h # error is desired position - current position
                ey = dot_y[i] - k
                i1 = i1 + ex  # integral of the error
                i2 = i2 + ey                # dt = 1   1 iteration is 1 count
                p1 = ex - p  # derivative of the error
                p = ex
                p2 = ey - q
                q = ey
                H = h
                K = k
                X_center.append(h)
                Y_center.append(k)
                # here final velocity after bot reached the dot is 0,so there is no steady state error ,so kp and ki values are 0.
                h = h + ex * 0.5 + 0 * i1 + 0 * p1
                k = k + ey * 0.5 + 0 * i2 + 0 * p2
                print(h, k)

        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
        cv2.waitKey(5000)

        print(len(X_center))

        for i in range(0, len(X_center), 1):
            print(X_center[i], Y_center[i])
            image = cv2.circle(image, (round(X_center[i]), round(Y_center[i])), 3, (0, 0, 0), -1)
            cv2.imshow("bot_movement", image)
            cv2.waitKey(1)

        con = int(input("enter the number")) # to run again enter 8
    break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()


