import numpy as np
import math
import cv2

fc = [347.1960, 352.3415]  # Focal length
cc = [241.5788, 188.9012]

# fc = [332.1207, 339.3542]  # Focal length
# cc = [245.2702, 189.3728]

kc = [-0.423287, 0.183867, -0.038207, 0.000657, 0.000187]  # Distortion (radial, decentering, and thin-prism, if any)



cam_height = 1.5
pov_height = 1.7
pov_length = 4.5

Green = (0, 255, 0)
Blue = (255, 0, 0)
Red = (0, 0, 255)


def rectify(src):
    h,w,_ = src.shape
    A = np.array([[fc[0], 0, cc[0]], [0, fc[1], cc[1]], [0, 0, 1]])
    distCoeffs = np.array([kc[0], kc[1], kc[2], kc[3], kc[4]])

    newcammtx,validROI = cv2.getOptimalNewCameraMatrix(A, distCoeffs,(w,h),1,(w,h))
    dst = cv2.undistort(src, A, distCoeffs, newCameraMatrix=newcammtx)
    dst = dst[validROI[1]:validROI[1]+validROI[3],0:w]
    scale_w = w/validROI[2]
    scale_h = h/validROI[3]
    h_scaled = int(round(scale_h*h))
    w_scaled = int(round(scale_w*w))
    # dst = cv2.resize(dst, (w_scaled, h_scaled))
    dst = ResizeWithAspectRatio(dst, width=w_scaled)
    # cv2.rectangle(dst,(validROI[0],validROI[1]),(validROI[2],validROI[3]),(255, 0, 0),1)
    # dst = cv2.resize(dst, (w*scale,h*scale)) ######################################################################
    return dst


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    return cv2.resize(image, dim, interpolation=inter)


def get_distance(vehicel_place, sv_hood_length, pov_width, pov_heading, image_center):
    a = (vehicel_place[0] - image_center[0])  # x position of right corner od the pov from center of image
    b = (vehicel_place[0] + vehicel_place[2] - image_center[0])  # x position of left corner of the pov from center of image
    if not np.isnan(pov_heading):
        vehicle_pixel_width = vehicel_place[2] / math.cos(pov_heading)
        longdistanceH = pov_width * fc[0] / vehicle_pixel_width #vehicel_place[2] # replace vehicle_place[2] by vehicle_pixel_width
    else:
        longdistanceH = pov_width * fc[0] / vehicel_place[2]


    if a == -b:  # b-a != 0:
        latdistanceH = 0
    else:
        latdistanceH = (pov_width / 2) * ((a+b)/(b-a))
    longdistanceH = longdistanceH - sv_hood_length
    # xx = distanceH * distanceH - cam_height * cam_height
    # distance = np.sqrt(xx)
    # print('pixel distance: ', distance)
    return longdistanceH, latdistanceH


