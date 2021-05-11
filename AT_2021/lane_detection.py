#What to fix:


#Import libraries
import cv2
import os
import math
import numpy as np
import matplotlib.pyplot as plt
    #Clear the terminal

#Extrapolation of the detected lane
def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]  #Start at the bottom of the image
    y2 = int(y1*(3/5))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])


def average_slope_intercept(image,lines,original_slope):
    left_fit = []
    left_line = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2), (y1,y2),1)
        slope = parameters[0]
        intercept = parameters[1]

        low_lim = 0.8
        up_lim = 1.2
        if original_slope > 0:
            valid_slope = original_slope * low_lim < slope < original_slope * up_lim
        else:
            valid_slope = original_slope * low_lim > slope > original_slope * up_lim

        if valid_slope:

            left_fit.append((slope,intercept))
            left_fit_average = np.average(left_fit, axis=0)
            left_line = make_coordinates(image,left_fit_average)
    return np.array([left_line]), slope


def region_of_interest(x1,y1,x2,y2, thick, length):
    # Define ROI
    alpha = math.atan((y2-y1)/(x2-x1))   #Angle of the lane
    beta = (math.pi)/2-alpha

    if y1 > y2:
        k = (y2-y1)/(x2-x1)
        m = y2 - k*x2
        y2 = y2 - length
        x2 = (y2 - m)/k
    elif y2 > y1:
        k = (y2-y1)/(x2-x1)
        m = y1 - k*x1
        y1 = y1 - length
        x1 = (y1 - m)/k


    x_new1 = x1 + thick * math.cos(beta)
    y_new1 = y1 - thick * math.sin(beta)
    x_new2 = x1 - thick * math.cos(beta)
    y_new2 = y1 + thick * math.sin(beta)
    x_new3 = x2 + thick * math.cos(beta)
    y_new3 = y2 - thick * math.sin(beta)
    x_new4 = x2 - thick * math.cos(beta)
    y_new4 = y2 + thick * math.sin(beta)

    myROI = [(x_new1, y_new1), (x_new2, y_new2), (x_new4, y_new4), (x_new3, y_new3)]
    return myROI

#Lane detection function

def color_mask(image,myROI):

    contr = 2 #Contrast control (1.0 - 3.0)
    bright = 50 #Brightness control (0 - 100)
    adjusted = cv2.convertScaleAbs(image, alpha=contr, beta=bright)

    #Tring stuff with colors
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  #You should also try hue
    #Yellow color
    lower_yellow = np.array([0, 25, 25])
    upper_yellow = np.array([50, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #White COLOR
    lower_white = np.uint8([160, 160, 160])
    upper_white = np.uint8([255, 255, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    #Combining
    mask = mask = cv2.bitwise_or(mask_yellow, mask_white)
    canny = cv2.Canny(mask, 50, 150)
    # Mask the image
    mask = np.zeros_like(canny)    #Black image with the same shape as the region of interest (same number of pixels)
    cv2.fillPoly(mask, np.int32([myROI]), 255)   #Create a white background fillPoly assumes int64, so you need to manually convert to int32!
    masked_image = cv2.bitwise_and(canny, mask)  #Add the binary number of these two images?

    return masked_image


def gray_mask(image,myROI,low,high):
    contr = 2 #Contrast control (1.0 - 3.0)
    bright = -50 #Brightness control (0 - 100)
    adjusted = cv2.convertScaleAbs(image, alpha=contr, beta=bright)
    gray = cv2.cvtColor(adjusted, cv2.COLOR_RGB2GRAY)  #Converts to grayscale image
    blur = cv2.GaussianBlur(gray,(5,5),0)   #Apply an Gassuian filter to the image
    canny = cv2.Canny(blur,low,high)  #Apply Canny function, (image,low_threshold, high_threshold) 60,120
    mask = np.zeros_like(canny)    #Black image with the same shape as the region of interest (same number of pixels)
    cv2.fillPoly(mask, np.int32([myROI]), 255)   #Create a white background fillPoly assumes int64, so you need to manually convert to int32!
    masked_image = cv2.bitwise_and(canny, mask)  #Add the binary number of these two images?

    return masked_image


def lane_detection(image, x1,x2,y1,y2,thick,length):
    # Process the image
    test = np.polyfit((x1,x2), (y1,y2),1)
    original_slope = test[0]

    # Define ROI
    myROI = region_of_interest(x1,y1,x2,y2, thick, length)  #Use the ROI function
    pts = np.array([myROI[0],myROI[1],myROI[2],myROI[3]], np.int32)
    pts = pts.reshape((-1,1,2))
    #cv2.polylines(image,[pts],True,(255,0,0))


    # Mask the image
    masked_image = color_mask(image,myROI)
    masked_image = gray_mask(image,myROI,50,150)

    #Find the lanes
    lines = cv2.HoughLinesP(masked_image, 1, np.pi/180, 60, maxLineGap=10)    #Curved lanes
    line_image = np.zeros_like(image)    #Create a black image with the same dimension as our image
    check_lines = 0

    #Create a black image with the same dimension as our image

    if lines is not None:  # Check if we found any lines (in this case lanes) in the image
        averaged_lines, lane_slope = average_slope_intercept(image, lines, original_slope)
        print('Found lane coord x1, y1, x2, y2')
        check_lines = 1  # Lines found
        if averaged_lines.any() == True: # is not None:
            for line in averaged_lines:
                check_lines = 1  # Lines found
                print('first loop')
                print(line)
                #print((lines[0]+lines[1])/2)  #The "average" lane. Find a better way to do this!
                x1, y1, x2, y2 = line.reshape(4)  #Reshapes to 1d with 4 arrays. The positions that defines the lines
                # cv2.line(line_image, (x1, y1), (x2, y2), (0,255,0),5)  #Draws the found line
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draws the found line
                parameters = np.polyfit((x1,x2), (y1,y2),1)
                slope_lanes = parameters[0]
                length_lane = math.sqrt(abs(x1-x2)^2+abs(y1-y2)^2)

    # print('lane detecttion: ', check_lines)

    if check_lines == 0:

        masked_image = gray_mask(image,myROI,100,250)

        #Find the lanes
        lines_2 = cv2.HoughLinesP(masked_image, 1, np.pi/180, 30, maxLineGap=50)    #Curved lanes
        line_image = np.zeros_like(image)    #Create a black image with the same dimension as our image

        if lines_2 is not None:            #Check if we found any lines (in this case lanes) in the image
            print('Found lane coord x1, y1, x2, y2')
            averaged_lines_2, lane_slope = average_slope_intercept(image,lines_2,original_slope)
            if averaged_lines_2.any() == True:
                for line in averaged_lines_2:
                    check_lines = 1  # Lines found
                    print('second loop')
                    print(line)
                    x1, y1, x2, y2 = line.reshape(4)  #Reshapes to 1d with 4 arrays. The positions that defines the lines
                    # cv2.line(line_image, (x1, y1), (x2, y2), (0,255,0),5)  #Draws the found line
                    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draws the found line
                    parameters = np.polyfit((x1,x2), (y1,y2),1)
                    slope_lanes = parameters[0]
                    length_lane = math.sqrt(abs(x1-x2)^2+abs(y1-y2)^2)

    # cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draws the found line
    # combo_image = cv2.addWeighted(image, 0.8, line_image, 1, 1)
    # cv2.imshow("result 2", combo_image)  # Displace the canny of the image
    # cv2.waitKey(0)  # Specify how long the image is displaced, 0=infinit
    return
