import cv2
from DistanceCalculations import *
from scipy import signal


def calculate_parameters(annotation_data, annotation_data_sv, annotation_data_adj, video):
    for i in range(annotation_data.frame_count):
        calculate_pov_in3D(annotation_data, annotation_data_sv, annotation_data_adj, i, video)
        calculate_pov_distance(annotation_data, i)
        calculate_sv_distance(annotation_data, annotation_data_sv, i)
        calculate_adj_distance(annotation_data, annotation_data_adj, i)

    return


def calculate_pov_in3D(annotation_data, annotation_data_sv, annotation_data_adj, i, video):

    lane_slope_points_left = annotation_data.lane_slope_points_left[i]
    lane_slope_points_right = annotation_data.lane_slope_points_right[i]
    pov_placement = annotation_data.pov_placement[i][1]
    wheel_points = annotation_data.pov_wheels[i][1]
    lane_slope_points_left_o = annotation_data.lane_slope_points_left_o[i]
    lane_slope_points_right_o = annotation_data.lane_slope_points_right_o[i]
    pov_placement_o = annotation_data.pov_placement_o[i][1]
    wheel_points_o = annotation_data.pov_wheels_o[i][1]
    calculate_pov_speeds(annotation_data)
    pov_placement_sv = annotation_data_sv.sv_placement[i][1]
    wheel_points_sv = annotation_data_sv.sv_wheels[i][1]
    pov_placement_adj = annotation_data_adj.adj_placement[i][1]
    wheel_points_adj = annotation_data_adj.adj_wheels[i][1]
    pov_placement_sv_o = annotation_data_sv.sv_placement_o[i][1]
    wheel_points_sv_o = annotation_data_sv.sv_wheels_o[i][1]
    pov_placement_adj_o = annotation_data_adj.adj_placement_o[i][1]
    wheel_points_adj_o = annotation_data_adj.adj_wheels_o[i][1]

    if not np.isnan(lane_slope_points_left[0]) and not np.isnan(lane_slope_points_right[0]):
        H, H_o = calculate_vp_and_homography(annotation_data, i)

        if not np.isnan(wheel_points[0][0]):
            calculate_pov_heading(annotation_data,  i,  H, H_o)

        else:
            annotation_data.pov_wheels_YX[i] = ((np.nan, np.nan), (np.nan, np.nan))
            annotation_data.pov_wheels_YX_o[i] = ((np.nan, np.nan), (np.nan, np.nan))

        if not np.isnan(pov_placement[0]) and not np.isnan(annotation_data.pov_heading[i]):
            transform_pov_to3D(annotation_data, i, H, H_o)
        else:
            annotation_data.pov_distance_long_H[i] = np.nan
            annotation_data.pov_extruded_box[i] = (np.nan, np.nan, np.nan, np.nan)
            annotation_data.pov_distance_lat_H_front[i] = np.nan
            annotation_data.pov_distance_lat_H_rear[i] = np.nan
            annotation_data.pov_distance_to_lane_lat_front[i] = np.nan
            annotation_data.pov_distance_to_lane_lat_rear[i] = np.nan

            annotation_data.pov_distance_long_H_o[i] = np.nan
            annotation_data.pov_extruded_box_o[i] = (np.nan, np.nan, np.nan, np.nan)
            annotation_data.pov_distance_lat_H_front_o[i] = np.nan
            annotation_data.pov_distance_lat_H_rear_o[i] = np.nan
            annotation_data.pov_distance_to_lane_lat_front_o[i] = np.nan
            annotation_data.pov_distance_to_lane_lat_rear_o[i] = np.nan

        if not np.isnan(wheel_points_sv[0][0]):
            calculate_sv_heading(annotation_data, annotation_data_sv, i, video, H, H_o)
        else:
            annotation_data_sv.sv_wheels_YX[i] = ((np.nan, np.nan), (np.nan, np.nan))
         #   annotation_data_sv.sv_wheels_YX_o[i] = ((np.nan, np.nan), (np.nan, np.nan))

        if not np.isnan(pov_placement_sv[0]) and not np.isnan(annotation_data_sv.sv_heading[i]):
            transform_pov_to3D_sv(annotation_data_sv, i, H, H_o)
        else:
            annotation_data_sv.sv_distance_long_H[i] = np.nan
            annotation_data_sv.sv_extruded_box[i] = (np.nan, np.nan, np.nan, np.nan)
            annotation_data_sv.sv_distance_lat_H_front[i] = np.nan
            annotation_data_sv.sv_distance_lat_H_rear[i] = np.nan
            annotation_data_sv.sv_distance_to_lane_lat_front[i] = np.nan
            annotation_data_sv.sv_distance_to_lane_lat_rear[i] = np.nan

            annotation_data_sv.sv_distance_long_H_o[i] = np.nan
            annotation_data_sv.sv_extruded_box_o[i] = (np.nan, np.nan, np.nan, np.nan)
            annotation_data_sv.sv_distance_lat_H_front_o[i] = np.nan
            annotation_data_sv.sv_distance_lat_H_rear_o[i] = np.nan
            annotation_data_sv.sv_distance_to_lane_lat_front_o[i] = np.nan
            annotation_data_sv.sv_distance_to_lane_lat_rear_o[i] = np.nan

        if not np.isnan(wheel_points_adj[0][0]):
            calculate_adj_heading(annotation_data, annotation_data_adj, i, video, H, H_o)
        else:
            annotation_data_adj.adj_wheels_YX[i] = ((np.nan, np.nan), (np.nan, np.nan))
         #   annotation_data_adj.sv_wheels_YX_o[i] = ((np.nan, np.nan), (np.nan, np.nan))

        if not np.isnan(pov_placement_adj[0]) and not np.isnan(annotation_data_adj.sv_heading[i]):
            transform_pov_to3D_adj(annotation_data_adj, i, H, H_o)
        else:
            annotation_data_adj.adj_distance_long_H[i] = np.nan
            annotation_data_adj.adj_extruded_box[i] = (np.nan, np.nan, np.nan, np.nan)
            annotation_data_adj.adj_distance_lat_H_front[i] = np.nan
            annotation_data_adj.adj_distance_lat_H_rear[i] = np.nan
            annotation_data_adj.adj_distance_to_lane_lat_front[i] = np.nan
            annotation_data_adj.adj_distance_to_lane_lat_rear[i] = np.nan

            annotation_data_adj.adj_distance_long_H_o[i] = np.nan
            annotation_data_adj.adj_extruded_box_o[i] = (np.nan, np.nan, np.nan, np.nan)
            annotation_data_adj.adj_distance_lat_H_front_o[i] = np.nan
            annotation_data_adj.adj_distance_lat_H_rear_o[i] = np.nan
            annotation_data_adj.adj_distance_to_lane_lat_front_o[i] = np.nan
            annotation_data_adj.adj_distance_to_lane_lat_rear_o[i] = np.nan

    return