def calculate_vp_and_homography(annotation_data, i): #used for lane markings
    # using the interpolated lane points
    lane_slope_points_left = annotation_data.lane_slope_points_left[i]
    lane_slope_points_right = annotation_data.lane_slope_points_right[i]
    lane_slope_points_left_o = annotation_data.lane_slope_points_left_o[i]
    lane_slope_points_right_o = annotation_data.lane_slope_points_right_o[i]

    x11 = lane_slope_points_left[0]
    y11 = lane_slope_points_left[1]
    x12 = lane_slope_points_left[2]
    y12 = lane_slope_points_left[3]
    x11_o = lane_slope_points_left_o[0]
    y11_o = lane_slope_points_left_o[1]
    x12_o = lane_slope_points_left_o[2]
    y12_o = lane_slope_points_left_o[3]

    m1 = (y11 - y12) / (x11 - x12)
    b1 = y11 - x11 * (y11 - y12) / (x11 - x12)
    m1_o = (y11_o - y12_o) / (x11_o - x12_o)
    b1_o = y11_o - x11_o * (y11_o - y12_o) / (x11_o - x12_o)

    x21 = lane_slope_points_right[0]
    y21 = lane_slope_points_right[1]
    x22 = lane_slope_points_right[2]
    y22 = lane_slope_points_right[3]
    x21_o = lane_slope_points_right_o[0]
    y21_o = lane_slope_points_right_o[1]
    x22_o = lane_slope_points_right_o[2]
    y22_o = lane_slope_points_right_o[3]

    m2 = (y21 - y22) / (x21 - x22)
    b2 = y21 - x21 * (y21 - y22) / (x21 - x22)
    m2_o = (y21_o - y22_o) / (x21_o - x22_o)
    b2_o = y21_o - x21_o * (y21_o - y22_o) / (x21_o - x22_o)

    xv = (b2 - b1) / (m1 - m2)
    xv_o = (b2_o - b1_o) / (m1_o - m2_o)

    yv = m1 * xv + b1
    yv_o = m1_o * xv_o + b1_o

    vp = int(round(xv)), int(round(yv))
    annotation_data.lanes_vp[i] = vp
    vp_o = int(round(xv_o)), int(round(yv_o))
    annotation_data.lanes_vp_o[i] = vp_o

    x1_L = vp[0]-5
    y1_L = int(round(annotation_data.lane_slope_left[i][1][0]*x1_L + annotation_data.lane_slope_left[i][1][1]))
    x1_L_o= vp_o[0] - 5
    y1_L_o = int(round(annotation_data.lane_slope_left_o[i][1][0] * x1_L_o + annotation_data.lane_slope_left_o[i][1][1]))
    x1_R = vp[0]+5
    y1_R = int(round(annotation_data.lane_slope_right[i][1][0]*x1_R + annotation_data.lane_slope_right[i][1][1]))
    x1_R_o = vp_o[0] + 5
    y1_R_o = int(round(annotation_data.lane_slope_right_o[i][1][0] * x1_R_o + annotation_data.lane_slope_right_o[i][1][1]))

    annotation_data.lane_slope_points_left[i] = x1_L, y1_L, int(round(x12)), int(round(y12))
    annotation_data.lane_slope_points_right[i] = x1_R, y1_R, int(round(x22)), int(round(y22))
    annotation_data.lane_slope_points_left_o[i] = x1_L_o, y1_L_o, int(round(x12_o)), int(round(y12_o))
    annotation_data.lane_slope_points_right_o[i] = x1_R_o, y1_R_o, int(round(x22_o)), int(round(y22_o))

    frame_size = annotation_data.frame_size
    image_center = annotation_data.image_center
    frame_size_o = annotation_data.frame_size_o
    image_center_o = annotation_data.image_center_o
    cam_yaw = -(-vp[0] + image_center[0]) / fc[0]
    cam_pitch = -(-vp[1] + image_center[1]) / fc[1]
    cam_yaw_o = -(-vp_o[0] + image_center_o[0]) / fc[0]
    cam_pitch_o= -(-vp_o[1] + image_center_o[1]) / fc[1]


    H = [[1, 0, -fc[0] * cam_yaw],  ######## last trial
         [0, 1, fc[1] * cam_pitch],
         [cam_yaw / fc[0], -cam_pitch / fc[1], 1]]

    H_o = [[1, 0, -fc[0] * cam_yaw_o],  ######## last trial
         [0, 1, fc[1] * cam_pitch_o],
         [cam_yaw_o / fc[0], -cam_pitch_o / fc[1], 1]]

    RR = [[1, 0, 0],
          [0, 1, 0],
          [0, 0, 1]]

    annotation_data.lane_points_YX_left[i] = transform_lane_3d(annotation_data.lane_slope_points_left[i], H, image_center)
    annotation_data.lane_points_YX_right[i] = transform_lane_3d(annotation_data.lane_slope_points_right[i], H, image_center)
    annotation_data.lane_points_YX_left_o[i] = transform_lane_3d(
        annotation_data.lane_slope_points_left_o[i], H_o, image_center_o)
    annotation_data.lane_points_YX_right_o[i] = transform_lane_3d(
        annotation_data.lane_slope_points_right_o[i], H_o, image_center_o)
    return H, H_o


