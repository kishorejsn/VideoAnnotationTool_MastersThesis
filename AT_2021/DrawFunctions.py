from typing import List, Any, Union, Tuple

import cv2
import numpy as np
from lane_detection import *
# from MousTrackingTest import MyDefineRoi
# from canny_avg import *

Green = (0, 255, 0)
Yellow = (0, 255, 255)
Blue = (255, 0, 0)
BlueGreen = (255, 255, 0)
Red = (0, 0, 255)
DarkRed = (0, 50, 180)
Black = (0, 0, 0)

circle_rad = 2
circle_thickness = 2
rescale = 2

class MyDefineRoi:
    def __init__(self):
        self.drawing = False
        self.roi = []
        self.mode = True
        self.Default = []
        self.img = []
        self.ix = 0
        self.iy = 0
        self.roi_o = []
        self.Default_o = []
        self.img_o = []
        self.ix_o = 0
        self.iy_o = 0

    def define_roi(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
            self.ix_o, self.iy_o = round(x/rescale), round(y/rescale)


        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                self.img = self.Default.copy()
                cv2.rectangle(self.img, (self.ix, self.iy), (x, y), Blue, 1)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            if self.ix < x:
                if self.iy < y:
                    self.roi = self.ix, self.iy, x-self.ix+1, y-self.iy+1
                    self.roi_o = self.ix_o, self.iy_o, round(x/rescale) - self.ix_o + 1, round(y/rescale) - self.iy_o + 1
                else:
                    self.roi = self.ix, y, x-self.ix+1, self.iy-y+1
                    self.roi_o = self.ix_o, round(y/rescale), round(x/rescale) - self.ix_o + 1, self.iy_o - round(y/rescale) + 1

            else:
                if self.iy < y:
                    self.roi = x, self.iy, self.ix-x+1, y - self.iy+1
                    self.roi_o = round(x/rescale), self.iy_o, self.ix_o - round(x/rescale) + 1, round(y/rescale) - self.iy_o + 1
                else:
                    self.roi = x, y, self.ix-x+1, self.iy - y+1
                    self.roi = round(x/rescale), round(y/rescale), self.ix_o - round(x/rescale) + 1, self.iy_o - round(y/rescale) + 1

            print(self.roi)
            print(self.roi_o)
            cv2.rectangle(self.img, self.roi, Blue, 1)



class store_point_coord:
    def __init__(self):
        self.point = []
        self.point_o = []
        self.done = False

    def drawing_done(self, keypress):
        if keypress == 13: # press enter to confirm selection
            self.done = True
        elif keypress == ord('c') or keypress == ord('C'): # press c to cancel selection
            self.__init__()
            self.done = True

        return self.done

    def draw_point(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            center = (x, y)
            radius = 2
            cv2.circle(param, center, radius, Blue, 2)
            self.point.append((x, y))
            self.point_o.append((round(x/rescale), round(y/rescale)))


mySelectRoi = MyDefineRoi()
coord_store = store_point_coord()


def define_vehicle_wheels(win_name, img, annotation_data, annotation_data_sv, annotation_data_adj, i, adnr):

    my_draw_annotations(img, annotation_data, i, draw_pov_wheels=False)

    img_copy = img.copy()
    coord_store.__init__()
    cv2.setMouseCallback(win_name, coord_store.draw_point, img_copy)

    while not coord_store.drawing_done(cv2.waitKey(1)):
        cv2.imshow(win_name, img_copy)

    cv2.setMouseCallback(win_name, do_nothing, img_copy)

    for i2 in range(len(coord_store.point)):
        cv2.circle(img, coord_store.point[i2][:], circle_rad, DarkRed, circle_thickness)

    if coord_store.point:
        for i2 in range(len(coord_store.point)):
            cv2.circle(img, coord_store.point[i2][:], circle_rad, Green, circle_thickness)

        if adnr == 1:
            annotation_data.pov_wheels[i] = 1, coord_store.point
            annotation_data.pov_wheels_o[i] = 1, coord_store.point_o
        elif adnr == 2:
            annotation_data_sv.sv_wheels[i] = 1, coord_store.point
            annotation_data_sv.sv_wheels_o[i] = 1, coord_store.point_o
        elif adnr == 3:
            annotation_data_adj.adj_wheels[i] = 1, coord_store.point
            annotation_data_adj.adj_wheels_o[i] = 1, coord_store.point_o
    else:
        if adnr == 1:
            annotation_data.pov_wheels[i] = 0, [(np.nan, np.nan)]
            annotation_data.pov_wheels_o[i] = 0, [(np.nan, np.nan)]
        elif adnr == 2:
            annotation_data_sv.sv_wheels[i] = 0, [(np.nan, np.nan)]
            annotation_data_sv.sv_wheels_o[i] = 0, [(np.nan, np.nan)]
        elif adnr == 3:
            annotation_data_adj.adj_wheels[i] = 0, [(np.nan, np.nan)]
            annotation_data_adj.adj_wheels_o[i] = 0, [(np.nan, np.nan)]
    return


def define_lane_left(win_name, img, annotation_data, i):

    my_draw_annotations(img, annotation_data, i, draw_lane_placement_left=False)

    img_copy = img.copy()
    coord_store.__init__()
    cv2.setMouseCallback(win_name, coord_store.draw_point, img_copy)

    while not coord_store.drawing_done(cv2.waitKey(1)):
        cv2.imshow(win_name, img_copy)

    cv2.setMouseCallback(win_name, do_nothing, img_copy) # to turn off the mouse callback

    if coord_store.point:
        for i2 in range(len(coord_store.point)):
            cv2.circle(img, coord_store.point[i2][:], circle_rad, Green, circle_thickness)
        annotation_data.lane_placement_left[i] = 1, coord_store.point
        annotation_data.lane_placement_left_o[i] = 1, coord_store.point_o

    else:
        annotation_data.lane_placement_left[i] = 0, [(np.nan, np.nan)]
        annotation_data.lane_placement_left_o[i] = 0, [(np.nan, np.nan)]
    return


def define_lane_right(win_name, img, annotation_data, i):

    my_draw_annotations(img, annotation_data, i, draw_lane_placement_right=False)

    img_copy = img.copy()
    coord_store.__init__()
    cv2.setMouseCallback(win_name, coord_store.draw_point, img_copy)

    while not coord_store.drawing_done(cv2.waitKey(1)):
        cv2.imshow(win_name, img_copy)

    cv2.setMouseCallback(win_name, do_nothing, img_copy)

    if coord_store.point:
        for i2 in range(len(coord_store.point)):
            cv2.circle(img, coord_store.point[i2][:], circle_rad, Green, circle_thickness)
            annotation_data.lane_placement_right[i] = 1, coord_store.point
            annotation_data.lane_placement_right_o[i] = 1, coord_store.point_o
    else:
        annotation_data.lane_placement_right[i] = 0, [(np.nan, np.nan)]
        annotation_data.lane_placement_right_o[i] = 0, [(np.nan, np.nan)]
    return


def do_nothing(event, x, y, flags, param):
    pass


def define_vehicle(win_name, img, annotation_data, annotation_data_sv, annotation_data_adj, i, adnr):
    my_draw_annotations(img, annotation_data, i, draw_pov_placement=False)
    mySelectRoi.img = img.copy()
    mySelectRoi.Default = img.copy()

    cv2.setMouseCallback(win_name, mySelectRoi.define_roi)

    while 1:
        cv2.imshow(win_name, mySelectRoi.img)
        k = cv2.waitKey(1)
        if k == ord('s'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1] + 1, mySelectRoi.roi[2], mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('w'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1] - 1, mySelectRoi.roi[2], mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)

        elif k == ord('d'):
            mySelectRoi.roi = mySelectRoi.roi[0] + 1, mySelectRoi.roi[1], mySelectRoi.roi[2], mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('a'):
            mySelectRoi.roi = mySelectRoi.roi[0] - 1, mySelectRoi.roi[1], mySelectRoi.roi[2], mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('5'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1], mySelectRoi.roi[2], mySelectRoi.roi[3] + 1
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('8'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1], mySelectRoi.roi[2], mySelectRoi.roi[3] - 1
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('6'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1], mySelectRoi.roi[2] + 1, mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('4'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1], mySelectRoi.roi[2] - 1, mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == 13:# enter
            vehicle_placement = mySelectRoi.roi
            vehicle_placement_o = [round(i/rescale) for i in vehicle_placement]
            break
        elif k == ord('c') or k == ord('C'): #cancel selection
            vehicle_placement = (0, 0, 0, 0)
            vehicle_placement_o = (0, 0, 0, 0)
            break

    cv2.setMouseCallback(win_name, do_nothing, mySelectRoi.img)

    if vehicle_placement == (0, 0, 0, 0):
        if adnr == 1:
            annotation_data.pov_placement[i] = 0, (np.nan, np.nan, np.nan, np.nan)
            annotation_data.pov_placement_o[i] = 0, (np.nan, np.nan, np.nan, np.nan)
        elif adnr == 2:
            annotation_data_sv.sv_placement[i] = 0, (np.nan, np.nan, np.nan, np.nan)
            annotation_data_sv.sv_placement_o[i] = 0, (np.nan, np.nan, np.nan, np.nan)
        elif adnr == 3:
            annotation_data_adj.adj_placement[i] = 0, (np.nan, np.nan, np.nan, np.nan)
            annotation_data_adj.adj_placement_o[i] = 0, (np.nan, np.nan, np.nan, np.nan)

        return
    else:
        if adnr == 1:
            cv2.rectangle(img, vehicle_placement, Green, 1)
            annotation_data.pov_placement[i] = 1, vehicle_placement
            annotation_data.pov_placement_o[i] = 1, vehicle_placement_o
        elif adnr == 2:
            cv2.rectangle(img, vehicle_placement, Green, 1)
            annotation_data_sv.sv_placement[i] = 1, vehicle_placement
            annotation_data_sv.sv_placement_o[i] = 1, vehicle_placement_o
        elif adnr == 3:
            cv2.rectangle(img, vehicle_placement, Green, 1)
            annotation_data_adj.adj_placement[i] = 1, vehicle_placement
            annotation_data_adj.adj_placement_o[i] = 1, vehicle_placement_o
        return


def define_lp(win_name, img, annotation_data, annotation_data_sv, annotation_data_adj, i, adnr):
    my_draw_annotations(img, annotation_data, i)

    mySelectRoi.img = img.copy()
    mySelectRoi.Default = img.copy()
    cv2.setMouseCallback(win_name, mySelectRoi.define_roi)

    while 1:
        cv2.imshow(win_name, mySelectRoi.img)
        k = cv2.waitKey(1)
        if k == ord('s'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1] + 1, mySelectRoi.roi[2], mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('w'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1] - 1, mySelectRoi.roi[2], mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)

        elif k == ord('d'):
            mySelectRoi.roi = mySelectRoi.roi[0] + 1, mySelectRoi.roi[1], mySelectRoi.roi[2], mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('a'):
            mySelectRoi.roi = mySelectRoi.roi[0] - 1, mySelectRoi.roi[1], mySelectRoi.roi[2], mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('5'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1], mySelectRoi.roi[2], mySelectRoi.roi[3] + 1
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('8'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1], mySelectRoi.roi[2], mySelectRoi.roi[3] - 1
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('6'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1], mySelectRoi.roi[2] + 1, mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == ord('4'):
            mySelectRoi.roi = mySelectRoi.roi[0], mySelectRoi.roi[1], mySelectRoi.roi[2] - 1, mySelectRoi.roi[3]
            mySelectRoi.img = mySelectRoi.Default.copy()
            cv2.rectangle(mySelectRoi.img, mySelectRoi.roi, (255, 0, 0), 1)
            # print(mySelectRoi.roi)
        elif k == 13:  # enter
            lp_placement1 = mySelectRoi.roi
            lp_placement = tuple(ele1 for ele1 in lp_placement1)

            break
        elif k == ord('c') or k == ord('C'):  # cancel selection
            lp_placement = (0, 0, 0, 0)
            break

    cv2.setMouseCallback(win_name, do_nothing, mySelectRoi.img)

    if lp_placement == (0, 0, 0, 0):
        if adnr == 1:
            annotation_data.lp_pos = (np.nan, np.nan, np.nan, np.nan)
        elif adnr == 2:
            annotation_data_sv.lp_pos = (np.nan, np.nan, np.nan, np.nan)
        elif adnr == 3:
            annotation_data_adj.lp_pos = (np.nan, np.nan, np.nan, np.nan)
        return

    else:
        cv2.rectangle(img, lp_placement, Green, 1)
        if not np.isnan((annotation_data.pov_placement[i][1][2])):
            pixel_per_metric = lp_placement[2]/annotation_data.lp_dim
            vehicle_width = annotation_data.pov_placement[i][1][2]/pixel_per_metric
            print(vehicle_width)
        if adnr == 1:
            annotation_data.lp_pos = lp_placement
            annotation_data.pov_width = vehicle_width
        elif adnr == 2:
            annotation_data_sv.lp_pos = lp_placement
            annotation_data_adj.sv_width = vehicle_width
        elif adnr == 3:
            annotation_data_adj.lp_pos = lp_placement
            annotation_data_adj.adj_width = vehicle_width


    return


