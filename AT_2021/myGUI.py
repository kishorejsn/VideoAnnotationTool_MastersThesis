
import cv2
import numpy as np
from time import sleep
import tkinter as tk
from DrawFunctions import *
from DistanceCalculations_mohammed import *
# from lane_detection import *
from lane_detection import *
from interpolationFunctions import *
from ClassStoraAnnotationData import *
from ClassStoraAnnotationData_sv import *
from ClassStoraAnnotationData_adj import *
from calculateParameters import *
from Plotting import TopViewFigure, DataOutFigure
adnr = 1


def load_videoFile(filepath):
    cap = cv2.VideoCapture(filepath)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    Video = []
    Video_unrectified = []
    ret_val, frame = cap.read()

    while ret_val:
        Video_unrectified.append(frame)
        frame_rectified = rectify(frame)
        Video.append(frame_rectified)

        frame_count += 1
        # print(i)
        ret_val, frame = cap.read()

    video_dim = Video[1].shape
    scale_percent = 200
    width = int(video_dim[0] * scale_percent / 100)
    height = int(video_dim[1] * scale_percent / 100)
    dim = (height, width)

    for i in range(frame_count):
        Video[i] = cv2.resize(Video[i], dim, interpolation=cv2.INTER_NEAREST)

    return Video, fps, frame_count, dim


def check_status(prev_status):
    try:
        key_press = cv2.waitKey(1)
        new_status = {ord('s'): 'pause', ord('S'): 'pause',
                      ord('w'): 'play', ord('W'): 'play',
                      ord('a'): 'prev_frame', ord('A'): 'prev_frame',
                      ord('d'): 'next_frame', ord('D'): 'next_frame',
                      ord('q'): 'fast_backward', ord('Q'): 'fast_backward',
                      ord('e'): 'fast_forward', ord('E'): 'fast_forward',
                      ord('c'): 'snap', ord('C'): 'snap',
                      ord('p'): 'defineVehicle', ord('P'): 'defineVehicle',
                      ord('l'): 'defineLane_left', ord('L'): 'defineLane_left',
                      ord('ö'): 'defineLane_right', ord('ö'): 'defineLane_right',
                      ord('-'): 'decrease_pov_width', ord('+'): 'increase_pov_width',
                      ord('6'): 'shift_radar_right', ord('4'): 'shift_radar_left',
                      ord('l'): 'lp', ord('L'): 'lp',
                      -1: prev_status,
                      27: 'exit'}[key_press]
        # if key_press == -1:
        #     button_pressed = False
        # else:
        #     button_pressed = True
        button_pressed = True
    except:
        new_status = prev_status
        button_pressed = False

    return new_status, button_pressed


class check_control_win_status:
    def __init__(self):
        self.status = None

    def play(self):
        self.status = 'play'
        # return self.status

    def pause(self):
        self.status = 'pause'

    def fast_forward(self):
        self.status = 'fast_forward'

    def fast_backward(self):
        self.status = 'fast_backward'

    def prev_frame(self):
        self.status = 'prev_frame'

    def next_frame(self):
        self.status = 'next_frame'

    def define_vehicle(self):
        self.status = 'defineVehicle'

    def define_lane_left(self):
        self.status = 'defineLane_left'

    def define_lane_right(self):
        self.status = 'defineLane_right'

    def define_wheels(self):
        self.status = 'defineWheels'

    def manoeuver_start(self):
        self.status = 'set_manoeuver_start'

    def set_times(self):
        self.status = 'set_times'

    def draw_on_off(self):
        self.status = 'draw_on_off'

    def lp(self):
        self.status = 'lp'