def calculate_pov_distance(annotation_data, i):

    pov_placement = annotation_data.pov_placement_o[i][1]
    pov_heading = annotation_data.pov_heading_o[i]

    if not np.isnan(pov_placement[0]):
        pov_distance_long, pov_distance_lat = get_distance(pov_placement, annotation_data.sv_hood_length,
                                                           annotation_data.pov_width,
                                                           pov_heading, annotation_data.image_center_o)
        annotation_data.pov_distance_long[i] = pov_distance_long
        annotation_data.pov_distance_lat[i] = pov_distance_lat
    else:
        annotation_data.pov_distance_long[i] = np.nan
        annotation_data.pov_distance_lat[i] = np.nan
    return


def calculate_sv_distance(annotation_data, annotation_data_sv, i):

    sv_placement = annotation_data_sv.sv_placement_o[i][1]
    sv_heading = annotation_data_sv.sv_heading_o[i]

    if not np.isnan(sv_placement[0]):
        sv_distance_long, sv_distance_lat = get_distance(sv_placement, annotation_data.sv_hood_length,
                                                           annotation_data.pov_width,
                                                           sv_heading, annotation_data.image_center_o)
        annotation_data_sv.sv_distance_long[i] = sv_distance_long
        annotation_data_sv.sv_distance_lat[i] = sv_distance_lat
    else:
        annotation_data_sv.sv_distance_long[i] = np.nan
        annotation_data_sv.sv_distance_lat[i] = np.nan
    return


