import numpy as np
import math
import cv2

fc = [347.1960, 352.3415]  # Focal length
cc = [241.5788, 188.9012]
kc = [-0.423287, 0.183867, -0.038207, 0.000657, 0.000187]  # Distortion (radial, decentering, and thin-prism, if any)

cam_height = 1.5
pov_height = 1.7
pov_width = 1.99
pov_length = 4.5

Green = (0, 255, 0)
Blue = (255, 0, 0)
Red = (0, 0, 255)

scale = 1

def rectify(src):
    h,w,_ = src.shape
    A = np.array([[fc[0], 0, cc[0]], [0, fc[1], cc[1]], [0, 0, 1]])
    distCoeffs = np.array([kc[0], kc[1], kc[2], kc[3], kc[4]])

    # scale_w = w/431
    # scale_h = h/306
    #
    # h_scaled = int(round(scale_h*h))
    # w_scaled = int(round(scale_w*w))

    # src_resized = cv2.resize(src, (w_scaled, h_scaled))
    #
    # newcammtx,_ = cv2.getOptimalNewCameraMatrix(A, distCoeffs,(w,h),1, (w_scaled,h_scaled))
    # dst = cv2.undistort(src_resized, newcammtx, distCoeffs, newCameraMatrix=newcammtx)
    newcammtx, validROI = cv2.getOptimalNewCameraMatrix(A, distCoeffs,(w,h),1,(w,h))
    dst = cv2.undistort(src, A, distCoeffs, newCameraMatrix=newcammtx)
    scale_w = w/validROI[2]
    scale_h = h/validROI[3]
    h_scaled = int(round(scale_h*h))
    w_scaled = int(round(scale_w*w))
    dst = cv2.resize(dst, (w_scaled, h_scaled))
    dst = cv2.resize(dst, (w*scale,h*scale)) ######################################################################
    return dst


def get_distance(vehicel_place, pov_heading):
    if not np.isnan(pov_heading):
        vehicle_pixel_width = vehicel_place[2] / math.cos(pov_heading)/scale  ######################################################################
        distanceH = pov_width * fc[0] / vehicle_pixel_width #vehicel_place[2] # replace vehicle_place[2] by vehicle_pixel_width
    else:
        distanceH = pov_width * fc[0] / vehicel_place[2]

    xx = distanceH * distanceH - cam_height * cam_height
    distance = np.sqrt(xx)
    # print('pixel distance: ', distance)
    return distance