def calculate_pov_heading(annotation_data,  i,  H, H_o):
    vp = annotation_data.lanes_vp[i] #vanishing point needed for calculate
    vp_o = annotation_data.lanes_vp_o[i]
    wheel_points = annotation_data.pov_wheels[i][1]
    wheel_points_o = annotation_data.pov_wheels_o[i][1]
    frame_size = annotation_data.frame_size
    image_center = annotation_data.image_center
    frame_size_o = annotation_data.frame_size_o
    image_center_o = int(round(frame_size[1] / 4)), int(round(frame_size[0] / 4)) #### CHECK IMAGECENTER
    vp_H = homo_trans(H, vp, image_center)
    vp_H_o = homo_trans(H_o, vp_o, image_center_o)
    vp_H = int(round(vp_H[0])), int(round(vp_H[1]))
    vp_H = vp_H[0] + image_center[0], vp_H[1] + image_center[1]
    vp_H_o = int(round(vp_H_o[0])), int(round(vp_H_o[1]))
    vp_H_o = vp_H_o[0] + image_center_o[0], vp_H_o[1] + image_center_o[1]

    wheel_1_x, wheel_1_y = homo_trans(H, wheel_points[0], image_center)
    x3d_wheel_1, y3d_wheel_1, z3d_wheel_1 = from2d23d((wheel_1_x, wheel_1_y), image_center)
    wheel_1_x_o, wheel_1_y_o = homo_trans(H_o, wheel_points_o[0], image_center_o)
    x3d_wheel_1_o, y3d_wheel_1_o, z3d_wheel_1_o = from2d23d((wheel_1_x_o, wheel_1_y_o), image_center_o)
    wheel_2_x, wheel_2_y = homo_trans(H, wheel_points[1], image_center)
    x3d_wheel_2, y3d_wheel_2, z3d_wheel_2 = from2d23d((wheel_2_x, wheel_2_y), image_center)
    wheel_2_x_o, wheel_2_y_o = homo_trans(H_o, wheel_points_o[1], image_center_o)
    x3d_wheel_2_o, y3d_wheel_2_o, z3d_wheel_2_o = from2d23d((wheel_2_x_o, wheel_2_y_o), image_center_o)

    annotation_data.pov_wheels_YX[i] = (x3d_wheel_1, y3d_wheel_1), (x3d_wheel_2, y3d_wheel_2)
    annotation_data.pov_wheels_YX_o[i] = (x3d_wheel_1_o, y3d_wheel_1_o), (x3d_wheel_2_o, y3d_wheel_2_o)

    X = x3d_wheel_2 - x3d_wheel_1
    Y = y3d_wheel_2 - y3d_wheel_1
    X_o = x3d_wheel_2_o - x3d_wheel_1_o
    Y_o = y3d_wheel_2_o - y3d_wheel_1_o
    pov_heading = -math.atan(X / Y)
    pov_heading_o = -math.atan(X_o / Y_o)
    annotation_data.pov_heading[i] = pov_heading
    annotation_data.pov_heading_o[i] = pov_heading_o

    return