def my_draw_annotations(img, annotation_data, i, draw_all=True, draw_pov_placement=True, draw_pov_wheels=True,
                        draw_lane_placement_left=True, draw_lane_slope_left=True,
                        draw_lane_placement_right=True, draw_lane_slope_right=True):
    if draw_all:
        # draw pov_placement of true
        if draw_pov_placement:
            if not np.isnan(annotation_data.pov_placement[i][1][0]):
                if annotation_data.pov_placement[i][0]:
                    cv2.rectangle(img, annotation_data.pov_placement[i][1], Green, 1)
                else:
                    cv2.rectangle(img, annotation_data.pov_placement[i][1], BlueGreen, 1)

                cv2.putText(img, str(round(annotation_data.pov_distance_long[i], 2))+'m',
                            (annotation_data.pov_placement[i][1][0], annotation_data.pov_placement[i][1][1]-5),
                            cv2.FONT_HERSHEY_SIMPLEX,  fontScale=0.4,
                            thickness=1, color=Black)
                cv2.putText(img, str(round(-annotation_data.pov_distance_lat[i], 2)) + 'm',
                            (annotation_data.pov_placement[i][1][0],
                             annotation_data.pov_placement[i][1][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.4,
                            thickness=1, color=Black)

        # draw pov_wheels if true
        if draw_pov_wheels:
            if not np.isnan(annotation_data.pov_wheels[i][1][0][0]):
                for i2 in range(len(annotation_data.pov_wheels[i][1])):
                    cv2.circle(img, annotation_data.pov_wheels[i][1][i2][:], circle_rad, DarkRed, circle_thickness)

        # draw lane_placement if true
        if draw_lane_placement_left:
            if not np.isnan(annotation_data.lane_placement_left[i][1][0][0]):
                for i2 in range(len(annotation_data.lane_placement_left[i][1])):
                    cv2.circle(img, annotation_data.lane_placement_left[i][1][i2][:], circle_rad, Green,
                               circle_thickness)

            if draw_lane_slope_left:
                if not np.isnan(annotation_data.lane_slope_left[i][1][0]):  # for all slopes
                    x1 = annotation_data.lane_slope_points_left[i][0]
                    y1 = annotation_data.lane_slope_points_left[i][1]
                    x2 = annotation_data.lane_slope_points_left[i][2]
                    y2 = annotation_data.lane_slope_points_left[i][3]

                    thick = 20  # abs(y1-y2) #20  # Thickness of ROI
                    length = -20  # abs(x1-x2) # 70
                    # lane_detection(img, x1, x2, y1, y2, thick, length)

                    cv2.line(img, (x1, y1), (x2, y2), Red, 1)

        if draw_lane_placement_right:
            if not np.isnan(annotation_data.lane_placement_right[i][1][0][0]):
                for i2 in range(len(annotation_data.lane_placement_right[i][1])):
                    cv2.circle(img, annotation_data.lane_placement_right[i][1][i2][:], circle_rad, Yellow, circle_thickness)

            if draw_lane_slope_right:
                if not np.isnan(annotation_data.lane_slope_right[i][1][0]):  # for all slopes
                    x1 = annotation_data.lane_slope_points_right[i][0]
                    y1 = annotation_data.lane_slope_points_right[i][1]
                    x2 = annotation_data.lane_slope_points_right[i][2]
                    y2 = annotation_data.lane_slope_points_right[i][3]

                    cv2.line(img, (x1, y1), (x2, y2), BlueGreen, 1)

        if draw_lane_placement_right and draw_lane_placement_left:
            # draw image center and vp
            if not np.isnan(annotation_data.lanes_vp[i][0]):
                img_center = int(annotation_data.frame_size[1]/2), int(annotation_data.frame_size[0]/2)
                vp = annotation_data.lanes_vp[i]
                # cv2.circle(img, img_center, circle_rad, BlueGreen, circle_thickness)
                # cv2.circle(img, vp, 5, Red, 2)

        if draw_pov_wheels and draw_lane_placement_left and draw_lane_placement_right and draw_pov_placement:
            pov_placement = annotation_data.pov_placement[i][1]
            extruded_box = annotation_data.pov_extruded_box[i]

            if not np.isnan(extruded_box[0]):
                # draw 3D box
                cv2.rectangle(img, extruded_box, Green, 1)
                cv2.line(img, (extruded_box[0], extruded_box[1]), (pov_placement[0], pov_placement[1]), Blue, 1)
                cv2.line(img, (extruded_box[0] + extruded_box[2], extruded_box[1]),
                         (pov_placement[0] + pov_placement[2], pov_placement[1]), Yellow, 1)

                cv2.line(img, (extruded_box[0], extruded_box[1] + extruded_box[3]),
                         (pov_placement[0], pov_placement[1] + pov_placement[3]), Green, 1)
                cv2.line(img, (extruded_box[0] + extruded_box[2], extruded_box[1] + extruded_box[3]),
                         (pov_placement[0] + pov_placement[2], pov_placement[1] + pov_placement[3]), Black, 1)

