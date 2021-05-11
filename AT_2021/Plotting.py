# complete implementation of script found in test/test.py
from pylab import *
from scipy import signal
# if global namespace, import plt.figure before drawnow.figure

import matplotlib.pyplot as plt

import matplotlib.lines as mlines


class TopViewFigure:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pov_rear_XY = 0
        self.pov_front_XY = 0
        self.lane_XY_right = 0
        self.lane_XY_left = 0
        self.pov_wheels_XY = 0
        plt.ion()
        self.top_view_figure = plt.figure()
        self.top_view_figure.canvas.manager.window.move(1000,0)
        # win_manager = plt.get_current_fig_manager()
        # win_manager.window.SetPosition((500, 0))
        self.top_view_plot = self.top_view_figure.add_subplot(111)

        self.top_view_plot.plot([-0.85, -0.85, 0.85, 0.85], [0, 2, 2, 0],
                      'r-', lw=2)
        self.top_view_plot.axis([-8, 8, 0, 40])

        self.left_lane_line, = self.top_view_plot.plot([np.nan, np.nan], [np.nan, np.nan], 'b--', lw=2)
        self.right_lane_line, = self.top_view_plot.plot([np.nan, np.nan], [np.nan, np.nan], 'b-', lw=2)

        self.pov_rear_line, = self.top_view_plot.plot([np.nan, np.nan], [np.nan, np.nan], 'k-', lw=2)
        self.pov_front_line, = self.top_view_plot.plot([np.nan, np.nan], [np.nan, np.nan], 'k-', lw=2)
        self.pov_left_line, = self.top_view_plot.plot([np.nan, np.nan], [np.nan, np.nan], 'k-', lw=2)
        self.pov_right_line, = self.top_view_plot.plot([np.nan, np.nan], [np.nan, np.nan], 'k-', lw=2)
        # self.fig.axes(xlim=(-10, 10), ylim=(0, 20))
        # win_manager = plt.get_current_fig_manager()
        # win_manager.window.wm_geometry('+500+0')

    def update_top_view_fig(self, annotation_data, i):

        self.pov_rear_XY = annotation_data.pov_rear_YX[i]
        self.pov_front_XY = annotation_data.pov_front_YX[i]
        # figure_empty = False

        # if not np.isnan(annotation_data.lane_points_YX_left[frame_i][0][0]):
        self.lane_XY_right = annotation_data.lane_points_YX_right[i]
        self.lane_XY_left = annotation_data.lane_points_YX_left[i]
        # figure_empty = False

        # if not np.isnan(annotation_data.pov_wheels_YX[frame_i][0][0]):
        self.pov_wheels_XY = annotation_data.pov_wheels_YX[i]

        # if self.lane_XY_left:
        lane_far_left = self.lane_XY_left[0]
        lane_close_left = self.lane_XY_left[1]
        # print(1, lane_far_left, lane_close_left)
        self.left_lane_line.set_xdata([lane_far_left[0], lane_close_left[0]])
        self.left_lane_line.set_ydata([lane_far_left[1], lane_close_left[1]])

        lane_far_right = self.lane_XY_right[0]
        lane_close_right = self.lane_XY_right[1]
        self.right_lane_line.set_xdata([lane_far_right[0], lane_close_right[0]])
        self.right_lane_line.set_ydata([lane_far_right[1], lane_close_right[1]])

        rear_corner_left = self.pov_rear_XY[0][0:2]
        rear_corner_right = self.pov_rear_XY[1][0:2]
        front_corner_left = self.pov_front_XY[0][0:2]
        front_corner_right = self.pov_front_XY[1][0:2]

        self.pov_rear_line.set_xdata([rear_corner_left[0], rear_corner_right[0]])
        self.pov_rear_line.set_ydata([rear_corner_left[1], rear_corner_right[1]])

        self.pov_front_line.set_xdata([front_corner_left[0], front_corner_right[0]])
        self.pov_front_line.set_ydata([front_corner_left[1], front_corner_right[1]])

        self.pov_left_line.set_xdata([front_corner_left[0], rear_corner_left[0]])
        self.pov_left_line.set_ydata([front_corner_left[1], rear_corner_left[1]])

        self.pov_right_line.set_xdata([front_corner_right[0], rear_corner_right[0]])
        self.pov_right_line.set_ydata([front_corner_right[1], rear_corner_right[1]])


    def make_fig(self):
        # self.fig.clf()
        # self.fig.scatter(self.x, self.y)  # I think you meant this
        if self.pov_rear_XY:
            rear_corner_left = self.pov_rear_XY[0][0:2]
            rear_corner_right = self.pov_rear_XY[1][0:2]
            front_corner_left = self.pov_front_XY[0][0:2]
            front_corner_right = self.pov_front_XY[1][0:2]

            self.top_view_plot.plot([rear_corner_left[0], rear_corner_right[0]], [rear_corner_left[1], rear_corner_right[1]], 'k-', lw=2)

            self.top_view_plot.plot([front_corner_left[0], front_corner_right[0]], [front_corner_left[1], front_corner_right[1]], 'k-', lw=2)

            self.top_view_plot.plot([front_corner_left[0], rear_corner_left[0]], [front_corner_left[1], rear_corner_left[1]], 'k-', lw=2)

            self.top_view_plot.plot([front_corner_right[0], rear_corner_right[0]], [front_corner_right[1], rear_corner_right[1]],
                          'k-', lw=2)

        if self.lane_XY_right:
            lane_far_right = self.lane_XY_right[0]
            lane_close_right = self.lane_XY_right[1]

            self.top_view_plot.plot([lane_far_right[0], lane_close_right[0]], [lane_far_right[1], lane_close_right[1]],
                          'k-', lw=2)

        if self.lane_XY_left:
            lane_far_left = self.lane_XY_left[0]
            lane_close_left = self.lane_XY_left[1]
            print(1)
            self.left_lane_line.set_ydata([lane_far_left[0], lane_close_left[0]])
            self.left_lane_line.set_xdata([lane_far_left[1], lane_close_left[1]])
            # self.top_view_plot.plot([lane_far_left[0], lane_close_left[0]], [lane_far_left[1], lane_close_left[1]],
            #               'k-', lw=2)

        if self.pov_wheels_XY:
            front_wheel = self.pov_wheels_XY[0]
            rear_wheel = self.pov_wheels_XY[1]
            self.top_view_plot.plot([front_wheel[0], rear_wheel[0]], [front_wheel[1], rear_wheel[1]],
                          'ro', lw=2)

        # self.top_view_figure.canvas.flush_events()
        # self.top_view_plot.xlim((-8, 8))