class control_win:


    def callback(self, selection):
        global adnr
        if selection == 'POV':
            adnr = 1
        elif selection == 'LV in front of POV':
            adnr = 2
        elif selection == 'LV adjacent lane':
            adnr = 3
        print(adnr)


    def __init__(self, controlWin):
        self.win = controlWin
        self.win_frame = tk.Frame(self.win)
        self.win_frame.pack()
        self.set_status = check_control_win_status()
        self.options = ['POV', 'LV in front of POV', 'LV adjacent lane']
        self.variable = tk.StringVar(self.win)
        self.variable.set(self.options[0])
        opt = tk.OptionMenu(self.win, self.variable, *self.options, command=self.callback)
        opt.config(width=200)
        opt.pack(side="top")
        tk.Button(self.win_frame, text='play', command=self.set_status.play).pack()
        tk.Button(self.win_frame, text='pause', command=self.set_status.pause).pack()
        tk.Button(self.win_frame, text='fast forward', command=self.set_status.fast_forward).pack()
        tk.Button(self.win_frame, text='fast backward', command=self.set_status.fast_backward).pack()
        tk.Button(self.win_frame, text='next frame', command=self.set_status.next_frame).pack()
        tk.Button(self.win_frame, text='prev frame', command=self.set_status.prev_frame).pack()
        self.define_vehicle_button = tk.Button(self.win_frame, text='define vehicle', command=self.set_status.define_vehicle)
        self.define_vehicle_button.pack()
        self.define_lp_button = tk.Button(self.win_frame, text='License Plate', command=self.set_status.lp)
        self.define_lp_button.pack()
        self.left_lane_button = tk.Button(self.win_frame, text='define left lane', command=self.set_status.define_lane_left)
        self.left_lane_button.pack()
        self.righ_lane_button = tk.Button(self.win_frame, text='define right lane', command=self.set_status.define_lane_right)
        self.righ_lane_button.pack()
        self.define_wheels_button = tk.Button(self.win_frame, text='define wheels', command=self.set_status.define_wheels)
        self.define_wheels_button.pack()
        tk.Button(self.win_frame, text='Manoeuvre Start', command=self.set_status.manoeuver_start).pack()
        tk.Button(self.win_frame, text='Set Times', command=self.set_status.set_times).pack()
        tk.Button(self.win_frame, text='Draw on/off', command=self.set_status.draw_on_off).pack()


    def update(self):
        self.win.update()

    def get_status(self):
        status = self.set_status.status
        return status

    def init_status(self):
        self.set_status.__init__()



class FrameCounter:
    def __init__(self, init):
        self.i = init

    def set_video_time(self, x):
        self.i = x
        return


def update_YX_figure(annotation_data, frame_i, my_fig):

    figure_empty = True

    my_fig.update_top_view_fig(annotation_data, frame_i)



def set_blinker_start(annotation_data, frame_counter, master):
    annotation_data.blinker_start = frame_counter.i
    print('blinker start: ', annotation_data.blinker_start)
    master.destroy()


def set_lane_cross(annotation_data, frame_counter, master):
    annotation_data.pov_lane_cross = frame_counter.i
    print('pov_lane_cross: ', annotation_data.pov_lane_cross)
    master.destroy()


def set_event_times(annotation_data, frame_counter):
    time_events_master = tk.Tk()

    tk.Label(time_events_master, text='Enter time events')

    try:
        annotation_data.blinker_start
        tk.Button(time_events_master, text='blinker start: ' + str(annotation_data.blinker_start),
                  command=lambda: set_blinker_start(annotation_data, frame_counter, time_events_master)).pack()
        tk.Button(time_events_master, text='lane crossed: ' + str(annotation_data.pov_lane_cross),
                  command=lambda: set_lane_cross(annotation_data, frame_counter, time_events_master)).pack()
    except:
        tk.Button(time_events_master, text='blinker start: ',
                  command=lambda: set_blinker_start(annotation_data, frame_counter, time_events_master)).pack()
        tk.Button(time_events_master, text='lane crossed: ',
                  command=lambda: set_lane_cross(annotation_data, frame_counter, time_events_master)).pack()

    time_events_master.geometry('100x100+700+100')

    done = False
    while not done:
        time_events_master.update()
        try:
            time_events_master.winfo_exists()
        except:
            done = True


