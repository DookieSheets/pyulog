#! /usr/bin/env python

from tkinter import Tk, Text, TOP, BOTTOM, BOTH, X, N, LEFT, RIGHT, Button, END, INSERT, HORIZONTAL, StringVar, DoubleVar, PhotoImage
from tkinter.ttk import Frame, Label, Entry
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.scrolledtext import ScrolledText

from .ulog2csv import convert_ulog2csv
from .ulog2mat import convert_ulog2mat
from .ulog2kml import convert_ulog2kml

import os

class PyulogGui(Frame):

    def __init__(self):
        super().__init__()
        
        self.input_filename = StringVar()
        self.output_dir = StringVar()
        self.progress_val = DoubleVar()
        
        self.initUI()

        
    def inputBrowseCallback(self):
        input_filename = askopenfilename()
        self.input_filename.set(input_filename)
        
        output_dir = os.path.splitext(input_filename)[:-1][0]

        self.output_entry.delete(0, END)
        self.output_entry.insert(0, output_dir)
        
    def outputBrowseCallback(self):
        output_dir = askdirectory()
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, output_dir)

    def initOutput(self):
        if self.output_dir.get() and not os.path.isdir(self.output_dir.get()):
            print('Creating output directory {:}'.format(self.output_dir.get()))
            os.mkdir(self.output_dir.get())
        
    def clearConsole(self):
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0,END)
        self.text_area.configure(state='disabled')
        
    def consolePrint(self, text):
        self.text_area.configure(state='normal')
        self.text_area.insert(END, text + '\n')
        self.text_area.configure(state='disabled')
        
    def matCallback(self):
        self.clearConsole()
        self.initOutput()
        
        self.consolePrint("Creating MAT...")

        convert_ulog2mat(self.input_filename.get(), None, self.output_dir.get())

        self.consolePrint("Done!")
    
    def kmlCallback(self):
        self.clearConsole()
        self.initOutput()
        
        self.consolePrint("Creating KML...")

        base_name = os.path.basename(self.input_filename.get())[:-4]
        output_file = os.path.join(self.output_dir.get(), base_name) + '.kml'

        convert_ulog2kml(self.input_filename.get(), output_file)

        self.consolePrint("Done!")
    
    def csvCallback(self):
        self.clearConsole()
        self.initOutput()
        
        self.consolePrint("Creating CSVs...")

        convert_ulog2csv(self.input_filename.get(), None, self.output_dir.get(), ',')

        self.consolePrint("Done!")

    def initUI(self):

        self.master.title("PyUlog Gui")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        open_label = Label(frame1, text="Input File")
        open_label.pack(side=LEFT, padx=5, pady=5)
        
        input_button = Button(frame1, text="Browse", command=self.inputBrowseCallback)
        input_button.pack(side=RIGHT, padx=5, pady=5)

        self.input_entry = Entry(frame1, textvariable=self.input_filename)
        self.input_entry.pack(fill=X, padx=5, expand=True)
        

        frame2 = Frame(self)
        frame2.pack(fill=X)

        output_label = Label(frame2, text="Output Directory")
        output_label.pack(side=LEFT, padx=5, pady=5)
        
        output_button = Button(frame2, text="Browse", command=self.outputBrowseCallback)
        output_button.pack(side=RIGHT, padx=5, pady=5)

        self.output_entry = Entry(frame2, textvariable=self.output_dir)
        self.output_entry.pack(fill=X, padx=5, expand=True)
        
        

        frame3 = Frame(self)
        frame3.pack(side=BOTTOM,fill=X, expand=True)

        mat_button = Button(frame3, text="Create MAT", command=self.matCallback)
        mat_button.pack(side=RIGHT, padx=5, pady=5)

        kml_button = Button(frame3, text="Create KML", command=self.kmlCallback)
        kml_button.pack(side=RIGHT, padx=5, pady=5)

        csv_button = Button(frame3, text="Create CSVs", command=self.csvCallback)
        csv_button.pack(side=RIGHT, padx=5, pady=5)


        self.text_area = ScrolledText(self)
        self.text_area.pack(fill=BOTH, pady=5, padx=5, expand=True)
        # self.text_area.insert(END, "Ready...\n")
        self.text_area.configure(state='disabled')

def main():
    root = Tk()
    root.geometry("500x200+500+200")
    
    app = PyulogGui()
    root.mainloop()