def calculate_sv_heading(annotation_data, annotation_data_sv, i, video, H, H_o):
    img = video[i].copy()
    vp = annotation_data.lanes_vp[i] #vanishing point needed for calculate
    vp_o = annotation_data.lanes_vp_o[i]
    wheel_points_sv = annotation_data_sv.sv_wheels[i][1]
    wheel_points_sv_o = annotation_data_sv.sv_wheels_o[i][1]
    frame_size = annotation_data.frame_size
    image_center = annotation_data.image_center
    frame_size_o = annotation_data.frame_size_o
    image_center_o = int(round(frame_size[1] / 4)), int(round(frame_size[0] / 4)) #### CHECK IMAGECENTER
    vp_H = homo_trans(H, vp, image_center)
    vp_H_o = homo_trans(H_o, vp_o, image_center_o)
    vp_H = int(round(vp_H[0])), int(round(vp_H[1]))
    vp_H = vp_H[0] + image_center[0], vp_H[1] + image_center[1]
    vp_H_o = int(round(vp_H_o[0])), int(round(vp_H_o[1]))
    vp_H_o = vp_H_o[0] + image_center_o[0], vp_H_o[1] + image_center_o[1]

    wheel_1_x_sv, wheel_1_y_sv = homo_trans(H, wheel_points_sv[0], image_center)
    x3d_wheel_1_sv, y3d_wheel_1_sv, z3d_wheel_1_sv = from2d23d((wheel_1_x_sv, wheel_1_y_sv), image_center)
    wheel_1_x_sv_o, wheel_1_y_sv_o = homo_trans(H_o, wheel_points_sv_o[0], image_center_o)
    x3d_wheel_1_sv_o, y3d_wheel_1_sv_o, z3d_wheel_1_sv_o = from2d23d((wheel_1_x_sv_o, wheel_1_y_sv_o), image_center_o)
    wheel_2_x_sv, wheel_2_y_sv = homo_trans(H, wheel_points_sv[1], image_center)
    x3d_wheel_2_sv, y3d_wheel_2_sv, z3d_wheel_2_sv = from2d23d((wheel_2_x_sv, wheel_2_y_sv), image_center)
    wheel_2_x_sv_o, wheel_2_y_sv_o = homo_trans(H_o, wheel_points_sv_o[1], image_center_o)
    x3d_wheel_2_sv_o, y3d_wheel_2_sv_o, z3d_wheel_2_sv_o = from2d23d((wheel_2_x_sv_o, wheel_2_y_sv_o), image_center_o)
    annotation_data_sv.sv_wheels_YX[i] = (x3d_wheel_1_sv, y3d_wheel_1_sv), (x3d_wheel_2_sv, y3d_wheel_2_sv)
    annotation_data_sv.sv_wheels_YX_o[i] = (x3d_wheel_1_sv_o, y3d_wheel_1_sv_o), (x3d_wheel_2_sv_o, y3d_wheel_2_sv_o)

    X_sv = x3d_wheel_2_sv - x3d_wheel_1_sv
    Y_sv = y3d_wheel_2_sv - y3d_wheel_1_sv
    X_sv_o = x3d_wheel_2_sv_o - x3d_wheel_1_sv_o
    Y_sv_o = y3d_wheel_2_sv_o - y3d_wheel_1_sv_o
    sv_heading = -math.atan(X_sv / Y_sv)
    sv_heading_o = -math.atan(X_sv_o / Y_sv_o)
    annotation_data_sv.sv_heading[i] = sv_heading
    annotation_data_sv.sv_heading_o[i] = sv_heading_o

    return


