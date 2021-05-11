import cv2
import numpy as np
from DrawFunctions import *


def interpolate_annotations(annotation_data):
    annotation_data.pov_placement, annotation_data.pov_placement_o = interpolate_pov_placement(annotation_data)
    annotation_data.lane_slope_left, annotation_data.lane_slope_points_left, annotation_data.lane_slope_left_o, \
    annotation_data.lane_slope_points_left_o = interpolate_lane_placement(annotation_data, lane_side='left')
    annotation_data.lane_slope_right, annotation_data.lane_slope_points_right, annotation_data.lane_slope_right_o, \
    annotation_data.lane_slope_points_right_o = interpolate_lane_placement(annotation_data, lane_side='right')


def interpolate_annotations_sv(annotation_data_sv):
    annotation_data_sv.sv_placement, annotation_data_sv.pov_placement_o = interpolate_sv_placement(annotation_data_sv)


def interpolate_annotations_adj(annotation_data_adj):
    annotation_data_adj.adj_placement, annotation_data_adj.adj_placement_o = interpolate_adj_placement(annotation_data_adj)


def interpolate_pov_placement(annotation_data):
    pov_placement = annotation_data.pov_placement
    pov_placement_itrp = pov_placement.copy()
    pov_placement_o = annotation_data.pov_placement_o
    pov_placement_itrp_o = pov_placement_o.copy()

    flags = np.array(get_pov_col(pov_placement, flags=True))
    user_input_i, = np.where(flags == 1)  # index for user inputs

    x_pos = np.array(get_pov_col(pov_placement, 0))
    y_pos = np.array(get_pov_col(pov_placement, 1))
    ix = np.array(get_pov_col(pov_placement, 2))
    iy = np.array(get_pov_col(pov_placement, 3))

    x_pos_o = np.array(get_pov_col(pov_placement_o, 0))
    y_pos_o = np.array(get_pov_col(pov_placement_o, 1))
    ix_o = np.array(get_pov_col(pov_placement_o, 2))
    iy_o = np.array(get_pov_col(pov_placement_o, 3))

    if user_input_i.size < 1:
        return pov_placement, pov_placement_o

    else:
        frames = np.linspace(0, flags.shape[0] - 1, flags.shape[0])
        x_pos_itrp = np.interp(frames, user_input_i, x_pos[user_input_i], left=np.nan, right=np.nan)
        y_pos_itrp = np.interp(frames, user_input_i, y_pos[user_input_i], left=np.nan, right=np.nan)
        ix_itrp = np.interp(frames, user_input_i, ix[user_input_i], left=np.nan, right=np.nan)
        iy_itrp = np.interp(frames, user_input_i, iy[user_input_i], left=np.nan, right=np.nan)
        x_pos_itrp_o = np.interp(frames, user_input_i, x_pos_o[user_input_i], left=np.nan, right=np.nan)
        y_pos_itrp_o = np.interp(frames, user_input_i, y_pos_o[user_input_i], left=np.nan, right=np.nan)
        ix_itrp_o = np.interp(frames, user_input_i, ix_o[user_input_i], left=np.nan, right=np.nan)
        iy_itrp_o = np.interp(frames, user_input_i, iy_o[user_input_i], left=np.nan, right=np.nan)

        for i in range(annotation_data.frame_count):
            if not np.isnan(x_pos_itrp[i]):
                pov_placement_itrp[i] = flags[i], (int(round(x_pos_itrp[i])), int(round(y_pos_itrp[i]))
                                                   , int(round(ix_itrp[i])), int(round(iy_itrp[i])))
                pov_placement_itrp_o[i] = flags[i], (int(round(x_pos_itrp_o[i])), int(round(y_pos_itrp_o[i]))
                                                     , int(round(ix_itrp_o[i])), int(round(iy_itrp_o[i])))
            else:
                pov_placement_itrp[i] = flags[i], (x_pos_itrp[i], y_pos_itrp[i], ix_itrp[i], iy_itrp[i])
                pov_placement_itrp_o[i] = flags[i], (x_pos_itrp_o[i], y_pos_itrp_o[i], ix_itrp_o[i], iy_itrp_o[i])

        return pov_placement_itrp, pov_placement_itrp_o


