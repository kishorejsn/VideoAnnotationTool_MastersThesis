# ----------------------------
# import stuff here
# main loads files and setups the structure of the data
import tkinter as tk
import tkinter.filedialog
from PIL import Image
from PIL import ImageTk
import cv2
from time import sleep
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from myGUI import *
import scipy.io
import pickle
from tkinter import ttk


def ask4filepath():
    global FilePath, file_path_win
    FilePath = tkinter.filedialog.askopenfilename()
    file_path_win.destroy()


def set_reannotate_true():
    global re_annotate_bool, re_annotate_win
    re_annotate_bool = True
    re_annotate_win.destroy()

def set_reannotate_false():
    global re_annotate_bool, re_annotate_win
    re_annotate_bool = False
    re_annotate_win.destroy()



def treeViewDouble(event):
    global tree, tree_view_master, Event_ID_Treeview
    Event_ID_Treeview = tree.selection()[0]
    print(Event_ID_Treeview)
    tree.unbind('<Double-1>')
    sleep(0.5)
    tree.destroy()
    tree_view_master.destroy()


# ------------------------ to be defined before annotation starts -------------
data10_disk = '/Users/kishorejsn/Documents/SP7-8/Thesis_Kishore_Burak/SHRP2_data_cutins'
projects10_disk = '/Users/kishorejsn/Documents/SP7-8/Thesis_Kishore_Burak'

annotator_name = 'ahmed'

# names: 'fgiulio', 'jonas', 'majid', 'pierluigi', 'ahmed' and 'hmed'

# load the list with usable events
usable_events_path = projects10_disk + '/AT_2021/usable_events_27_5_2020'
usable_vids = scipy.io.loadmat(usable_events_path + '.mat', struct_as_record=True, squeeze_me=True)
scipy.io.savemat(usable_events_path + '_backup.mat', {'usable_events': usable_vids['usable_events']})
# File path win
FilePath = None

Event_ID_Treeview = None
Event_ID_Treeview_Index = None

tree_view_master = tk.Tk()
tree_view_master.title('User: ' + annotator_name)
tree = ttk.Treeview(tree_view_master)
tree['columns'] = ('one', 'two', 'three', 'four', 'five', 'six')

tree.heading('#0', text='Event ID', anchor=tk.W)
tree.heading('#1', text='status', anchor=tk.W)
tree.heading('#2', text='Opened by',  anchor=tk.W)
tree.heading('#3', text='Date modified',  anchor=tk.W)
tree.heading('#4', text='suitable for annotation', anchor=tk.W)
tree.heading('#5', text='Assigned annotator', anchor=tk.W)
tree.heading('#6', text='Reason', anchor=tk.W)
tree.column('#6', width=400)
tree.bind('<Double-1>', treeViewDouble)

# screened_folder = tree.insert('', '1', text='screened')
# suitable_for_annotation_folder = tree.insert('', 1, text='suitable for annotation')
un_suitable_for_annotation_folder = tree.insert('', 1, text='not suitable for annotation')
# un_screened_folder = tree.insert('', 1, text='not screened')
ahmed_folder = tree.insert('', 1, text='Ahmed')
jonas_folder= tree.insert('', 1, text='jonas')
guilio_folder = tree.insert('', 1, text='giulio')
majid_folder = tree.insert('', 1, text='majid')
pierluigi_folder = tree.insert('', 1, text='pierluigi')

other_good_events = tree.insert('', 1, text='Other good events')
# good_events_folder = tree.insert('', '1', text= 'good events')

scroll_bar = ttk.Scrollbar(tree_view_master, orient='vertical', command=tree.yview)
scroll_bar.pack(side='right', fill='y')
tree.configure(yscrollcommand=scroll_bar.set)

