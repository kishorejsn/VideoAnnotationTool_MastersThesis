import numpy as np


class StoreAnnotationData_sv:
    def __init__(self, frame_count, frame_size):
        # constant parameters
        self.sv_width = 1.788
        self.lp_dim = 0.3
        self.lp_pos = (np.nan, np.nan, np.nan, np.nan)
        self.sv_length = 2
        self.sv_hood_length = 2
        self.camera_matrix = []
        self.frame_size = frame_size    # y, x (height, width)
        self.height = frame_size[0]
        self.width = frame_size[1]
        self.image_center = int(round(frame_size[0] / 2)), int(round(frame_size[1] / 2))
        self.width_o = round(frame_size[1]/2)
        self.height_o = round(frame_size[0]/2)
        self.frame_size_o = [self.height_o, self.width_o]
        self.image_center_o = int(round(self.height_o / 2)), int(round(self.width_o / 2))

        self.manoeuver_start = 0
        self.manoeuver_end = 0
        self.blinker_start = 0
        self.sv_lane_cross = 0
        self.frame_count = frame_count

        #OG Calculation
        self.sv_placement = [(0, (np.nan, np.nan, np.nan, np.nan)), ] * frame_count
        self.sv_wheels = [(0, [(np.nan, np.nan)]), ] * frame_count
        self.sv_placement_o = [(0, (np.nan, np.nan, np.nan, np.nan)), ] * frame_count
        self.sv_wheels_o = [(0, [(np.nan, np.nan)]), ] * frame_count

        # sv heading
        self.sv_heading = [np.nan] * frame_count
        self.sv_heading_o = [np.nan] * frame_count

        # long
        self.sv_distance_long = [np.nan] * frame_count
        self.sv_distance_long_smooth = [np.nan] * frame_count
        self.sv_distance_long_avg = [np.nan] * frame_count
        self.relative_sv_speed_long = [np.nan]*frame_count
        self.relative_sv_speed_long_smooth = [np.nan] * frame_count
        self.relative_sv_speed_long_avg = [np.nan] * frame_count

        # lat
        self.sv_distance_lat = [np.nan] * frame_count
        self.sv_distance_lat_smooth = [np.nan] * frame_count
        self.sv_distance_lat_avg = [np.nan] * frame_count
        self.relative_sv_speed_lat = [np.nan]*frame_count
        self.relative_sv_speed_lat_smooth = [np.nan] * frame_count
        self.relative_sv_speed_lat_avg = [np.nan] * frame_count

        # pov distances using homography method
        self.sv_distance_long_H = [np.nan] * frame_count
        self.sv_distance_lat_H = [np.nan] * frame_count
        self.sv_distance_lat_H_front = [np.nan] * frame_count
        self.sv_distance_lat_H_rear = [np.nan] * frame_count

        # lane position on the ground using homography method
        self.lane_points_YX_left = [((np.nan, np.nan), (np.nan, np.nan)), ] * frame_count
        self.lane_points_YX_right = [((np.nan, np.nan), (np.nan, np.nan)), ] * frame_count
        self.sv_rear_YX = [((np.nan, np.nan, np.nan), (np.nan, np.nan, np.nan)), ] * frame_count
        self.sv_front_YX = [((np.nan, np.nan, np.nan), (np.nan, np.nan, np.nan)), ] * frame_count
        self.sv_wheels_YX = [((np.nan, np.nan), (np.nan, np.nan)), ] * frame_count
        self.sv_extruded_box = [(np.nan, np.nan, np.nan, np.nan), ] * frame_count
        self.sv_distance_to_lane_long = [np.nan]*frame_count
        self.sv_distance_to_lane_lat_front = [np.nan] * frame_count
        self.sv_distance_to_lane_lat_rear = [np.nan] * frame_count

        self.sv_distance_long_H_o = [np.nan] * frame_count
        self.sv_extruded_box_o = [(np.nan, np.nan, np.nan, np.nan), ] * frame_count
        self.sv_distance_lat_H_front_o = [np.nan] * frame_count
        self.sv_distance_lat_H_rear_o = [np.nan] * frame_count
        self.sv_distance_to_lane_lat_front_o = [np.nan] * frame_count
        self.sv_distance_to_lane_lat_rear_o = [np.nan] * frame_count