def transform_pov_to3D(annotation_data, i, video):

    img = video[i].copy()

    # using the interpolated lane points
    lane_slope_points_left = annotation_data.lane_slope_points_left[i]
    lane_slope_points_right = annotation_data.lane_slope_points_right[i]

    pov_placement = annotation_data.pov_placement[i][1]
    wheel_points = annotation_data.pov_wheels[i][1]

    x11 = lane_slope_points_left[0]
    y11 = lane_slope_points_left[1]
    x12 = lane_slope_points_left[2]
    y12 = lane_slope_points_left[3]

    m1 = (y11 - y12) / (x11 - x12)
    b1 = y11 - x11 * (y11 - y12) / (x11 - x12)

    x21 = lane_slope_points_right[0]
    y21 = lane_slope_points_right[1]
    x22 = lane_slope_points_right[2]
    y22 = lane_slope_points_right[3]

    m2 = (y21 - y22) / (x21 - x22)
    b2 = y21 - x21 * (y21 - y22) / (x21 - x22)

    xv = (b2 - b1) / (m1 - m2)

    yv = m1 * xv + b1

    vp = int(round(xv)), int(round(yv))

    annotation_data.lanes_vp[i] = vp
    # cv2.circle(img, vp, 5, Blue, 2)

    # frame_size = img.shape
    frame_size = annotation_data.frame_size
    image_center = int(round(frame_size[1] / 2)), int(round(frame_size[0] / 2))

    cam_yaw = -(-vp[0] + image_center[0]) / fc[0]
    cam_pitch = -(-vp[1] + image_center[1]) / fc[1]
    # print('vp', vp)
    # print('yaw', cam_yaw, 'pitch', cam_pitch)

    H = [[1, fc[0] * cam_yaw, 0],
         [-cam_yaw / fc[0], 1, fc[1] * cam_pitch],
         [0, -cam_pitch / fc[1], 1]]

    H = [[1, cam_yaw, 0],
         [-cam_yaw, 1, fc[1] * cam_pitch],
         [0, -cam_pitch / fc[1], 1]]
    #
    H = [[1, -cam_yaw, 0],
         [cam_yaw, 1, -fc[1] * cam_pitch],
         [0, cam_pitch / fc[1], 1]]

    # H = [[1, 0, -fc[0] * cam_yaw],
    #      [0, 1, -fc[1] * cam_pitch],
    #      [cam_yaw / fc[0], cam_pitch / fc[1], 1]]
    # #
    # H = [[1, 0, -fc[0] * cam_yaw],
    #      [0, 1, fc[1] * cam_pitch],
    #      [cam_yaw / fc[0], -cam_pitch / fc[1], 1]]
    # #
    # H = [[1, - cam_yaw, 0],
    #      [cam_yaw, 1, - fc[1] * cam_pitch],
    #      [cam_pitch * cam_yaw / fc[0], cam_pitch / fc[1], 1]]
    #
    # R_mul = get_R(cam_pitch, cam_yaw)
    #
    # R_mul[0,2] = R_mul[0,2]*fc[0]
    # R_mul[1, 2] = R_mul[1, 2] * fc[1]
    # R_mul[2, 0] = R_mul[2, 0] / fc[0]
    # R_mul[2, 1] = R_mul[2, 1] / fc[1]
    #
    # H = R_mul
    #
    RR = [[1, 0, 0],
          [0, 1, 0],
          [0, 0, 1]]
    H1 = np.array(np.matmul(H, RR))
    new_img = cv2.warpPerspective(img, H1, (img.shape[1], img.shape[0]))

    vp_H = my_warp_perspective(vp, H)
    # vp_H = cv2.warpPerspective(vp, H1, (1, 1))

    vp_H = int(round(vp_H[0])), int(round(vp_H[1]))

    cv2.circle(new_img, vp_H, 5,  (0, 0, 255), 2)
    print(vp_H)
    cv2.circle(new_img, image_center, 5, (0, 255, 0), 1)
    cv2.imshow('win', new_img)

    # wheel_1_x, wheel_1_y = homo_trans(H, wheel_points[0], image_center)
    wheel_1_x, wheel_1_y = my_warp_perspective(wheel_points[0], H)
    x3d_wheel_1, y3d_wheel_1, z3d_wheel_1 = from2d23d((wheel_1_x,wheel_1_y), image_center)

    # z3d_wheel_1 = -cam_height
    # y3d_wheel_1 = fc[1] * z3d_wheel_1 / wheel_1_y
    # x3d_wheel_1 = y3d_wheel_1 * wheel_1_x / fc[0]

    # wheel_2_x, wheel_2_y = homo_trans(H, wheel_points[1], image_center)
    wheel_2_x, wheel_2_y = my_warp_perspective(wheel_points[1], H)
    x3d_wheel_2, y3d_wheel_2, z3d_wheel_2 = from2d23d((wheel_2_x,wheel_2_y), image_center)

    # z3d_wheel_2 = -cam_height
    # y3d_wheel_2 = fc[1] * z3d_wheel_2 / wheel_2_y
    # x3d_wheel_2 = y3d_wheel_2 * wheel_2_x / fc[0]

    X = x3d_wheel_2 - x3d_wheel_1
    Y = y3d_wheel_2 - y3d_wheel_1

    annotation_data.pov_wheels_YX[i] = (x3d_wheel_1, y3d_wheel_1), (x3d_wheel_2, y3d_wheel_2)

    pov_heading = -math.atan(X / Y)
    print('heading angle: ', pov_heading)

    extruded_box, y_homo = get_3d_box(pov_heading, pov_placement, H, image_center, annotation_data, i)
    annotation_data.pov_distancem2[i] = y_homo

    annotation_data.lane_points_YX_left[i] = transform_lane_3d(annotation_data.lane_slope_points_left[i], H, image_center)
    annotation_data.lane_points_YX_right[i] = transform_lane_3d(annotation_data.lane_slope_points_right[i], H, image_center)

    annotation_data.pov_heading[i] = pov_heading
    annotation_data.pov_extruded_box[i] = extruded_box

    latdistance_pov_to_lane(annotation_data, i, H, image_center)

    return pov_heading, extruded_box

def transform_lane_3d(lane_slope_points, H, image_center):
    # lane_slope_points_left = annotation_data.lane_slope_points_left[i]
    # lane_slope_points_right = annotation_data.lane_slope_points_right[i]

    x1 = lane_slope_points[0]
    y1 = lane_slope_points[1]
    x2 = lane_slope_points[2]
    y2 = lane_slope_points[3]

    # x1_right = lane_slope_points_right[0]
    # y1_right = lane_slope_points_right[1]
    # x2_right = lane_slope_points_right[2]
    # y2_right = lane_slope_points_right[3]

    lane_points = [None] * 2
    transformed_lane_points = [None] * 2
    real_lane_points = [None] * 2

    lane_points[0] = x1, y1
    lane_points[1] = x2, y2

    for i2 in range(2):
        # transformed_lane_points[i2] = homo_trans(H, lane_points[i2], image_center)
        transformed_lane_points[i2] = my_warp_perspective(lane_points[i2], H)
        x, y, z = from2d23d(transformed_lane_points[i2], image_center)

        # z = -cam_height
        # y = fc[1] * z / transformed_lane_points[i2][1]
        # x = y * transformed_lane_points[i2][0] / fc[0]

        real_lane_points[i2] = x, y, z

    return real_lane_points[0][0:2], real_lane_points[1][0:2]