for i in range(len(usable_vids['usable_events']['EventID'])):
    EventID = usable_vids['usable_events']['EventID'][i]
    Status = usable_vids['usable_events']['Status'][i]
    By = usable_vids['usable_events']['by'][i]
    Date = usable_vids['usable_events']['dateModified'][i]
    Reason = usable_vids['usable_events']['reason'][i]
    good = usable_vids['usable_events']['good'][i]
    assigned_annotator = usable_vids['usable_events']['assigned_annotator'][i]

    if good == 'yes':
        # tree.insert(suitable_for_annotation_folder, 'end', id=EventID, text=EventID, values=(Status, By, Date, good, Reason))
        if assigned_annotator == 'ahmed':
            tree.insert(ahmed_folder, 'end', id=EventID, text=EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        elif assigned_annotator == 'fgiulio':
            tree.insert(guilio_folder, 'end', id=EventID, text=EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        elif assigned_annotator == 'jonas':
            tree.insert(jonas_folder, 'end', id=EventID, text= EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        elif assigned_annotator == 'majid':
            tree.insert(majid_folder, 'end', id=EventID, text= EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        elif assigned_annotator == 'pierluigi':
            tree.insert(pierluigi_folder, 'end', id=EventID, text= EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        else:
            tree.insert(other_good_events, 'end', id=EventID, text= EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
    elif good == 'no':
        if assigned_annotator == 'ahmed':
            tree.insert(ahmed_folder, 'end', id=EventID, text=EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        elif assigned_annotator == 'fgiulio':
            tree.insert(guilio_folder, 'end', id=EventID, text=EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        elif assigned_annotator == 'jonas':
            tree.insert(jonas_folder, 'end', id=EventID, text= EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        elif assigned_annotator == 'majid':
            tree.insert(majid_folder, 'end', id=EventID, text= EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        elif assigned_annotator == 'pierluigi':
            tree.insert(pierluigi_folder, 'end', id=EventID, text= EventID, values=(Status, By, Date, good, assigned_annotator, Reason))
        else:
            tree.insert(un_suitable_for_annotation_folder, 'end', id=EventID, text=EventID,
                        values=(Status, By, Date, good, assigned_annotator, Reason))

    # if good == 'yes':
        # tree.insert(good_events_folder, 'end', id=EventID, text=EventID, values=(Status, By, Date, good, Reason))
    # tree.insert('', i, id= EventID, text=EventID, values=(Status, By, Date, good, Reason))

tree.pack(expand=True, fill='y')
tree_view_master.geometry('1400x700')
tree_view_master.mainloop()

videos_file_path = data10_disk + '/DUL-A-3-19-432/FrontVideos/Event_ID_'
#FilePath = videos_file_path + Event_ID_Treeview + '_Front.mp4'
FilePath = videos_file_path + '10528090' +'_Front.mp4'
print(FilePath)

# re-annotate win this will only run if there is a previously annotated file
re_annotate_bool = False

annotation_tool_out_path = projects10_disk + '/Annotation tool out/Annotation_out_ID_'
SHPR2_mat_in_path = projects10_disk + '/SHRP2_data_cutins/DUL-A-3-19-432/MatOut/Event_ID_'

if FilePath:
    file_name = FilePath
    file_name = file_name.replace('_', ' ')
    event_ID = str([int(s) for s in file_name.split() if s.isdigit()][0])
    print('Event ID='+event_ID)
    re_annotate_file_exists = False

    video_Default, frame_rate, frame_count, video_dim = load_videoFile(FilePath)

    try:
        in_file = open(annotation_tool_out_path + event_ID
                       + annotator_name +'.shams', 'rb')
        annotation_data = pickle.load(in_file)
        in_file.close()
        re_annotate_file_exists = True

    except FileNotFoundError:
        print("no previous annotations found")
        re_annotate_file_exists = False

    if re_annotate_file_exists:
        re_annotate_win = tk.Tk()
        re_annotate_win.title("Ask for re-annotation")

        re_annotate_frame = tk.Frame(re_annotate_win)
        re_annotate_frame.pack()


        tk.Label(re_annotate_frame,
                 text="There is previously annotated data available for this video, would you like to use it?").pack()
        tk.Button(re_annotate_frame, text="Yes", command=set_reannotate_true).pack()
        tk.Button(re_annotate_frame, text="No", command=set_reannotate_false).pack()
        re_annotate_win.mainloop()

    if not re_annotate_bool: # if the user no want to use old annotation
        SHARP2_mat_exists = False

        try:
            print('Loading...')
            SHARP2_mat = scipy.io.loadmat(SHPR2_mat_in_path + event_ID + '.mat',struct_as_record=False,squeeze_me=True)
            SHARP2_mat_exists = True
        except FileNotFoundError:
            print('No SHRP2 mat found')
            SHARP2_mat_exists = False

        if SHARP2_mat_exists:
            oDBdata = SHARP2_mat['oDBdata']
            # time = np.linspace(0, frame_count / frame_rate, frame_count)
            voMeasureData = oDBdata.voMeasureData
            # Get video duration assumed its the same as the timeseries
            vid_duration = voMeasureData.timestamp[-1] - voMeasureData.timestamp[0]
            # make time vector for all video frames
            vid_frames = np.linspace(0, frame_count-1, frame_count)
            time = np.linspace(0, vid_duration, frame_count)
            # here the offset between the video and data is removed.
            video_start_time = oDBdata.oSegmentInfo.Video_start_time
            dt = (voMeasureData.timestamp[0] - video_start_time) * 1e-3
            voMeasureData.event_start = (oDBdata.oSegmentInfo.EventStart - voMeasureData.timestamp[0]) * 1e-3 + dt
            voMeasureData.timestamp = (voMeasureData.timestamp - voMeasureData.timestamp[0]) * 1e-3 + dt
            voMeasureData.dt = dt

        else:
            voMeasureData = 0

    annotation_data = StoreAnnotationData(frame_count, video_dim, frame_rate, voMeasureData)
    annotation_data_sv = StoreAnnotationData_sv(frame_count, video_dim)
    annotation_data_adj = StoreAnnotationData_adj(frame_count, video_dim)
    video_player_win = 'video player: Event ID -' + event_ID + ' user ' + annotator_name
    tk_information_win = tk.Tk()
    tk_controls_win = tk.Tk()

    annotation_data_out, annotation_data_out_sv, annotation_data_out_adj = play_videoFile(video_Default, frame_rate,
                                                                                          frame_count, video_player_win,
                                                                                          annotation_data,
                                                                                          annotation_data_sv,
                                                                                          annotation_data_adj,
                                                                                          tk_information_win,
                                                                                          tk_controls_win)

    cv2.destroyAllWindows()
    tk_controls_win.destroy()
    tk_information_win.destroy()

    # ----------------------- Ask if annotation is good and save
    yeah_no = True
    reason = ''

    def hell_yeah():
        global yeah_no
        yeah_no = True
        reason_win.destroy()


    def nope():
        global yeah_no
        yeah_no = False
        reason_win.destroy()


    def get_e1():
        global reason
        reason = e1.get()
        ask_good_win.destroy()


    reason_win = tk.Tk()
    tk.Label(reason_win, text='Was the annotation good?').pack()
    tk.Button(reason_win, text='yes', command=hell_yeah).pack()
    tk.Button(reason_win, text='No', command=nope).pack()
    reason_win.mainloop()

    if not yeah_no:
        ask_good_win = tk.Tk()
        ask_good_win.geometry('300x100')
        ask_good_win.bind('<Return>', (lambda event: get_e1()))
        tk.Label(ask_good_win, text='Enter reason annotation is not suitable').pack()
        e1 = tk.Entry(ask_good_win, width=300)
        e1.insert(10, 'Enter reason')
        e1.pack(fill='y')
        tk.Button(ask_good_win, text='accept', command=get_e1).pack()
        e1.select_range(0, 'end')
        ask_good_win.focus_set()
        ask_good_win.after(1, lambda: ask_good_win.focus_force())
        ask_good_win.bind('<FocusIn>', lambda event: e1.select_range(0, 'end'))
        ask_good_win.mainloop()

    # reload usable events again in case someone changed while annotating
    usable_vids = scipy.io.loadmat(usable_events_path + '.mat', struct_as_record=True, squeeze_me=True)

    for i in range(len(usable_vids['usable_events']['EventID'])):
        if Event_ID_Treeview == str(usable_vids['usable_events']['EventID'][i]):
            Event_ID_Treeview_Index = i
            break

    from datetime import datetime

    time = datetime.now()
    time_string = time.strftime('%d/%m/%y %H:%M')
    usable_vids['usable_events']['dateModified'][Event_ID_Treeview_Index] = time_string
    usable_vids['usable_events']['by'][Event_ID_Treeview_Index] = usable_vids['usable_events']['by'][Event_ID_Treeview_Index].replace('No one', '')

    if not annotator_name in usable_vids['usable_events']['by'][Event_ID_Treeview_Index]:
        usable_vids['usable_events']['by'][Event_ID_Treeview_Index] = usable_vids['usable_events']['by'][Event_ID_Treeview_Index] + annotator_name + ', '

    assigned_annotator = usable_vids['usable_events']['assigned_annotator'][Event_ID_Treeview_Index].replace(' ', '')
    if assigned_annotator in usable_vids['usable_events']['by'][Event_ID_Treeview_Index] and yeah_no:
        usable_vids['usable_events']['Status'][Event_ID_Treeview_Index] = 'Annotated'
    else:
        usable_vids['usable_events']['Status'][Event_ID_Treeview_Index] = 'Not Annotated'

    if yeah_no:
        usable_vids['usable_events']['good'][Event_ID_Treeview_Index] = 'yes'
        # usable_vids['usable_events']['reason'][Event_ID_Treeview_Index] = 'None'

        if assigned_annotator == '':
            usable_vids['usable_events']['assigned_annotator'][Event_ID_Treeview_Index] = annotator_name

    else:
        usable_vids['usable_events']['good'][Event_ID_Treeview_Index] = 'no'
        usable_vids['usable_events']['reason'][Event_ID_Treeview_Index] = reason + '// ' + annotator_name

    annotation_data_dict = annotation_data_out.__dict__
    annotation_data_lv_dict = annotation_data_out_sv.__dict__
    annotation_data_adj_dict = annotation_data_out_adj.__dict__

    scipy.io.savemat(annotation_tool_out_path + event_ID +
                     annotator_name + '.mat',
                     {'annotation_data': annotation_data_dict, 'annotation_data_lv': annotation_data_lv_dict,
                      'annotation_data_adj': annotation_data_adj_dict}, long_field_names=True)

    out_file = open(annotation_tool_out_path + event_ID +
                    annotator_name + '.shams',
                    'wb')
    pickle.dump(annotation_data, out_file)
    out_file.close()
    scipy.io.savemat(usable_events_path + '.mat', {'usable_events': usable_vids['usable_events']})