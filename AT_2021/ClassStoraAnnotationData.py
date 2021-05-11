
import numpy as np


class StoreAnnotationData:
    def __init__(self, frame_count, frame_size, frame_rate, voMeasureData):
        # constant parameters
        self.pov_width = 1.788
        self.pov_length = 4
        self.sv_hood_length = 2
        self.camera_matrix = []
        self.lp_dim = 0.3
        self.lp_pos = (np.nan, np.nan, np.nan, np.nan)
        self.pov_length = 2

        # video specific
        self.voMeasureData = voMeasureData
        self.frame_count = frame_count
        self.frame_rate = frame_rate
        self.vid_duration = voMeasureData.timestamp[-1]-voMeasureData.timestamp[0]
        self.time = np.linspace(0, self.vid_duration, frame_count)
        # self.time = np.linspace(0, frame_count / frame_rate, frame_count)
        self.frame_size = frame_size    # y, x (height, width)
        self.height = frame_size[0]
        self.width = frame_size[1]
        self.image_center = int(round(frame_size[0] / 2)), int(round(frame_size[1] / 2))
        self.width_o = round(frame_size[1]/2)
        self.height_o = round(frame_size[0]/2)
        self.frame_size_o = [self.height_o, self.width_o]
        self.image_center_o = int(round(self.height_o / 2)), int(round(self.width_o / 2))

        # data input by the user
        self.manoeuver_start = 0
        self.manoeuver_end = 0
        self.blinker_start = 0
        self.pov_lane_cross = 0

        self.pov_placement = [(0, (np.nan, np.nan, np.nan, np.nan)), ] * frame_count
        self.pov_wheels = [(0, [(np.nan, np.nan)]), ] * frame_count
        self.lane_placement_left = [(0, [(np.nan, np.nan)]), ] * frame_count
        self.lane_slope_left = [(0, (np.nan, np.nan)), ] * frame_count
        self.lane_placement_right = [(0, [(np.nan, np.nan)]), ] * frame_count
        self.lane_slope_right = [(0, (np.nan, np.nan)), ] * frame_count

        # parameters calculated in post processing
        # start and end points for lane slope in (x1, y1, x2, y2)
        self.lane_slope_points_left = [(np.nan, np.nan, np.nan, np.nan), ] * frame_count
        self.lane_slope_points_right = [(np.nan, np.nan, np.nan, np.nan), ] * frame_count

        # the vp
        self.lanes_vp = [(np.nan, np.nan), ] * frame_count

        # pov heading
        self.pov_heading = [np.nan] * frame_count

        # pov lan and long distance and speed using the pixel width method
        # long
        self.pov_distance_long = [np.nan] * frame_count
        self.pov_distance_long_smooth = [np.nan] * frame_count
        self.pov_distance_long_avg = [np.nan] * frame_count

        self.relative_pov_speed_long = [np.nan]*frame_count
        self.relative_pov_speed_long_smooth = [np.nan] * frame_count
        self.relative_pov_speed_long_avg = [np.nan] * frame_count

        # lat
        self.pov_distance_lat = [np.nan] * frame_count
        self.pov_distance_lat_smooth = [np.nan] * frame_count
        self.pov_distance_lat_avg = [np.nan] * frame_count

        self.relative_pov_speed_lat = [np.nan]*frame_count
        self.relative_pov_speed_lat_smooth = [np.nan] * frame_count
        self.relative_pov_speed_lat_avg = [np.nan] * frame_count


        # pov distances using homography method
        self.pov_distance_long_H = [np.nan] * frame_count
        self.pov_distance_lat_H = [np.nan] * frame_count

        self.pov_distance_lat_H_front = [np.nan] * frame_count
        self.pov_distance_lat_H_rear = [np.nan] * frame_count

        # lane position on the ground using homography method
        self.lane_points_YX_left = [((np.nan, np.nan), (np.nan, np.nan)), ] * frame_count
        self.lane_points_YX_right = [((np.nan, np.nan), (np.nan, np.nan)), ] * frame_count
        self.pov_rear_YX = [((np.nan, np.nan, np.nan), (np.nan, np.nan, np.nan)), ] * frame_count
        self.pov_front_YX = [((np.nan, np.nan, np.nan), (np.nan, np.nan, np.nan)), ] * frame_count
        self.pov_wheels_YX = [((np.nan, np.nan), (np.nan, np.nan)), ] * frame_count
        self.pov_extruded_box = [(np.nan, np.nan, np.nan, np.nan), ] * frame_count

        self.pov_distance_to_lane_long = [np.nan]*frame_count
        self.pov_distance_to_lane_lat_front = [np.nan] * frame_count
        self.pov_distance_to_lane_lat_rear = [np.nan] * frame_count


        self.pov_placement_o = [(0, (np.nan, np.nan, np.nan, np.nan)), ] * frame_count
        self.pov_wheels_o = [(0, [(np.nan, np.nan)]), ] * frame_count
        self.lane_placement_left_o = [(0, [(np.nan, np.nan)]), ] * frame_count
        self.lane_slope_left_o = [(0, (np.nan, np.nan)), ] * frame_count
        self.lane_placement_right_o = [(0, [(np.nan, np.nan)]), ] * frame_count
        self.lane_slope_right_o = [(0, (np.nan, np.nan)), ] * frame_count

        # parameters calculated in post processing
        # start and end points for lane slope in (x1, y1, x2, y2)
        self.lane_slope_points_left_o = [(np.nan, np.nan, np.nan, np.nan), ] * frame_count
        self.lane_slope_points_right_o = [(np.nan, np.nan, np.nan, np.nan), ] * frame_count

        # the vp
        self.lanes_vp_o = [(np.nan, np.nan), ] * frame_count

        # pov heading
        self.pov_heading_o = [np.nan] * frame_count

        # pov lan and long distance and speed using the pixel width method
        # long
        self.pov_distance_long_o = [np.nan] * frame_count
        self.pov_distance_long_smooth_o = [np.nan] * frame_count
        self.pov_distance_long_avg_o = [np.nan] * frame_count

        self.relative_pov_speed_long_o = [np.nan]*frame_count
        self.relative_pov_speed_long_smootho = [np.nan] * frame_count
        self.relative_pov_speed_long_avg_o = [np.nan] * frame_count

        # lat
        self.pov_distance_lat_o = [np.nan] * frame_count
        self.pov_distance_lat_smooth_o = [np.nan] * frame_count
        self.pov_distance_lat_avg_o = [np.nan] * frame_count

        self.relative_pov_speed_lat_o = [np.nan]*frame_count
        self.relative_pov_speed_lat_smooth_o = [np.nan] * frame_count
        self.relative_pov_speed_lat_avg_o = [np.nan] * frame_count


        # pov distances using homography method
        self.pov_distance_long_H_o = [np.nan] * frame_count
        self.pov_distance_lat_H_o = [np.nan] * frame_count

        self.pov_distance_lat_H_front_o = [np.nan] * frame_count
        self.pov_distance_lat_H_rear_o = [np.nan] * frame_count

        # lane position on the ground using homography method
        self.lane_points_YX_left_o = [((np.nan, np.nan), (np.nan, np.nan)), ] * frame_count
        self.lane_points_YX_right_o = [((np.nan, np.nan), (np.nan, np.nan)), ] * frame_count
        self.pov_rear_YX_o = [((np.nan, np.nan, np.nan), (np.nan, np.nan, np.nan)), ] * frame_count
        self.pov_front_YX_o = [((np.nan, np.nan, np.nan), (np.nan, np.nan, np.nan)), ] * frame_count
        self.pov_wheels_YX_o = [((np.nan, np.nan), (np.nan, np.nan)), ] * frame_count
        self.pov_extruded_box_o = [(np.nan, np.nan, np.nan, np.nan), ] * frame_count

        self.pov_distance_to_lane_long_o = [np.nan]*frame_count
        self.pov_distance_to_lane_lat_front_o = [np.nan] * frame_count
        self.pov_distance_to_lane_lat_rear_o = [np.nan] * frame_count