def latdistance_pov_to_lane(annotation_data, i, H, image_center):

    pov_placement = annotation_data.pov_placement[i][1]
    lane_slope_left = annotation_data.lane_slope_left[i]
    lane_slope_right = annotation_data.lane_slope_right[i]
    extruded_box = annotation_data.pov_extruded_box[i]

    # determine if the pov is left or right of the sv
    center_line_image_x = annotation_data.frame_size[1]/2

    if center_line_image_x < pov_placement[0]: # the pov is on the right
        lane_slope = lane_slope_right
        pov_point = extruded_box[0], extruded_box[1] + extruded_box[3]
    else:
        lane_slope = lane_slope_left
        pov_point = extruded_box[0] + extruded_box[2], extruded_box[1] + extruded_box[3]

    # transformed_pov_point = homo_trans(H, pov_point, image_center)
    transformed_pov_point = my_warp_perspective(pov_point, H)
    x, y, z = from2d23d(transformed_pov_point, image_center)

    # z = -cam_height
    # y = fc[1] * z / transformed_pov_point[1]
    # x = y * transformed_pov_point[0] / fc[0]

    real_pov_point = x, y

    height = annotation_data.frame_size[0]

    p0 = lane_slope[1][0]
    p1 = lane_slope[1][1]

    y1 = int(height *0.6) # changed /2 to *0.75
    x1 = int((height *0.6 - p1) / p0)
    y2 = height
    x2 = int((height - p1) / p0)

    lane_points = [None] * 2
    transformed_lane_points = [None]*2
    real_lane_points = [None]*2




    lane_points[0] = x1, y1
    lane_points[1] = x2, y2

    for i2 in range(2):
        # transformed_lane_points[i2] = homo_trans(H, lane_points[i2], image_center)
        transformed_lane_points[i2] = my_warp_perspective(lane_points[i2], H)
        x, y, z = from2d23d(transformed_lane_points[i2], image_center)

        # z = -cam_height
        # y = fc[1] * z / transformed_lane_points[i2][1]
        # x = y * transformed_lane_points[i2][0] / fc[0]

        real_lane_points[i2] = x, y, z

    # annotation_data.real_lane_points[i] = real_lane_points[0][0:2], real_lane_points[1][0:2]

    a, b = np.polyfit((real_lane_points[0][0], real_lane_points[1][0]), (real_lane_points[0][1], real_lane_points[1][1]), 1)

    lat_distance = (a*real_pov_point[0] - real_pov_point[1] + b)/math.sqrt(a*a + 1)

    print('pov to lane: ', lat_distance)
    print(1)