def interpolate_sv_placement(annotation_data_sv):
    sv_placement = annotation_data_sv.sv_placement
    sv_placement_itrp = sv_placement.copy()
    sv_placement_o = annotation_data_sv.sv_placement_o
    sv_placement_itrp_o = sv_placement_o.copy()

    flags = np.array(get_pov_col(sv_placement, flags=True))
    user_input_i, = np.where(flags == 1)  # index for user inputs

    x_pos = np.array(get_pov_col(sv_placement, 0))
    y_pos = np.array(get_pov_col(sv_placement, 1))
    ix = np.array(get_pov_col(sv_placement, 2))
    iy = np.array(get_pov_col(sv_placement, 3))

    x_pos_o = np.array(get_pov_col(sv_placement_o, 0))
    y_pos_o = np.array(get_pov_col(sv_placement_o, 1))
    ix_o = np.array(get_pov_col(sv_placement_o, 2))
    iy_o = np.array(get_pov_col(sv_placement_o, 3))

    if user_input_i.size < 1:
        return sv_placement, sv_placement_o

    else:
        frames = np.linspace(0, flags.shape[0] - 1, flags.shape[0])
        x_pos_itrp = np.interp(frames, user_input_i, x_pos[user_input_i], left=np.nan, right=np.nan)
        y_pos_itrp = np.interp(frames, user_input_i, y_pos[user_input_i], left=np.nan, right=np.nan)
        ix_itrp = np.interp(frames, user_input_i, ix[user_input_i], left=np.nan, right=np.nan)
        iy_itrp = np.interp(frames, user_input_i, iy[user_input_i], left=np.nan, right=np.nan)
        x_pos_itrp_o = np.interp(frames, user_input_i, x_pos_o[user_input_i], left=np.nan, right=np.nan)
        y_pos_itrp_o = np.interp(frames, user_input_i, y_pos_o[user_input_i], left=np.nan, right=np.nan)
        ix_itrp_o = np.interp(frames, user_input_i, ix_o[user_input_i], left=np.nan, right=np.nan)
        iy_itrp_o = np.interp(frames, user_input_i, iy_o[user_input_i], left=np.nan, right=np.nan)

        for i in range(annotation_data_sv.frame_count):
            if not np.isnan(x_pos_itrp[i]):
                sv_placement_itrp[i] = flags[i], (int(round(x_pos_itrp[i])), int(round(y_pos_itrp[i]))
                                                   , int(round(ix_itrp[i])), int(round(iy_itrp[i])))
                sv_placement_itrp_o[i] = flags[i], (int(round(x_pos_itrp_o[i])), int(round(y_pos_itrp_o[i]))
                                                     , int(round(ix_itrp_o[i])), int(round(iy_itrp_o[i])))
            else:
                sv_placement_itrp[i] = flags[i], (x_pos_itrp[i], y_pos_itrp[i], ix_itrp[i], iy_itrp[i])
                sv_placement_itrp_o[i] = flags[i], (x_pos_itrp_o[i], y_pos_itrp_o[i], ix_itrp_o[i], iy_itrp_o[i])

        return sv_placement_itrp, sv_placement_itrp_o


def interpolate_adj_placement(annotation_data_adj):
    adj_placement = annotation_data_adj.adj_placement
    adj_placement_itrp = adj_placement.copy()
    adj_placement_o = annotation_data_adj.adj_placement_o
    adj_placement_itrp_o = adj_placement_o.copy()

    flags = np.array(get_pov_col(adj_placement, flags=True))
    user_input_i, = np.where(flags == 1)  # index for user inputs

    x_pos = np.array(get_pov_col(adj_placement, 0))
    y_pos = np.array(get_pov_col(adj_placement, 1))
    ix = np.array(get_pov_col(adj_placement, 2))
    iy = np.array(get_pov_col(adj_placement, 3))

    x_pos_o = np.array(get_pov_col(adj_placement_o, 0))
    y_pos_o = np.array(get_pov_col(adj_placement_o, 1))
    ix_o = np.array(get_pov_col(adj_placement_o, 2))
    iy_o = np.array(get_pov_col(adj_placement_o, 3))

    if user_input_i.size < 1:
        return adj_placement, adj_placement_o

    else:
        frames = np.linspace(0, flags.shape[0] - 1, flags.shape[0])
        x_pos_itrp = np.interp(frames, user_input_i, x_pos[user_input_i], left=np.nan, right=np.nan)
        y_pos_itrp = np.interp(frames, user_input_i, y_pos[user_input_i], left=np.nan, right=np.nan)
        ix_itrp = np.interp(frames, user_input_i, ix[user_input_i], left=np.nan, right=np.nan)
        iy_itrp = np.interp(frames, user_input_i, iy[user_input_i], left=np.nan, right=np.nan)
        x_pos_itrp_o = np.interp(frames, user_input_i, x_pos_o[user_input_i], left=np.nan, right=np.nan)
        y_pos_itrp_o = np.interp(frames, user_input_i, y_pos_o[user_input_i], left=np.nan, right=np.nan)
        ix_itrp_o = np.interp(frames, user_input_i, ix_o[user_input_i], left=np.nan, right=np.nan)
        iy_itrp_o = np.interp(frames, user_input_i, iy_o[user_input_i], left=np.nan, right=np.nan)

        for i in range(annotation_data_adj.frame_count):
            if not np.isnan(x_pos_itrp[i]):
                adj_placement_itrp[i] = flags[i], (int(round(x_pos_itrp[i])), int(round(y_pos_itrp[i]))
                                                   , int(round(ix_itrp[i])), int(round(iy_itrp[i])))
                adj_placement_itrp_o[i] = flags[i], (int(round(x_pos_itrp_o[i])), int(round(y_pos_itrp_o[i]))
                                                     , int(round(ix_itrp_o[i])), int(round(iy_itrp_o[i])))
            else:
                adj_placement_itrp[i] = flags[i], (x_pos_itrp[i], y_pos_itrp[i], ix_itrp[i], iy_itrp[i])
                adj_placement_itrp_o[i] = flags[i], (x_pos_itrp_o[i], y_pos_itrp_o[i], ix_itrp_o[i], iy_itrp_o[i])

        return adj_placement_itrp, adj_placement_itrp_o

