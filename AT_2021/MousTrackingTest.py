import cv2
import numpy as np

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix, iy = -1, -1


class MyDefineRoi:
    def __init__(self):
        self.roi = []
        self.drawing = False
        self.Default = []
        self.img = []
        self.ix = 0
        self.iy = 0
        self.mode = True

    def define_roi(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                self.img = self.Default.copy()
                cv2.rectangle(self.img, (self.ix, self.iy), (x, y), (0, 255, 0), 1)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            # self.roi = self.ix, self.iy, x, y
            if self.ix < x:
                if self.iy < y:
                    self.roi = self.ix, self.iy, x-self.ix+1, y-self.iy+1
                else:
                    self.roi = self.ix, y, x-self.ix+1, self.iy-y+1

            else:
                if self.iy < y:
                    self.roi = x, self.iy, self.ix-x+1, y - self.iy+1
                else:
                    self.roi = x, y, self.ix-x+1, self.iy - y+1
            # cv2.rectangle(self.img, (self.ix, self.iy), (x, y), (255, 0, 0), 2)
            cv2.rectangle(self.img, self.roi, (255, 0, 0), 1)

                # self.roi = x, y, self.ix - x, self.iy-y

            print(self.roi)


img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
user_roi = MyDefineRoi()
user_roi.img = img.copy()
user_roi.Default = img.copy()
# cv2.setMouseCallback('image',draw_circle)
cv2.setMouseCallback('image', user_roi.define_roi)
while(1):
    cv2.imshow('image', user_roi.img)
    k = cv2.waitKey(1)
    if k == 13:  # enter
        vehicle_placement = user_roi.roi
        print(vehicle_placement)
        break
    elif k == ord('c'):  # cancel selection
        vehicle_placement = (0, 0, 0, 0)
        print(vehicle_placement)
        break
    elif k == ord('s'):
        user_roi.roi = user_roi.roi[0], user_roi.roi[1] + 1, user_roi.roi[2], user_roi.roi[3]
        user_roi.img = user_roi.Default.copy()
        cv2.rectangle(user_roi.img, user_roi.roi, (255, 0, 0), 1)
        print(user_roi.roi)
    elif k == ord('w'):
        user_roi.roi = user_roi.roi[0], user_roi.roi[1] - 1, user_roi.roi[2], user_roi.roi[3]
        user_roi.img = user_roi.Default.copy()
        cv2.rectangle(user_roi.img, user_roi.roi, (255, 0, 0), 1)
        print(user_roi.roi)
    elif k == ord('d'):
        user_roi.roi = user_roi.roi[0] + 1, user_roi.roi[1], user_roi.roi[2], user_roi.roi[3]
        user_roi.img = user_roi.Default.copy()
        cv2.rectangle(user_roi.img, user_roi.roi, (255, 0, 0), 1)
        print(user_roi.roi)
    elif k == ord('a'):
        user_roi.roi = user_roi.roi[0] - 1, user_roi.roi[1], user_roi.roi[2], user_roi.roi[3]
        user_roi.img = user_roi.Default.copy()
        cv2.rectangle(user_roi.img, user_roi.roi, (255, 0, 0), 1)
        print(user_roi.roi)
    elif k == ord('5'):
        user_roi.roi = user_roi.roi[0], user_roi.roi[1], user_roi.roi[2], user_roi.roi[3] + 1
        user_roi.img = user_roi.Default.copy()
        cv2.rectangle(user_roi.img, user_roi.roi, (255, 0, 0), 1)
        print(user_roi.roi)
    elif k == ord('8'):
        user_roi.roi = user_roi.roi[0], user_roi.roi[1], user_roi.roi[2], user_roi.roi[3] - 1
        user_roi.img = user_roi.Default.copy()
        cv2.rectangle(user_roi.img, user_roi.roi, (255, 0, 0), 1)
        print(user_roi.roi)
    elif k == ord('6'):
        user_roi.roi = user_roi.roi[0], user_roi.roi[1], user_roi.roi[2] + 1, user_roi.roi[3]
        user_roi.img = user_roi.Default.copy()
        cv2.rectangle(user_roi.img, user_roi.roi, (255, 0, 0), 1)
        print(user_roi.roi)
    elif k == ord('4'):
        user_roi.roi = user_roi.roi[0], user_roi.roi[1], user_roi.roi[2] - 1, user_roi.roi[3]
        user_roi.img = user_roi.Default.copy()
        cv2.rectangle(user_roi.img, user_roi.roi, (255, 0, 0), 1)
        print(user_roi.roi)
#
# cv2.destroyAllWindows()