def get_3d_box(pov_heading, pov_placement, H, image_center, annotation_data, frame_i):
    # transform vehicle box to real coords
    corners = [None]*4
    transformed_corners = [None]*4
    real_corners = [None]*4
    real_extruded_corners = [None]*4
    transformed_extruded_corners = [None]*4
    extruded_corners = [None]*4

    corners[0] = pov_placement[0], pov_placement[1]
    corners[1] = pov_placement[0] + pov_placement[2], pov_placement[1]
    corners[2] = pov_placement[0], pov_placement[1]+pov_placement[3]
    corners[3] = pov_placement[0] + pov_placement[2], pov_placement[1] + pov_placement[3]


    for i in reversed(range(4)):
        # transformed_corners[i] = homo_trans(H, corners[i], image_center)

        transformed_corners[i] = my_warp_perspective(corners[i], H)
        transformed_corners[i] = transformed_corners[i][0] - image_center[0], - transformed_corners[i][1] + image_center[1]

        if i < 2:
            #z = -cam_height + pov_height
            y = real_corners[i+2][1] #fc[1] * z / transformed_corners[i][1]
            x = y * transformed_corners[i][0] / fc[0]
            z = y * transformed_corners[i][1] / fc[1]
        else:
            z = -cam_height
            y = fc[1] * z / transformed_corners[i][1]
            x = y * transformed_corners[i][0] / fc[0]

        real_corners[i] = x, y, z

        real_extruded_corners[i] = real_corners[i][0] - pov_length * math.sin(pov_heading), \
                                   real_corners[i][1] + pov_length * math.cos(pov_heading), \
                                   real_corners[i][2]

        ze = real_extruded_corners[i][2]
        ye = fc[1] * ze / real_extruded_corners[i][1]
        xe = real_extruded_corners[i][0] * fc[0] / real_extruded_corners[i][1]

        transformed_extruded_corners[i] = xe, ye

        # extruded_corners[i] = no_homo_trans(H, transformed_extruded_corners[i], image_center)

        # a = np.array([[transformed_extruded_corners[i][0], transformed_extruded_corners[i][1]]], 'float32')
        # H_nparray = np.array(np.linalg.inv(H), 'float32')
        # a = np.array([a])
        #
        # test_val = cv2.perspectiveTransform(a, H_nparray)[0][0]
        transformed_extruded_corners[i] = transformed_extruded_corners[i][0] + image_center[0], image_center[1] - transformed_extruded_corners[i][1]
        extruded_corners[i] = my_inv_warp_perspective(transformed_extruded_corners[i], H)

        # extruded_corners[i] = transformed_extruded_corners[i]
    print('homo y:', real_corners[2][1])
    print('homo x:', real_corners[2][0])
    homo_y = real_corners[2][1]

    annotation_data.pov_rear_YX[frame_i] = real_corners[2], real_corners[3]
    annotation_data.pov_front_YX[frame_i] = real_extruded_corners[2], real_extruded_corners[3]
    # annotation_data.pov_distancem2[i] = real_corners[2][1]

    # b_x = int(extruded_corners[0][0])
    # b_y = int(extruded_corners[0][1])
    b_x = int(extruded_corners[0][0]) #+ image_center[0]
    b_y = int(extruded_corners[0][1]) #+ image_center[1]
    b_ix = int(extruded_corners[1][0] - extruded_corners[0][0])
    b_iy = int(extruded_corners[2][1] - extruded_corners[0][1])
    extruded_box = b_x, b_y, b_ix, b_iy

    return extruded_box, homo_y

def my_warp_perspective(img_point, H): # input tuple
    a = np.array([[img_point[0], img_point[1]]], 'float32')
    H_nparray = np.array(H, 'float32')
    a = np.array([a])
    test_val = cv2.perspectiveTransform(a, H_nparray)[0][0]
    return test_val[0], test_val[1]

def my_inv_warp_perspective(img_point, H): # input tuple
    a = np.array([[img_point[0], img_point[1]]], 'float32')
    H_nparray = np.array(np.linalg.inv(H), 'float32')
    a = np.array([a])
    test_val = cv2.perspectiveTransform(a, H_nparray)[0][0]
    return test_val[0], test_val[1]


def homo_trans(H, image_coords, image_center):
    # x_center = image_coords[0] - image_center[0]
    # y_center = - image_coords[1] + image_center[1]

    x_center = image_coords[0]
    y_center = image_coords[1]

    [[l_x], [l_y], [l]] = np.matmul(H, [[x_center], [y_center], [1]])
    x_homo = l_x / l
    y_homo = l_y / l

    # x_homo = x_center # for removing homography
    # y_homo = y_center # remove homo

    return x_homo, y_homo
    # return x_center, y_center


def no_homo_trans(H, coord, image_center):
    H_inv = np.linalg.inv(H)

    [[x_l], [y_l], [l_inv]] = np.matmul(H_inv, [[coord[0]], [coord[1]], [1]])
    x_center = x_l / l_inv
    y_center = y_l / l_inv

    # x_center = coord[0] # remove
    # y_center = coord[1] # remove

    x = x_center + image_center[0]
    y = image_center[1] - y_center
    x = x_center
    y = y_center

    return x, y

def from2d23d(warped_point, image_center):
    x, y = warped_point[0] - image_center[0], - warped_point[1] + image_center[1]

    z3d = -cam_height
    y3d = fc[1] * z3d / y/scale ######################################################################
    x3d = y3d * x / fc[0]/scale ######################################################################

    return x3d, y3d, z3d


def get_R(cam_pitch, cam_yaw):

    R_x = np.array([[1, 0, 0],
                    [0, math.cos(cam_pitch), -math.sin(cam_pitch)],
                    [0, math.sin(cam_pitch), math.cos(cam_pitch)]
                    ])

    # R_y = np.array([[math.cos(theta[1]), 0, math.sin(theta[1])],
    #                 [0, 1, 0],
    #                 [-math.sin(theta[1]), 0, math.cos(theta[1])]
    #                 ])

    R_z = np.array([[math.cos(cam_yaw), -math.sin(cam_yaw), 0],
                    [math.sin(cam_yaw), math.cos(cam_yaw), 0],
                    [0, 0, 1]
                    ])

    R_dot = np.dot(R_x, R_z)

    return R_dot