def interpolate_lane_placement(annotation_data, lane_side):
    if lane_side == 'left':
        lane_placement = annotation_data.lane_placement_left
        lane_slope = annotation_data.lane_slope_left
        lane_slope_points = annotation_data.lane_slope_points_left
        lane_placement_o = annotation_data.lane_placement_left_o
        lane_slope_o = annotation_data.lane_slope_left_o
        lane_slope_points_o = annotation_data.lane_slope_points_left_o

    elif lane_side == 'right':
        lane_placement = annotation_data.lane_placement_right
        lane_slope = annotation_data.lane_slope_right
        lane_slope_points = annotation_data.lane_slope_points_right
        lane_placement_o = annotation_data.lane_placement_right_o
        lane_slope_o = annotation_data.lane_slope_right_o
        lane_slope_points_o = annotation_data.lane_slope_points_right_o

    lane_slope_itrp = lane_slope.copy()
    lane_slope_points_itrp = lane_slope_points.copy()
    lane_slope_itrp_o = lane_slope_o.copy()
    lane_slope_points_itrp_o = lane_slope_points_o.copy()

    flags = np.array(get_pov_col(lane_placement, flags=True))
    user_input_i, = np.where(flags == 1)  # index for user inputs

    if user_input_i.size < 1:
        return lane_slope, lane_slope_points, lane_slope_o, lane_slope_points_o

    else:
        # save lane slope for each frame of user input
        for row in user_input_i:
            lane_placement_frame = lane_placement[row][1]
            x_pos = get_col(lane_placement_frame, 0)
            y_pos = get_col(lane_placement_frame, 1)
            p0, p1 = np.polyfit(x_pos, y_pos, 1)
            lane_slope[row] = 1, (p0, p1)
            lane_placement_frame_o = lane_placement_o[row][1]
            x_pos_o = get_col(lane_placement_frame_o, 0)
            y_pos_o = get_col(lane_placement_frame_o, 1)
            p0_o, p1_o = np.polyfit(x_pos_o, y_pos_o, 1)
            lane_slope_o[row] = 1, (p0_o, p1_o)


        frames = np.linspace(0, flags.shape[0] - 1, flags.shape[0])

        p0_list = np.array(get_pov_col(lane_slope, 0))
        p1_list = np.array(get_pov_col(lane_slope, 1))
        p0_list_o = np.array(get_pov_col(lane_slope_o, 0))
        p1_list_o = np.array(get_pov_col(lane_slope_o, 1))

        p0_itrp = np.interp(frames, user_input_i, p0_list[user_input_i], left=np.nan, right=np.nan)
        p1_itrp = np.interp(frames, user_input_i, p1_list[user_input_i], left=np.nan, right=np.nan)
        p0_itrp_o = np.interp(frames, user_input_i, p0_list_o[user_input_i], left=np.nan, right=np.nan)
        p1_itrp_o = np.interp(frames, user_input_i, p1_list_o[user_input_i], left=np.nan, right=np.nan)

        for i in range(flags.shape[0]):
            if not np.isnan(p0_itrp[i]):
                lane_slope_itrp[i] = flags[i], (p0_itrp[i], p1_itrp[i])
                p0 = p0_itrp[i]
                p1 = p1_itrp[i]
                y1 = int(round(annotation_data.height * 0.5))
                x1 = int(round((y1 - p1) / p0))
                y2 = annotation_data.height
                x2 = int(round((y2 - p1) / p0))
                lane_slope_points_itrp[i] = x1, y1, x2, y2

                lane_slope_itrp_o[i] = flags[i], (p0_itrp_o[i], p1_itrp_o[i])
                p0_o = p0_itrp_o[i]
                p1_o = p1_itrp_o[i]
                y1_o = int(round(annotation_data.height_o * 0.5))
                x1_o = int(round((y1_o - p1_o) / p0_o))
                y2_o = annotation_data.height_o
                x2_o = int(round((y2_o - p1_o) / p0_o))
                lane_slope_points_itrp_o[i] = x1_o, y1_o, x2_o, y2_o

            else:
                lane_slope_itrp[i] = 0, (np.nan, np.nan)
                lane_slope_points_itrp[i] = np.nan, np.nan, np.nan, np.nan
                lane_slope_itrp_o[i] = 0, (np.nan, np.nan)
                lane_slope_points_itrp_o[i] = np.nan, np.nan, np.nan, np.nan

        return lane_slope_itrp, lane_slope_points_itrp, lane_slope_itrp_o, lane_slope_points_itrp_o


