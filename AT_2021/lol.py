import scipy.io
import tkinter as tk
from tkinter import ttk
from time import sleep
data10_disk = 'Y'
projects10_disk = 'W'

annotator_name = 'ahmed'

# load the list with usable events
usable_events_path = projects10_disk + ':\Annotation Tool Common\\usable_events'
usable_vids = scipy.io.loadmat(usable_events_path + '.mat', struct_as_record=True, squeeze_me=True)

# File path win
FilePath = None

Event_ID_Treeview = None
Event_ID_Treeview_Index = None

def treeViewDouble(event):
    global tree, tree_view_master, Event_ID_Treeview
    wtf = tree.selection()
    Event_ID_Treeview = tree.selection()[0]
    print(Event_ID_Treeview)
    tree.unbind('<Double-1>')
    sleep(0.5)
    tree.destroy()
    tree_view_master.destroy()

tree_view_master = tk.Tk()
tree = ttk.Treeview(tree_view_master)
tree['columns'] = ('one', 'two', 'three', 'four', 'five')

tree.heading('#0', text='Event ID', anchor=tk.W)
tree.heading('#1', text='status', anchor=tk.W)
tree.heading('#2', text='Annotated by',  anchor=tk.W)
tree.heading('#3', text='Date modified',  anchor=tk.W)
tree.heading('#4', text='Good', anchor=tk.W)
tree.heading('#5', text='Reason', anchor=tk.W)
tree.column('#5', width=400)
tree.bind('<Double-1>', treeViewDouble)

Ahmed_folder = tree.insert('', '1', text='ahmed')
folder_2 = tree.insert('', '1', text='not screened')

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

    if By == 'No one':
        tree.insert(folder_2, 'end', id=EventID, text=EventID, values=(Status, By, Date, good, Reason))
    else:
        tree.insert(Ahmed_folder, 'end', id=EventID, text=EventID, values=(Status, By, Date, good, Reason))

tree.pack(expand=True, fill='y')
tree_view_master.geometry('1400x700')
tree_view_master.mainloop()