def calculate_adj_heading(annotation_data, annotation_data_adj, i, video, H, H_o):
    img = video[i].copy()
    vp = annotation_data.lanes_vp[i] #vanishing point needed for calculate
    vp_o = annotation_data.lanes_vp_o[i]
    wheel_points_adj = annotation_dataadj.adj_wheels[i][1]
    wheel_points_adj_o = annotation_data_adj.adj_wheels_o[i][1]
    frame_size = annotation_data.frame_size
    image_center = annotation_data.image_center
    frame_size_o = annotation_data.frame_size_o
    image_center_o = int(round(frame_size[1] / 4)), int(round(frame_size[0] / 4)) #### CHECK IMAGECENTER
    vp_H = homo_trans(H, vp, image_center)
    vp_H_o = homo_trans(H_o, vp_o, image_center_o)
    vp_H = int(round(vp_H[0])), int(round(vp_H[1]))
    vp_H = vp_H[0] + image_center[0], vp_H[1] + image_center[1]
    vp_H_o = int(round(vp_H_o[0])), int(round(vp_H_o[1]))
    vp_H_o = vp_H_o[0] + image_center_o[0], vp_H_o[1] + image_center_o[1]


    wheel_2_x_adj, wheel_2_y_adj = homo_trans(H, wheel_points_adj[1], image_center)
    x3d_wheel_2_adj, y3d_wheel_2_adj, z3d_wheel_2_adj = from2d23d((wheel_2_x_adj, wheel_2_y_adj), image_center)
    wheel_2_x_adj_o, wheel_2_y_adj_o = homo_trans(H_o, wheel_points_adj_o[1], image_center_o)
    x3d_wheel_2_adj_o, y3d_wheel_2_adj_o, z3d_wheel_2_adj_o = from2d23d((wheel_2_x_adj_o, wheel_2_y_adj_o), image_center_o)
    wheel_2_x_adj, wheel_2_y_adj = homo_trans(H, wheel_points_adj[1], image_center)
    x3d_wheel_2_adj, y3d_wheel_2_adj, z3d_wheel_2_adj = from2d23d((wheel_2_x_adj, wheel_2_y_adj), image_center)
    wheel_2_x_adj_o, wheel_2_y_adj_o = homo_trans(H_o, wheel_points_adj_o[1], image_center_o)
    x3d_wheel_2_adj_o, y3d_wheel_2_adj_o, z3d_wheel_2_adj_o = from2d23d((wheel_2_x_adj_o, wheel_2_y_adj_o), image_center_o)

    annotation_data_adj.adj_wheels_YX[i] = (x3d_wheel_1_adj, y3d_wheel_1_adj), (x3d_wheel_2_adj, y3d_wheel_2_adj)
    annotation_data_adj.adj_wheels_YX_o[i] = (x3d_wheel_1_adj_o, y3d_wheel_1_adj_o), (x3d_wheel_2_adj_o, y3d_wheel_2_adj_o)

    X_adj = x3d_wheel_2_adj - x3d_wheel_1_adj
    Y_adj = y3d_wheel_2_adj - y3d_wheel_1_adj
    X_adj_o = x3d_wheel_2_adj_o - x3d_wheel_1_adj_o
    Y_adj_o = y3d_wheel_2_adj_o - y3d_wheel_1_adj_o
    adj_heading = -math.atan(X_adj / Y_adj)
    adj_heading_o = -math.atan(X_adj_o / Y_adj_o)
    annotation_data_adj.adj_heading[i] = adj_heading
    annotation_data_adj.adj_heading_o[i] = adj_heading_o

    return


def transform_pov_to3D(annotation_data, i, H, H_o):
    # frame_size = img.shape
    pov_placement = annotation_data.pov_placement[i][1]
    pov_heading = annotation_data.pov_heading[i]
    #pov_placement_o = annotation_data.pov_placement_o[i][1]
    #pov_heading_o = annotation_data.pov_heading_o[i]

    frame_size = annotation_data.frame_size
    image_center = int(round(frame_size[1] / 2)), int(round(frame_size[0] / 2))
    frame_size_o = annotation_data.frame_size_o
    image_center_o = int(round(frame_size[1] / 4)), int(round(frame_size[0] / 4))

    extruded_box, y_homo = get_3d_box(pov_heading, pov_placement, H, image_center, annotation_data, i)
    #extruded_box_o, y_homo_o = get_3d_box_o(pov_heading_o, pov_placement_o, H_o, image_center_o, annotation_data, i)
    annotation_data.pov_distance_long_H[i] = y_homo
    #annotation_data.pov_distance_long_H_o[i] = y_homo_o

    annotation_data.pov_extruded_box[i] = extruded_box
    #annotation_data.pov_extruded_box_o[i] = extruded_box_o

    latdistance_pov_to_lane(annotation_data, i, H, H_o, image_center, image_center_o)

    return pov_heading, extruded_box