class DataOutFigure:
    def __init__(self):
        plt.ion()
        # self.distance_long_fig = plt
        # self.speed_long_fig = plt

        self.long_plot = plt.figure()
        self.long_plot.canvas.manager.window.move(2000, 0)
        self.distance_long_subplot = self.long_plot.add_subplot(211)
        self.distance_long_radar_data = None
        self.distance_long_out_line = None
        self.distance_long_out_line_time = None
        self.distance_long_out_line_time_start = None

        self.speed_long_subplot = self.long_plot.add_subplot(212)
        self.speed_long_radar_data = None
        self.speed_long_out_line = None
        self.speed_long_out_line_time = None
        self.speed_long_out_line_time_start = None

        # ------------- Lateral Figures
        self.distance_lat_fig = plt
        self.speed_lat_fig = plt

        self.lat_plot = plt.figure()
        self.lat_plot.canvas.manager.window.move(2700, 0)
        self.distance_lat_subplot = self.lat_plot.add_subplot(211)
        self.distance_lat_radar_data = None
        self.distance_lat_out_line = None
        self.distance_lat_out_line_time = None
        self.distance_lat_out_line_time_start = None

        self.speed_lat_subplot = self.lat_plot.add_subplot(212)
        self.speed_lat_radar_data = None
        self.speed_lat_out_line = None
        self.speed_lat_out_line_time = None
        self.speed_lat_out_line_time_start = None

    def initial_speed_plots(self, annotation_data_out):
        time = annotation_data_out.time

        self.distance_long_subplot.axis([0, time[-1], -2, 40])
        self.distance_long_subplot.grid(True)
        self.distance_long_subplot.set_title('Longitudinal Direction')
        self.distance_long_subplot.set_ylabel('Range[m]')

        self.speed_long_subplot.axis([0, time[-1], -10, 10])
        self.speed_long_subplot.grid(True)
        # self.speed_long_subplot.title('Speed')
        self.speed_long_subplot.set_xlabel('Time [s]')
        self.speed_long_subplot.set_ylabel('Relative Speed [m/s]')

        self.distance_lat_subplot.axis([0, time[-1], -10, 10])
        self.distance_lat_subplot.grid(True)
        self.distance_lat_subplot.set_title('Lateral Direction')
        self.distance_lat_subplot.set_ylabel('Range[m]')

        self.speed_lat_subplot.axis([0, time[-1], -10, 10])
        self.speed_lat_subplot.grid(True)
        # self.speed_long_subplot.title('Speed')
        self.speed_lat_subplot.set_xlabel('Time [s]')
        self.speed_lat_subplot.set_ylabel('Relative Speed [m/s]')

        if annotation_data_out.voMeasureData:
            timestamp = annotation_data_out.voMeasureData.timestamp

            timestamp = timestamp + 0

            event_start = annotation_data_out.voMeasureData.event_start

            range_x_t0 = annotation_data_out.voMeasureData.range_x_t0
            range_x_t1 = annotation_data_out.voMeasureData.range_x_t1
            range_x_t2 = annotation_data_out.voMeasureData.range_x_t2
            range_x_t3 = annotation_data_out.voMeasureData.range_x_t3
            range_x_t4 = annotation_data_out.voMeasureData.range_x_t4
            range_x_t5 = annotation_data_out.voMeasureData.range_x_t5
            range_x_t6 = annotation_data_out.voMeasureData.range_x_t6
            range_x_t7 = annotation_data_out.voMeasureData.range_x_t7

            range_rate_x_t0 = annotation_data_out.voMeasureData.range_rate_x_t0
            range_rate_x_t1 = annotation_data_out.voMeasureData.range_rate_x_t1
            range_rate_x_t2 = annotation_data_out.voMeasureData.range_rate_x_t2
            range_rate_x_t3 = annotation_data_out.voMeasureData.range_rate_x_t3
            range_rate_x_t4 = annotation_data_out.voMeasureData.range_rate_x_t4
            range_rate_x_t5 = annotation_data_out.voMeasureData.range_rate_x_t5
            range_rate_x_t6 = annotation_data_out.voMeasureData.range_rate_x_t6
            range_rate_x_t7 = annotation_data_out.voMeasureData.range_rate_x_t7

            range_y_t0 = annotation_data_out.voMeasureData.range_y_t0
            range_y_t1 = annotation_data_out.voMeasureData.range_y_t1
            range_y_t2 = annotation_data_out.voMeasureData.range_y_t2
            range_y_t3 = annotation_data_out.voMeasureData.range_y_t3
            range_y_t4 = annotation_data_out.voMeasureData.range_y_t4
            range_y_t5 = annotation_data_out.voMeasureData.range_y_t5
            range_y_t6 = annotation_data_out.voMeasureData.range_y_t6
            range_y_t7 = annotation_data_out.voMeasureData.range_y_t7

            range_rate_y_t0 = annotation_data_out.voMeasureData.range_rate_y_t0
            range_rate_y_t1 = annotation_data_out.voMeasureData.range_rate_y_t1
            range_rate_y_t2 = annotation_data_out.voMeasureData.range_rate_y_t2
            range_rate_y_t3 = annotation_data_out.voMeasureData.range_rate_y_t3
            range_rate_y_t4 = annotation_data_out.voMeasureData.range_rate_y_t4
            range_rate_y_t5 = annotation_data_out.voMeasureData.range_rate_y_t5
            range_rate_y_t6 = annotation_data_out.voMeasureData.range_rate_y_t6
            range_rate_y_t7 = annotation_data_out.voMeasureData.range_rate_y_t7

            # Plot Radar long Distance if there is
            self.distance_long_radar_data = self.distance_long_subplot.plot(timestamp, range_x_t0,
                                                                             timestamp, range_x_t1,
                                                                             timestamp, range_x_t2,
                                                                             timestamp, range_x_t3,
                                                                             timestamp, range_x_t4,
                                                                             timestamp, range_x_t5,
                                                                             timestamp, range_x_t6,
                                                                             timestamp, range_x_t7,
                                                                            [event_start, event_start], [-100, 100], '--y')

            # self.distance_long_subplot.plot([event_start, event_start], [-100, 100], '--y')
            # Plot Radar long range rate if there is
            self.speed_long_radar_data = self.speed_long_subplot.plot(timestamp, range_rate_x_t0,
                                                                             timestamp, range_rate_x_t1,
                                                                             timestamp, range_rate_x_t2,
                                                                             timestamp, range_rate_x_t3,
                                                                             timestamp, range_rate_x_t4,
                                                                             timestamp, range_rate_x_t5,
                                                                             timestamp, range_rate_x_t6,
                                                                             timestamp, range_rate_x_t7,
                                                                      [event_start, event_start], [-100, 100], '--y')
            # self.speed_long_subplot.plot([event_start, event_start], [-100, 100], '--y')

            # Plot radar lat range if there is
            self.distance_lat_radar_data = self.distance_lat_subplot.plot(timestamp, range_y_t0,
                                                                             timestamp, range_y_t1,
                                                                             timestamp, range_y_t2,
                                                                             timestamp, range_y_t3,
                                                                             timestamp, range_y_t4,
                                                                             timestamp, range_y_t5,
                                                                             timestamp, range_y_t6,
                                                                             timestamp, range_y_t7,
                                                                          [event_start, event_start], [-100, 100], '--y')
            # self.distance_lat_subplot.plot([event_start, event_start], [-100, 100], '--y')

            # Plot radar lat range rate if there is
            self.speed_lat_radar_data = self.speed_lat_subplot.plot(timestamp, range_rate_y_t0,
                                                                        timestamp, range_rate_y_t1,
                                                                        timestamp, range_rate_y_t2,
                                                                        timestamp, range_rate_y_t3,
                                                                        timestamp, range_rate_y_t4,
                                                                        timestamp, range_rate_y_t5,
                                                                        timestamp, range_rate_y_t6,
                                                                        timestamp, range_rate_y_t7,
                                                                    [event_start, event_start], [-100, 100], '--y')
                # [event_start, event_start], [-100, 100], '--y')
            # self.speed_lat_subplot.plot([event_start, event_start], [-100, 100], '--y')


        # Set initial distance long output
        pov_distance_long = np.array(annotation_data_out.pov_distance_long_avg)
        pov_speed_long = np.array(annotation_data_out.relative_pov_speed_long_avg)
        start_time = time[annotation_data_out.manoeuver_start]

        self.distance_long_out_line, = self.distance_long_subplot.plot(time, pov_distance_long, '--r')
        self.distance_long_out_line_time, = self.distance_long_subplot.plot([1, 1], [-100, 100], '-r')
        self.distance_long_out_line_time_start, = self.distance_long_subplot.plot([start_time, start_time], [-100, 100], '--b')

        self.speed_long_out_line, = self.speed_long_subplot.plot(time, pov_speed_long, '--r')
        self.speed_long_out_line_time, = self.speed_long_subplot.plot([1, 1], [-100, 100], '-r')
        self.speed_long_out_line_time_start, = self.speed_long_subplot.plot([start_time, start_time], [-100, 100], '--b')

        # initial lat plots
        pov_distance_lat = -np.array(annotation_data_out.pov_distance_lat_avg)
        pov_speed_lat = -np.array(annotation_data_out.relative_pov_speed_lat_avg)

        self.distance_lat_out_line, = self.distance_lat_subplot.plot(time, pov_distance_lat, '--r')
        self.distance_lat_out_line_time, = self.distance_lat_subplot.plot([1, 1], [-100, 100], '-r')
        self.distance_lat_out_line_time_start, = self.distance_lat_subplot.plot([start_time, start_time], [-100, 100], '--b')

        self.speed_lat_out_line, = self.speed_lat_subplot.plot(time, pov_speed_lat, '--r')
        self.speed_lat_out_line_time, = self.speed_lat_subplot.plot([1, 1], [-100, 100], '-r')
        self.speed_lat_out_line_time_start, = self.speed_lat_subplot.plot([start_time, start_time], [-100, 100], '--b')
        # self.long_plot.canvas.draw()
        # self.long_plot.canvas.flush_events()

    def update_speed_plots(self, annotation_data_out, i):
        pov_distance_long = np.array(annotation_data_out.pov_distance_long_avg)
        pov_speed_long = annotation_data_out.relative_pov_speed_long_avg

        self.distance_long_out_line.set_ydata(pov_distance_long)
        self.speed_long_out_line.set_ydata(pov_speed_long)

        pov_distance_lat = -np.array(annotation_data_out.pov_distance_lat_avg)
        pov_speed_lat = -annotation_data_out.relative_pov_speed_lat_avg

        self.distance_lat_out_line.set_ydata(pov_distance_lat)
        self.speed_lat_out_line.set_ydata(pov_speed_lat)
        # self.long_plot.canvas.draw()
        # self.long_plot.canvas.flush_events()
        # print(1)

    def update_time_marker(self, annotation_data_out, i):
        time = annotation_data_out.time

        self.distance_long_out_line_time.set_xdata([time[i], time[i]])
        self.speed_long_out_line_time.set_xdata([time[i], time[i]])

        self.distance_lat_out_line_time.set_xdata([time[i], time[i]])
        self.speed_lat_out_line_time.set_xdata([time[i], time[i]])

    def update_start_time_marker(self, annotation_data_out):
        time = annotation_data_out.time

        start_time = time[annotation_data_out.manoeuver_start]
        self.distance_long_out_line_time_start.set_xdata([start_time, start_time])
        self.speed_long_out_line_time_start.set_xdata([start_time, start_time])
        self.distance_lat_out_line_time_start.set_xdata([start_time, start_time])
        self.speed_lat_out_line_time_start.set_xdata([start_time, start_time])

    def update_radar_plots(self, annotation_data_out):
        timestamp = annotation_data_out.voMeasureData.timestamp
        event_start = annotation_data_out.voMeasureData.event_start
        print(timestamp[0])
        # Update Distance long
        for line in self.distance_long_radar_data[:-1]:
            line.set_xdata(timestamp)

        self.distance_long_radar_data[-1].set_xdata([event_start, event_start])
        # update speed long
        for line in self.speed_long_radar_data[:-1]:
            line.set_xdata(timestamp)
        self.speed_long_radar_data[-1].set_xdata([event_start, event_start])

        for line in self.distance_lat_radar_data[:-1]:
            line.set_xdata(timestamp)
        self.distance_lat_radar_data[-1].set_xdata([event_start, event_start])

        for line in self.speed_lat_radar_data[:-1]:
            line.set_xdata(timestamp)
        self.speed_lat_radar_data[-1].set_xdata([event_start, event_start])

    def plot_dataOut_vs_radar(self, annotation_data_out, i):
        time = annotation_data_out.time

        if annotation_data_out.voMeasureData:
            timestamp = annotation_data_out.voMeasureData.timestamp

            # dt = time[-1] - timestamp[-1]
            #
            # timestamp = timestamp + dt #- 0.2

            range_x_t0 = annotation_data_out.voMeasureData.range_x_t0
            range_x_t1 = annotation_data_out.voMeasureData.range_x_t1
            range_x_t2 = annotation_data_out.voMeasureData.range_x_t2
            range_x_t3 = annotation_data_out.voMeasureData.range_x_t3
            range_x_t4 = annotation_data_out.voMeasureData.range_x_t4
            range_x_t5 = annotation_data_out.voMeasureData.range_x_t5
            range_x_t6 = annotation_data_out.voMeasureData.range_x_t6
            range_x_t7 = annotation_data_out.voMeasureData.range_x_t7

            range_rate_x_t0 = annotation_data_out.voMeasureData.range_rate_x_t0
            range_rate_x_t1 = annotation_data_out.voMeasureData.range_rate_x_t1
            range_rate_x_t2 = annotation_data_out.voMeasureData.range_rate_x_t2
            range_rate_x_t3 = annotation_data_out.voMeasureData.range_rate_x_t3
            range_rate_x_t4 = annotation_data_out.voMeasureData.range_rate_x_t4
            range_rate_x_t5 = annotation_data_out.voMeasureData.range_rate_x_t5
            range_rate_x_t6 = annotation_data_out.voMeasureData.range_rate_x_t6
            range_rate_x_t7 = annotation_data_out.voMeasureData.range_rate_x_t7

            range_y_t0 = annotation_data_out.voMeasureData.range_y_t0
            range_y_t1 = annotation_data_out.voMeasureData.range_y_t1
            range_y_t2 = annotation_data_out.voMeasureData.range_y_t2
            range_y_t3 = annotation_data_out.voMeasureData.range_y_t3
            range_y_t4 = annotation_data_out.voMeasureData.range_y_t4
            range_y_t5 = annotation_data_out.voMeasureData.range_y_t5
            range_y_t6 = annotation_data_out.voMeasureData.range_y_t6
            range_y_t7 = annotation_data_out.voMeasureData.range_y_t7

        pov_distance_long = np.array(annotation_data_out.pov_distance_long)
        pov_distance_long_H = annotation_data_out.pov_distance_long_H
        pov_distance_long_filterd = annotation_data_out.pov_distance_long_avg
        # plt.figure(0)
        # self.speed_long_fig.clf()
        # self.distance_long_fig.clf()

        # subplot(211)
        if annotation_data_out.voMeasureData:
            self.distance_long_fig.plot(timestamp, range_x_t0,
                     timestamp, range_x_t1,
                     timestamp, range_x_t2,
                     timestamp, range_x_t3,
                     timestamp, range_x_t4,
                     timestamp, range_x_t5,
                     timestamp, range_x_t6,
                     timestamp, range_x_t7,)

        self.distance_long_fig.plot(
                 time, pov_distance_long, 'or',
                 time, pov_distance_long_filterd, '--k',
                 time, pov_distance_long_H, '--b',
                 [time[i], time[i]], [-15, 15], '-r')

        self.distance_long_fig.title('Distance comparison')
        self.distance_long_fig.ylabel('Range [m]')
        self.distance_long_fig.draw()

        subplot(212)
        if annotation_data_out.voMeasureData:
            self.speed_long_fig.plot(timestamp, range_rate_x_t0,
                     timestamp, range_rate_x_t1,
                     timestamp, range_rate_x_t2,
                     timestamp, range_rate_x_t3,
                     timestamp, range_rate_x_t4,
                     timestamp, range_rate_x_t5,
                     timestamp, range_rate_x_t6,
                     timestamp, range_rate_x_t7)

        self.speed_long_fig.plot(
            time, annotation_data_out.relative_pov_speed_long_avg, '--r',
                 [time[i], time[i]], [-5, 5], '-r')

        self.speed_long_fig.title('Speed comparison')
        self.speed_long_fig.xlabel('Time [s]')
        self.speed_long_fig.ylabel('Relative speed [m/s]')
        self.speed_long_fig.draw()

        pov_distance_lat_front = -np.array(annotation_data_out.pov_distance_lat_H_front)
        pov_distance_lat_rear = -np.array(annotation_data_out.pov_distance_lat_H_rear)
        pov_distance_lat = -np.array(annotation_data_out.pov_distance_lat)


        # plt.figure(2)
        # self.distance_lat_fig.plot(timestamp, range_y_t0,
        #          timestamp, range_y_t1,
        #          timestamp, range_y_t2,
        #          timestamp, range_y_t3,
        #          timestamp, range_y_t4,
        #          timestamp, range_y_t5,
        #          timestamp, range_y_t6,
        #          timestamp, range_y_t7,
        #          time, pov_distance_lat_front, '*r',
        #          time, pov_distance_lat_rear, '*b',
        #          time, pov_distance_lat, 'oy')
        #          # time, annotation_data.pov_distancem2, 'ob')
        # #plt.plot(time, pov_distance)
        # plt.show(block=False)

        plt.tight_layout()

# print(pov_distance)