def calculate_adj_distance(annotation_data, annotation_data_adj, i):

    adj_placement = annotation_data_adj.adj_placement_o[i][1]
    adj_heading = annotation_data_adj.adj_heading_o[i]

    if not np.isnan(adj_placement[0]):
        adj_distance_long, adj_distance_lat = get_distance(adj_placement, annotation_data.sv_hood_length,
                                                           annotation_data.pov_width,
                                                           adj_heading, annotation_data.image_center_o)
        annotation_data_adj.adj_distance_long[i] = adj_distance_long
        annotation_data_adj.adj_distance_lat[i] = adj_distance_lat
    else:
        annotation_data_adj.adj_distance_long[i] = np.nan
        annotation_data_adj.adj_distance_lat[i] = np.nan
    return


def calculate_pov_speeds(annotation_data):
    # ------------------------- Longitudinal speed ------------------------------
    # speed before filtering
    relative_pov_speed_long = np.diff(annotation_data.pov_distance_long) / (1 / annotation_data.frame_rate)
    relative_pov_speed_long = np.insert(relative_pov_speed_long, -1, relative_pov_speed_long[-1])
    annotation_data.relative_pov_speed_long = relative_pov_speed_long

    # speed after smoothening
    avg_window = 15
    avg_mask = np.ones(avg_window) / avg_window

    # Smoothen distance and get speed
    pov_distance_long_smooth = signal.savgol_filter(annotation_data.pov_distance_long, window_length=13, polyorder=2, deriv=0, mode='mirror')
    annotation_data.pov_distance_long_smooth = pov_distance_long_smooth

    relative_pov_speed_long_smooth = np.diff(pov_distance_long_smooth) / (1 / annotation_data.frame_rate)
    relative_pov_speed_long_smooth = np.insert(relative_pov_speed_long_smooth, -1, relative_pov_speed_long_smooth[-1])
    annotation_data.relative_pov_speed_long_smooth = relative_pov_speed_long_smooth

    # smoothen more with moving average
    pov_distance_long_avg = np.convolve(pov_distance_long_smooth, avg_mask, 'same')
    annotation_data.pov_distance_long_avg = pov_distance_long_avg
    # pov_distance_long_avg = signal.medfilt(pov_distance_long_avg, avg_window-1)

    relative_pov_speed_avg = np.diff(pov_distance_long_avg) /(1/ annotation_data.frame_rate)
    relative_pov_speed_avg = np.insert(relative_pov_speed_avg, -1, relative_pov_speed_avg[-1])
    annotation_data.relative_pov_speed_long_avg = relative_pov_speed_avg

    # ------------------------- Lateral speed ------------------------------
    # speed before filtering
    relative_pov_speed_lat = np.diff(annotation_data.pov_distance_lat_o) / (1/ annotation_data.frame_rate)
    relative_pov_speed_lat = np.insert(relative_pov_speed_lat, -1, relative_pov_speed_lat[-1])
    annotation_data.relative_pov_speed_lat = relative_pov_speed_lat

    # speed after savgol smoothning filter
    pov_distance_lat_smooth = signal.savgol_filter(annotation_data.pov_distance_lat_o, window_length=13, polyorder=2, deriv=0, mode='mirror')
    annotation_data.pov_distance_lat_smooth = pov_distance_lat_smooth

    relative_pov_speed_lat_smooth = np.diff(pov_distance_lat_smooth) / (1 / annotation_data.frame_rate)
    relative_pov_speed_lat_smooth = np.insert(relative_pov_speed_lat_smooth, -1, relative_pov_speed_lat_smooth[-1])
    annotation_data.relative_pov_speed_lat_smooth = relative_pov_speed_lat_smooth

    # moving average
    pov_distance_lat_avg = np.convolve(pov_distance_lat_smooth, avg_mask, 'same')
    annotation_data.pov_distance_lat_avg = pov_distance_lat_avg

    relative_pov_speed_lat_avg = np.diff(pov_distance_lat_avg) /(1/ annotation_data.frame_rate)
    relative_pov_speed_lat_avg = np.insert(relative_pov_speed_lat_avg, -1, relative_pov_speed_lat_avg[-1])
    annotation_data.relative_pov_speed_lat_avg = relative_pov_speed_lat_avg