def transform_pov_to3D_sv(annotation_data_sv, i, H, H_o):
    # frame_size = img.shape
    sv_placement = annotation_data_sv.sv_placement[i][1]
    sv_heading = annotation_data_sv.sv_heading[i]
    #pov_placement_o = annotation_data.pov_placement_o[i][1]
    #pov_heading_o = annotation_data.pov_heading_o[i]

    frame_size = annotation_data_sv.frame_size
    image_center = int(round(frame_size[1] / 2)), int(round(frame_size[0] / 2))
    #frame_size_o = annotation_data.frame_size_o
    #image_center_o = int(round(frame_size[1] / 4)), int(round(frame_size[0] / 4))

    extruded_box, y_homo = get_3d_box(sv_heading, sv_placement, H, image_center, annotation_data_sv, i)
    #extruded_box_o, y_homo_o = get_3d_box_o(pov_heading_o, pov_placement_o, H_o, image_center_o, annotation_data, i)
    annotation_data_sv.sv_distance_long_H[i] = y_homo
    #annotation_data.pov_distance_long_H_o[i] = y_homo_o

    annotation_data_sv.sv_extruded_box[i] = extruded_box
    #annotation_data.pov_extruded_box_o[i] = extruded_box_o

    latdistance_pov_to_lane(annotation_data_sv, i, H, H_o, image_center, image_center_o)

    return sv_heading, extruded_box


def transform_pov_to3D_adj(annotation_data_adj, i, H, H_o):
    # frame_size = img.shape
    adj_placement = annotation_data_adj.adj_placement[i][1]
    adj_heading = annotation_data_adj.adj_heading[i]
    #pov_placement_o = annotation_data.pov_placement_o[i][1]
    #pov_heading_o = annotation_data.pov_heading_o[i]

    frame_size = annotation_data_adj.frame_size
    image_center = int(round(frame_size[1] / 2)), int(round(frame_size[0] / 2))
    #frame_size_o = annotation_data.frame_size_o
    #image_center_o = int(round(frame_size[1] / 4)), int(round(frame_size[0] / 4))

    extruded_box, y_homo = get_3d_box(adj_heading, adj_placement, H, image_center, annotation_data_adj, i)
    #extruded_box_o, y_homo_o = get_3d_box_o(pov_heading_o, pov_placement_o, H_o, image_center_o, annotation_data, i)
    annotation_data_adj.adj_distance_long_H[i] = y_homo
    #annotation_data.pov_distance_long_H_o[i] = y_homo_o

    annotation_data_adj.adj_extruded_box[i] = extruded_box
    #annotation_data.pov_extruded_box_o[i] = extruded_box_o

    latdistance_pov_to_lane(annotation_data_adj, i, H, H_o, image_center, image_center_o)

    return adj_heading, extruded_box



def transform_sv_to3D(annotation_data_sv, i, H, H_o):
    # frame_size = img.shape
    sv_placement = annotation_data_sv.sv_placement[i][1]
    sv_heading = annotation_data_sv.sv_heading[i]
    sv_placement_o = annotation_data_sv.sv_placement_o[i][1]
    sv_heading_o = annotation_data_sv.sv_heading_o[i]

    frame_size = annotation_data_sv.frame_size
    image_center = int(round(frame_size[1] / 2)), int(round(frame_size[0] / 2))
    frame_size_o = annotation_data_sv.frame_size_o
    image_center_o = int(round(frame_size[1] / 4)), int(round(frame_size[0] / 4))

    extruded_box, y_homo = get_3d_box(sv_heading, sv_placement, H, image_center, annotation_data_sv, i)
    extruded_box_o, y_homo_o = get_3d_box_o(sv_heading_o, sv_placement_o, H_o, image_center_o, annotation_data_sv, i)
    annotation_data_sv.sv_distance_long_H[i] = y_homo
    annotation_data_sv.sv_distance_long_H_o[i] = y_homo_o

    annotation_data_sv.sv_extruded_box[i] = extruded_box
    annotation_data_sv.sv_extruded_box_o[i] = extruded_box_o

    latdistance_pov_to_lane(annotation_data_sv, i, H, H_o, image_center, image_center_o)

    return pov_heading, extruded_box, pov_heading_o, extruded_box_o