def interpolate_pov_heading(annotation_data):
    frames = np.linspace(0, annotation_data.frame_count - 1, annotation_data.frame_count)
    pov_wheels = annotation_data.pov_wheels
    flags = np.array(get_pov_col(pov_wheels, flags=True))
    user_input_i, = np.where(
        flags == 1)  # index for user inputs    value_index, = np.where(np.isfinite(annotation_data.pov_heading))
    pov_heading = np.array(annotation_data.pov_heading)
    pov_heading_o = np.array(annotation_data.pov_heading_o)

    if user_input_i.size < 1:
        return [np.nan] * annotation_data.frame_count, [np.nan] * annotation_data.frame_count

    else:
        itrp_heading_angle = np.interp(frames, user_input_i, pov_heading[user_input_i], left=np.nan, right=np.nan)
        itrp_heading_angle_o = np.interp(frames, user_input_i, pov_heading_o[user_input_i], left=np.nan, right=np.nan)
        return itrp_heading_angle, itrp_heading_angle_o


def interpolate_sv_heading(annotation_data_sv):
    frames = np.linspace(0, annotation_data_sv.frame_count - 1, annotation_data_sv.frame_count)
    sv_wheels = annotation_data_sv.sv_wheels
    flags = np.array(get_pov_col(sv_wheels, flags=True))
    user_input_i, = np.where(
        flags == 1)  # index for user inputs
    sv_heading = np.array(annotation_data_sv.sv_heading)
    sv_heading_o = np.array(annotation_data_sv.sv_heading_o)

    if user_input_i.size < 1:
        return [np.nan] * annotation_data_sv.frame_count, [np.nan] * annotation_data_sv.frame_count

    else:
        itrp_heading_angle = np.interp(frames, user_input_i, sv_heading[user_input_i], left=np.nan, right=np.nan)
        itrp_heading_angle_o = np.interp(frames, user_input_i, sv_heading_o[user_input_i], left=np.nan, right=np.nan)
        return itrp_heading_angle, itrp_heading_angle_o


def interpolate_adj_heading(annotation_data_adj):
    frames = np.linspace(0, annotation_data_adj.frame_count - 1, annotation_data_adj.frame_count)
    adj_wheels = annotation_data_adj.adj_wheels
    flags = np.array(get_pov_col(adj_wheels, flags=True))
    user_input_i, = np.where(
        flags == 1)  # index for user inputs
    adj_heading = np.array(annotation_data_adj.adj_heading)
    adj_heading_o = np.array(annotation_data_adj.adj_heading_o)

    if user_input_i.size < 1:
        return [np.nan] * annotation_data_adj.frame_count, [np.nan] * annotation_data_adj.frame_count

    else:
        itrp_heading_angle = np.interp(frames, user_input_i, adj_heading[user_input_i], left=np.nan, right=np.nan)
        itrp_heading_angle_o = np.interp(frames, user_input_i, adj_heading_o[user_input_i], left=np.nan, right=np.nan)
        return itrp_heading_angle, itrp_heading_angle_o


def get_col(List, col_i):
    col = []
    for row_i in range(List.__len__()):
        col.append(List[row_i][col_i])

    return col


def get_pov_col(List, col_i=None, flags=False):
    col = []

    if flags:
        for row_i in range(List.__len__()):
            col.append(List[row_i][0])
    else:
        for row_i in range(List.__len__()):
            col.append(List[row_i][1][col_i])

    return col
