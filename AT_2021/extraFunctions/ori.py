
import cv2
import numpy as np
import msvcrt

from PIL import ImageEnhance

cropping = False

x_start, y_start, x_end, y_end = 0, 0, 0, 0

#image = cv2.imread('curved_lanes.jpg')
image = cv2.imread('C:/Users/modys/Desktop/Python test/footage3.jpeg')
oriImage = image.copy()


def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping

    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True

    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False # cropping is finished

        refPoint = [(x_start, y_start), (x_end, y_end)]

        if len(refPoint) == 2: #when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)
            alpha = 1.5  # Contrast control (1.0-3.0)
            beta = 0  # Brightness control (0-100)

            adjusted = cv2.convertScaleAbs(roi, alpha=alpha, beta=beta)
            #cv2.imshow('original', image)
            #cv2.imshow('adjusted', adjusted)

            gray = cv2.cvtColor(adjusted, cv2.COLOR_RGB2GRAY)  #Converts to grayscale image
            blur = cv2.GaussianBlur(gray,(5,5),0)   #Apply an Gassuian filter to the image
            canny = cv2.Canny(blur,50,150)  #Apply Canny function, (image,low_threshold, high_threshold) 50,150

            lines = cv2.HoughLinesP(canny,2,np.pi/180,100,np.array([]), minLineLength=15, maxLineGap=5)

            cv2.imshow("Cropped-canny", canny)

            line_image = np.zeros_like(roi)    #Create a black image with the same dimension as our image
            if lines is not None:            #Check if we found any lines (in this case lanes) in the image
                print('Found line coord x1, y1, x2. y2')
                for line in lines:
                    print(line)  #Prints out line posistions
                    x1, y1, x2, y2 = line.reshape(4)  #Reshapes to 1d with 4 arrays. The positions that defines the lines
                    cv2.line(line_image, (x1, y1), (x2, y2), (255,0,0),10)  #Draws the found line

            combo_image = cv2.addWeighted(roi,0.8,line_image,1,1)


            cv2.imshow("result 4", line_image)    # Display the masked image
            cv2.waitKey(0)       # Specify how long the image

            cv2.imshow("result 5", combo_image)    # Display the masked image
            cv2.waitKey(0)       # Specify how long the image









cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)
done = False
while not done:

    i = image.copy()

    if not cropping:
        cv2.imshow("image", image)

    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)

    elif ord(msvcrt.getch()) == "c":
        cropping = False

    if cv2.waitKey(1) == 27:
        done = True

# close all open windows
#cv2.destroyAllWindows()