def play_videoFile(video_default, fps, frame_count, win_name, annotation_data, annotation_data_sv, annotation_data_adj,
                   win_display_tkinter, win_control):
    global adnr

    video_dim = video_default[1].shape

    # configure information window
    win_display_tkinter.geometry('%dx%d+%d+%d' % (video_dim[1] + 5, 100, 0, video_dim[0] + 90))
    controls_label = tk.Label(win_display_tkinter, text='Keyboard controls: \nW/Play, S/Pause, A/Prev frame, D/Next frame, L/Define lane '
                                                     'Ö/Define right lane, ''P/Define POV, esc/End')
    controls_label.config(width=300, wraplength= video_dim[1], justify='left', bg='green')
    controls_label.pack()

    status_label = tk.Label(win_display_tkinter)
    status_label.config(width=300, wraplength=video_dim[1], anchor='w', justify='left', bg='grey')
    status_label.pack()

    information_label = tk.Label(win_display_tkinter)
    information_label.config(width=300, wraplength=video_dim[1], anchor='w', justify='left', bg='grey')
    information_label.pack()

    # configure video window
    frame_counter = FrameCounter(0)
    cv2.namedWindow(win_name, cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow(win_name, 0, 0)
    cv2.resizeWindow(win_name, video_dim[0], video_dim[1])
    cv2.createTrackbar('Frames', win_name, 0, frame_count-1, frame_counter.set_video_time)

    # configure control button window
    win_control.geometry('%dx%d+%d+%d' % (100, video_dim[0], video_dim[1]+5, 0))
    win_control_buttons = control_win(win_control)

    vid_end = False
    draw_all = True
    status = 'pause'

    # Configure enter time events win


    my_fig = TopViewFigure()
    data_out_fig = DataOutFigure()

    video_withdrawing = video_default.copy()
    data_out_fig.initial_speed_plots(annotation_data)

    for i1 in range(frame_count):
        img1 = video_default[i1].copy()
        my_draw_annotations(img1, annotation_data, i1)
        video_withdrawing[i1] = img1.copy()

    win_control_buttons.update()

    # Video player loop
    while not vid_end:
        status, button_pressed = check_status(status)
        cv2.setTrackbarPos('Frames', win_name, frame_counter.i)

        win_control_buttons.update()

        if win_control_buttons.get_status():
            status = win_control_buttons.get_status()
            win_control_buttons.init_status()

        if status == 'play':
            status_label.config(text='status: '+status + ' Draw: ' + str(draw_all))
            cv2.imshow(win_name, video_withdrawing[frame_counter.i])
            sleep(0.25/fps)
            if frame_counter.i == frame_count - 1:
                frame_counter.i = frame_counter.i
            else:
                frame_counter.i += 1

            my_fig.update_top_view_fig(annotation_data, frame_counter.i)
            data_out_fig.update_time_marker(annotation_data, frame_counter.i)
            continue

        elif status == 'pause':
            status_label.config(text='status: '+status + ' Draw: ' + str(draw_all))
            cv2.imshow(win_name, video_withdrawing[frame_counter.i])
            continue

        elif status == 'fast_forward':
            status_label.config(text='status: '+status + ' Draw: ' + str(draw_all))
            if frame_counter.i < frame_count - 1:
                frame_counter.i += 1
                cv2.imshow(win_name, video_withdrawing[frame_counter.i])
                sleep(0.25 / fps)
            else:
                status = 'pause'
            continue

        elif status == 'fast_backward':
            status_label.config(text='status: '+status + ' Draw: ' + str(draw_all))
            if frame_counter.i > 0:
                frame_counter.i -= 1
                cv2.imshow(win_name, video_withdrawing[frame_counter.i])
                sleep(0.25 / fps)
            else:
                status = 'pause'
            continue

        elif status == 'prev_frame':
            if frame_counter.i > 0:
                frame_counter.i -= 1
            cv2.imshow(win_name, video_withdrawing[frame_counter.i])
            my_fig.update_top_view_fig(annotation_data, frame_counter.i)
            data_out_fig.update_time_marker(annotation_data, frame_counter.i)
            status = 'pause'
            continue

        elif status == 'next_frame':
            if frame_counter.i < frame_count - 1:
                frame_counter.i += 1
            cv2.imshow(win_name, video_withdrawing[frame_counter.i])
            status = 'pause'
            my_fig.update_top_view_fig(annotation_data, frame_counter.i)
            data_out_fig.update_time_marker(annotation_data, frame_counter.i)
            continue

        elif status == 'defineVehicle':
            win_control_buttons.define_vehicle_button.config(background='red')
            status_label.config(text='status: ' + status + ' Draw: ' + str(draw_all))
            status_label.update()
            information_label.config(
                text='Use the mouse to drag a box around the vehicle. \nPress enter to confirm selection')
            information_label.update()
            img = video_default[frame_counter.i].copy()  # Copy original image
            define_vehicle(win_name, img, annotation_data, annotation_data_sv, annotation_data_adj, frame_counter.i, adnr)

            cv2.imshow(win_name, video_withdrawing[frame_counter.i])
            win_control_buttons.define_vehicle_button.config(background='SystemButtonFace')
            print(str(frame_counter.i))
            status = 'pause'

        elif status == 'defineLane_left':
            win_control_buttons.left_lane_button.config(background='red')
            status_label.config(text='status: ' + status + ' Draw: ' + str(draw_all))
            status_label.update()
            information_label.config(
                text='Use the mouse to place at least two points on the left lane.\nPress enter to confirm selection')
            information_label.update()
            img = video_default[frame_counter.i].copy()
            define_lane_left(win_name, img, annotation_data, frame_counter.i)
            win_control_buttons.left_lane_button.config(background='SystemButtonFace')
            status = 'pause'

        elif status == 'defineLane_right':
            win_control_buttons.righ_lane_button.config(background='red')
            status_label.config(text='status: ' + status + ' Draw: ' + str(draw_all))
            status_label.update()
            information_label.config(
                text='Use the mouse to place at least two points on the right lane. \nPress enter to confirm selection')
            information_label.update()
            img = video_default[frame_counter.i].copy()
            define_lane_right(win_name, img, annotation_data, frame_counter.i)
            win_control_buttons.righ_lane_button.config(background='SystemButtonFace')
            status = 'pause'

        elif status == 'defineWheels':
            win_control_buttons.define_wheels_button.config(background='red')
            status_label.config(text='status: ' + status + ' Draw: ' + str(draw_all))
            status_label.update()
            information_label.config(
                text='Use the mouse to mark the wheels of the pov vehicle. \nPress Enter to confirm selection')

            information_label.update()
            img = video_default[frame_counter.i].copy()
            cv2.imshow(win_name, video_withdrawing[frame_counter.i])
            define_vehicle_wheels(win_name, img, annotation_data, annotation_data_sv, annotation_data_adj, frame_counter.i, adnr)
            win_control_buttons.define_wheels_button.configure(background='SystemButtonFace')
            status = 'pause'

        elif status == 'set_manoeuver_start':
            annotation_data.manoeuver_start = frame_counter.i
            print(annotation_data.manoeuver_start)
            data_out_fig.update_start_time_marker(annotation_data)
            status = 'pause'

        elif status == 'set_times':
            set_event_times(annotation_data, frame_counter)
            status = 'pause'

        elif status == 'decrease_pov_width':
            annotation_data.sv_hood_length = annotation_data.sv_hood_length - 0.1
            print('hood_length= ' + str(annotation_data.sv_hood_length))
            cv2.imshow(win_name, video_withdrawing[frame_counter.i])
            status = 'pause'

        elif status == 'increase_pov_width':
            annotation_data.sv_hood_length = annotation_data.sv_hood_length + 0.1
            print('hood_length= ' + str(annotation_data.sv_hood_length))
            cv2.imshow(win_name, video_withdrawing[frame_counter.i])
            status = 'pause'

        elif status == 'shift_radar_right':
            annotation_data.voMeasureData.timestamp = annotation_data.voMeasureData.timestamp + 0.05
            annotation_data.voMeasureData.event_start = annotation_data.voMeasureData.event_start + 0.05
            data_out_fig.update_radar_plots(annotation_data)
            status = 'pause'

        elif status == 'lp':
            win_control_buttons.define_lp_button.config(background='red')
            status_label.config(text='status: ' + status + ' Draw: ' + str(draw_all))
            status_label.update()
            information_label.config(

                text='Use the mouse to drag a box around the license plate. \nPress enter to confirm selection')

            information_label.update()
            img = video_default[frame_counter.i].copy()  # Copy original image
            define_lp(win_name, img, annotation_data, annotation_data_sv, annotation_data_adj, frame_counter.i, adnr)
            cv2.imshow(win_name, video_withdrawing[frame_counter.i])
            win_control_buttons.define_lp_button.config(background='SystemButtonFace')
            status = 'pause'


        elif status == 'shift_radar_left':
            annotation_data.voMeasureData.timestamp = annotation_data.voMeasureData.timestamp - 0.05
            annotation_data.voMeasureData.event_start = annotation_data.voMeasureData.event_start - 0.05
            data_out_fig.update_radar_plots(annotation_data)
            status = 'pause'

        elif status == 'draw_on_off':
            draw_all = not draw_all
            status = 'pause'

        elif status == 'exit':

            break

        information_label.config(text='')
        information_label.update()
        interpolate_annotations(annotation_data)
        interpolate_annotations_sv(annotation_data_sv)
        interpolate_annotations_adj(annotation_data_adj)
        calculate_parameters(annotation_data, annotation_data_sv, annotation_data_adj, video_default)
        annotation_data_sv.pov_heading_sv, annotation_data_sv.pov_heading_sv = interpolate_sv_heading(annotation_data_sv)
        annotation_data_sv.pov_heading_adj, annotation_data_sv.pov_heading_adj_o = interpolate_adj_heading(annotation_data_adj)
        annotation_data.pov_heading, annotation_data.pov_heading_o = interpolate_pov_heading(annotation_data)
        annotation_data_sv.sv_heading, annotation_data_sv.sv_heading_o = interpolate_sv_heading(annotation_data_sv)
        annotation_data_adj.adj_heading, annotation_data_adj.adj_heading_o = interpolate_adj_heading(annotation_data_adj)
        my_fig.update_top_view_fig(annotation_data, frame_counter.i)
        data_out_fig.update_speed_plots(annotation_data, frame_counter.i)

        for i1 in range(frame_count):
            img1 = video_default[i1].copy()
            my_draw_annotations(img1, annotation_data, i1, draw_all=draw_all)
            video_withdrawing[i1] = img1.copy()

    return annotation_data, annotation_data_sv, annotation_data_adj