def transform_lane_3d(lane_slope_points, H, image_center):
    x1 = lane_slope_points[0]
    y1 = lane_slope_points[1]
    x2 = lane_slope_points[2]
    y2 = lane_slope_points[3]

    lane_points = [None] * 2
    transformed_lane_points = [None] * 2
    real_lane_points = [None] * 2

    lane_points[0] = x1, y1
    lane_points[1] = x2, y2

    for i2 in range(2):
        transformed_lane_points[i2] = homo_trans(H, lane_points[i2], image_center)
        x,y,z = from2d23d(transformed_lane_points[i2], image_center)

        real_lane_points[i2] = x, y, z

    return real_lane_points[0][0:2], real_lane_points[1][0:2]


def latdistance_pov_to_lane(annotation_data, i, H, H_o, image_center, image_center_o):

    pov_placement = annotation_data.pov_placement[i][1]
    lane_slope_left = annotation_data.lane_slope_left[i]
    lane_slope_right = annotation_data.lane_slope_right[i]
    extruded_box = annotation_data.pov_extruded_box[i]
    pov_placement_o = annotation_data.pov_placement_o[i][1]
    lane_slope_left_o = annotation_data.lane_slope_left_o[i]
    lane_slope_right_o = annotation_data.lane_slope_right_o[i]
    extruded_box_o = annotation_data.pov_extruded_box_o[i]
    # determine if the pov is left or right of the sv
    center_line_image_x = annotation_data.frame_size[1]/2
    center_line_image_x_o = annotation_data.frame_size[1]/4


    if center_line_image_x < pov_placement[0]: # the pov is on the right
        lane_slope = lane_slope_right
        pov_point_rear = pov_placement[0], pov_placement[1] + pov_placement[3]
        pov_point_front = extruded_box[0], extruded_box[1] + extruded_box[3]
    else:
        lane_slope = lane_slope_left
        pov_point_rear = pov_placement[0] + pov_placement[2], pov_placement[1] + pov_placement[3]
        pov_point_front = extruded_box[0] + extruded_box[2], extruded_box[1] + extruded_box[3]

    if center_line_image_x_o < pov_placement_o[0]: # the pov is on the right
        lane_slope_o = lane_slope_right_o
        pov_point_rear_o = pov_placement_o[0], pov_placement_o[1] + pov_placement_o[3]
        pov_point_front_o = extruded_box_o[0], extruded_box_o[1] + extruded_box_o[3]
    else:
        lane_slope_o = lane_slope_left_o
        pov_point_rear_o = pov_placement_o[0] + pov_placement_o[2], pov_placement_o[1] + pov_placement_o[3]
        pov_point_front_o = extruded_box_o[0] + extruded_box_o[2], extruded_box_o[1] + extruded_box_o[3]

    transformed_pov_point_front = homo_trans(H, pov_point_front, image_center)
    transformed_pov_point_front_o = homo_trans(H_o, pov_point_front_o, image_center_o)
    x, y, z = from2d23d(transformed_pov_point_front, image_center)
    x_o, y_o, z_o = from2d23d(transformed_pov_point_front_o, image_center_o)

    annotation_data.pov_distance_lat_H_front[i] = x_o
    annotation_data.pov_distance_lat_H_front_o[i] = x_o
    transformed_pov_point_rear = homo_trans(H, pov_point_rear, image_center)
    transformed_pov_point_rear_o = homo_trans(H_o, pov_point_rear_o, image_center_o)
    x, y, z = from2d23d(transformed_pov_point_rear, image_center)
    x_o, y_o, z_o = from2d23d(transformed_pov_point_rear_o, image_center_o)
    annotation_data.pov_distance_lat_H_rear[i] = x_o
    annotation_data.pov_distance_lat_H_rear_o[i] = x_o


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
        transformed_corners[i] = homo_trans(H, corners[i], image_center)

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

        extruded_corners[i] = no_homo_trans(H, transformed_extruded_corners[i], image_center)

    homo_y = real_corners[2][1]

    annotation_data.pov_rear_YX[frame_i] = real_corners[2], real_corners[3]
    annotation_data.pov_front_YX[frame_i] = real_extruded_corners[2], real_extruded_corners[3]

    b_x = int(extruded_corners[0][0]) #+ image_center[0]
    b_y = int(extruded_corners[0][1]) #+ image_center[1]
    b_ix = int(extruded_corners[1][0] - extruded_corners[0][0])
    b_iy = int(extruded_corners[2][1] - extruded_corners[0][1])
    extruded_box = b_x, b_y, b_ix, b_iy

    return extruded_box, homo_y


