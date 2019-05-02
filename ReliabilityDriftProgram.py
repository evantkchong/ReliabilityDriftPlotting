#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.21
#  in conjunction with Tcl version 8.6
#    Apr 25, 2019 01:29:54 AM +0800  platform: Windows NT

import sys

import tkinter as tk
import tkinter.ttk as ttk

import ReliabilityDriftProgram_support


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    ReliabilityDriftProgram_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    ReliabilityDriftProgram_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x420+660+320")
        top.title("Reliability Drift Plotting and Tracking Program")
        top.configure(background="#ffffff")
        top.configure(highlightbackground="#ffffff")
        top.configure(highlightcolor="black")
        top.configure(takefocus="1")

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.033, rely=0.071, height=56, width=552)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#ffffff")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font="-family {Segoe UI} -size 14 -weight bold")
        self.Label3.configure(foreground="#3d3d3d")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(text='''AMS TAMPINES RELIABILITY DRIFT ANALYSIS PLATFORM''')
        self.Label3.configure(wraplength="400")

        self.database_frame = tk.LabelFrame(top)
        self.database_frame.place(relx=0.117, rely=0.262, relheight=0.226
                , relwidth=0.75)
        self.database_frame.configure(relief='groove')
        self.database_frame.configure(font="-family {Segoe UI} -size 9")
        self.database_frame.configure(foreground="#1e1e1e")
        self.database_frame.configure(labelanchor="n")
        self.database_frame.configure(text='''Database Options''')
        self.database_frame.configure(background="#ffffff")
        self.database_frame.configure(highlightbackground="#d9d9d9")
        self.database_frame.configure(highlightcolor="black")
        self.database_frame.configure(width=400)

        self.drift_calculation_button = tk.Button(self.database_frame)
        self.drift_calculation_button.place(relx=0.511, rely=0.316, height=53
                , width=196, bordermode='ignore')
        self.drift_calculation_button.configure(activebackground="#ececec")
        self.drift_calculation_button.configure(activeforeground="#000000")
        self.drift_calculation_button.configure(background="#ececec")
        self.drift_calculation_button.configure(command=ReliabilityDriftProgram_support.drift_calculation)
        self.drift_calculation_button.configure(disabledforeground="#a3a3a3")
        self.drift_calculation_button.configure(foreground="#000000")
        self.drift_calculation_button.configure(highlightbackground="#d9d9d9")
        self.drift_calculation_button.configure(highlightcolor="black")
        self.drift_calculation_button.configure(pady="0")
        self.drift_calculation_button.configure(relief='flat')
        self.drift_calculation_button.configure(text='''Compute Drift from Database''')
        self.drift_calculation_button.configure(wraplength="110")
        tooltip_font = "TkDefaultFont"
        ToolTip(self.drift_calculation_button, tooltip_font, '''Select the folder for which you would like to calculate drift metrics for.''', delay=0.5)

        self.build_database_button = tk.Button(self.database_frame)
        self.build_database_button.place(relx=0.044, rely=0.316, height=53
                , width=196, bordermode='ignore')
        self.build_database_button.configure(activebackground="#ececec")
        self.build_database_button.configure(activeforeground="#000000")
        self.build_database_button.configure(background="#ececec")
        self.build_database_button.configure(command=ReliabilityDriftProgram_support.build_database)
        self.build_database_button.configure(disabledforeground="#a3a3a3")
        self.build_database_button.configure(foreground="#000000")
        self.build_database_button.configure(highlightbackground="#d9d9d9")
        self.build_database_button.configure(highlightcolor="black")
        self.build_database_button.configure(pady="0")
        self.build_database_button.configure(relief='flat')
        self.build_database_button.configure(text='''Compile Files to Database''')
        self.build_database_button.configure(wraplength="110")
        tooltip_font = "TkDefaultFont"
        ToolTip(self.build_database_button, tooltip_font, '''Click to select an RTO folder to add them to a database for that RTO, sorted by stress type and test type.''', delay=0.5)

        self.plotting_frame = tk.LabelFrame(top)
        self.plotting_frame.place(relx=0.117, rely=0.5, relheight=0.226
                , relwidth=0.75)
        self.plotting_frame.configure(relief='groove')
        self.plotting_frame.configure(font="-family {Segoe UI} -size 9")
        self.plotting_frame.configure(foreground="#1e1e1e")
        self.plotting_frame.configure(labelanchor="n")
        self.plotting_frame.configure(text='''Plotting Options''')
        self.plotting_frame.configure(background="#ffffff")
        self.plotting_frame.configure(highlightbackground="#d9d9d9")
        self.plotting_frame.configure(highlightcolor="black")
        self.plotting_frame.configure(width=400)

        self.folder_save_img_button = tk.Button(self.plotting_frame)
        self.folder_save_img_button.place(relx=0.511, rely=0.316, height=53
                , width=196, bordermode='ignore')
        self.folder_save_img_button.configure(activebackground="#ececec")
        self.folder_save_img_button.configure(activeforeground="#000000")
        self.folder_save_img_button.configure(background="#ececec")
        self.folder_save_img_button.configure(command=ReliabilityDriftProgram_support.folder_save_img)
        self.folder_save_img_button.configure(disabledforeground="#a3a3a3")
        self.folder_save_img_button.configure(foreground="#000000")
        self.folder_save_img_button.configure(highlightbackground="#d9d9d9")
        self.folder_save_img_button.configure(highlightcolor="black")
        self.folder_save_img_button.configure(pady="0")
        self.folder_save_img_button.configure(relief='flat')
        self.folder_save_img_button.configure(text='''Plot All Files In Folder (Save to .jpg)''')
        self.folder_save_img_button.configure(wraplength="150")
        tooltip_font = "TkDefaultFont"
        ToolTip(self.folder_save_img_button, tooltip_font, '''Select a folder containing the files you would like to plot.''', delay=0.5)

        self.file_plot_interactive_button = tk.Button(self.plotting_frame)
        self.file_plot_interactive_button.place(relx=0.044, rely=0.316, height=53
                , width=196, bordermode='ignore')
        self.file_plot_interactive_button.configure(activebackground="#ececec")
        self.file_plot_interactive_button.configure(activeforeground="#000000")
        self.file_plot_interactive_button.configure(background="#ececec")
        self.file_plot_interactive_button.configure(command=ReliabilityDriftProgram_support.file_plot_interactive)
        self.file_plot_interactive_button.configure(disabledforeground="#a3a3a3")
        self.file_plot_interactive_button.configure(foreground="#000000")
        self.file_plot_interactive_button.configure(highlightbackground="#d9d9d9")
        self.file_plot_interactive_button.configure(highlightcolor="black")
        self.file_plot_interactive_button.configure(pady="0")
        self.file_plot_interactive_button.configure(relief='flat')
        self.file_plot_interactive_button.configure(text='''Select Files To Plot (Interactive)''')
        self.file_plot_interactive_button.configure(wraplength="150")
        tooltip_font = "TkDefaultFont"
        ToolTip(self.file_plot_interactive_button, tooltip_font, '''Select files to view an interactive plot without saving them to a database.''', delay=0.5)

        self.TestTypeFrame_2 = tk.LabelFrame(top)
        self.TestTypeFrame_2.place(relx=0.117, rely=0.738, relheight=0.167
                , relwidth=0.75)
        self.TestTypeFrame_2.configure(relief='groove')
        self.TestTypeFrame_2.configure(font="-family {Segoe UI} -size 9")
        self.TestTypeFrame_2.configure(foreground="#1e1e1e")
        self.TestTypeFrame_2.configure(labelanchor="n")
        self.TestTypeFrame_2.configure(text='''Task Progress''')
        self.TestTypeFrame_2.configure(background="#ffffff")
        self.TestTypeFrame_2.configure(highlightbackground="#d9d9d9")
        self.TestTypeFrame_2.configure(highlightcolor="black")
        self.TestTypeFrame_2.configure(width=450)
        
        self.TProgressbar1 = ttk.Progressbar(self.TestTypeFrame_2, 
                                            mode='determinate', 
                                            maximum=15, 
                                            var=ReliabilityDriftProgram_support.progress_var)
        self.TProgressbar1.place(relx=0.044, rely=0.429, relwidth=0.9
                , relheight=0.0, height=22, bordermode='ignore')
        self.TProgressbar1.configure(length="400")

# ======================================================
# Modified by Rozen to remove Tkinter import statements and to receive 
# the font as an argument.
# ======================================================
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# ======================================================
# How to use this class...
#   Copy the file tooltip.py into your working directory
#   import this into the _support python file created by Page
#   from tooltip import ToolTip
#   in the _support python file, create a function to attach each tooltip
#   to the widgets desired. Example:
#   ToolTip(self.widgetname, font, msg='Exit program', follow=False, delay=0.5)
# ======================================================
from time import time, localtime, strftime

class ToolTip(tk.Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """
    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
                 delay=0.2, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          tooltip_font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initalise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The text of the ToolTip is displayed in a Message widget
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                font=tooltip_font,
                aspect=1000).grid()

        # Add bindings to the widget.  This will NOT override
        # bindings that the widget already has
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in miliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        #
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()

# ===========================================================
#                   End of Class ToolTip
# ===========================================================

if __name__ == '__main__':
    vp_start_gui()