def get_3d_box_sv(sv_heading, sv_placement, H, image_center, annotation_data_sv, frame_i):
    # transform vehicle box to real coords
    corners = [None]*4
    transformed_corners = [None]*4
    real_corners = [None]*4
    real_extruded_corners = [None]*4
    transformed_extruded_corners = [None]*4
    extruded_corners = [None]*4

    corners[0] = sv_placement[0], sv_placement[1]
    corners[1] = sv_placement[0] + sv_placement[2], sv_placement[1]
    corners[2] = sv_placement[0], sv_placement[1] + sv_placement[3]
    corners[3] = sv_placement[0] + sv_placement[2], sv_placement[1] + sv_placement[3]

    for i in reversed(range(4)):
        transformed_corners[i] = homo_trans(H, corners[i], image_center)

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

        extruded_corners[i] = no_homo_trans(H, transformed_extruded_corners[i], image_center)

    homo_y = real_corners[2][1]

    annotation_data_sv.sv_rear_YX[frame_i] = real_corners[2], real_corners[3]
    annotation_data_sv.sv_front_YX[frame_i] = real_extruded_corners[2], real_extruded_corners[3]

    b_x = int(extruded_corners[0][0]) #+ image_center[0]
    b_y = int(extruded_corners[0][1]) #+ image_center[1]
    b_ix = int(extruded_corners[1][0] - extruded_corners[0][0])
    b_iy = int(extruded_corners[2][1] - extruded_corners[0][1])
    extruded_box = b_x, b_y, b_ix, b_iy

    return extruded_box, homo_y


#homographic transformation needed to get from image plane to real world
def homo_trans(H, image_coords, image_center):
    x_center = image_coords[0] - image_center[0]
    y_center = - image_coords[1] + image_center[1]
    [[l_x], [l_y], [l]] = np.matmul(H, [[x_center], [y_center], [1]])
    x_homo = l_x / l
    y_homo = l_y / l

    return x_homo, y_homo


#inverted homographic transformation to get from real world to image world
def no_homo_trans(H, coord, image_center):
    H_inv = np.linalg.inv(H)

    [[x_l], [y_l], [l_inv]] = np.matmul(H_inv, [[coord[0]], [coord[1]], [1]])
    x_center = x_l / l_inv
    y_center = y_l / l_inv

    x = x_center + image_center[0]
    y = image_center[1] - y_center

    return x, y

def from2d23d(warped_point, image_center):
    # x, y = warped_point[0] - image_center[0], - warped_point[1] + image_center[1]
    x, y = warped_point
    z3d = -cam_height
    y3d = fc[1] * z3d / y#/scale ######################################################################
    x3d = y3d * x / fc[0]#/scale ######################################################################

    return x3d, y3d, z3d
