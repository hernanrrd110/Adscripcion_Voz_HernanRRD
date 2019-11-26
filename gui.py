#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from tkinter import Tk, filedialog, Frame, Text, Button, StringVar, Radiobutton
from tkinter import Label, Entry, Listbox, END, BOTTOM, BOTH, TOP
from tkinter import ttk
from revisar_registros import rev_registros, series_fft







class gui(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.folder = ''
        self.create_widgets()

    def create_widgets(self):
        # Barra de directorio
        self.folderPath = StringVar()
        self.lblName = Label(self, text='Folder')
        self.lblName.grid(row=0, column=0)
        self.entPath = Entry(self, textvariable=self.folderPath, width=80)
        self.entPath.grid(row=1, column=0)

        # Botón
        self.btnFind = ttk.Button(self, text="Abrir", command=self.setFolderPath)
        self.btnFind.grid(row=1, column=1)

        # Lista de archivos
        self.lbox = Listbox(self, width=80)
        self.lbox.grid(row=2, column=0)
        self.lbox.bind("<<ListboxSelect>>", self.OnSelect)

        # Label check archivos
        self.check_files = StringVar()
        self.check_files.set('Estado de archivos: sin comprobar')
        self.label_fcheck = Label(self, textvariable=self.check_files)
        self.label_fcheck.grid(row=4, column=0)

        # Plots
        fig1, self.axis1 = plt.subplots(2, 2, num=1, sharex=True)
        fig2, self.axis2 = plt.subplots(2, 2, num=2, sharex=True)

        # Series Temporales
        self.canvas1 = FigureCanvasTkAgg(fig1, self)
        self.canvas1.get_tk_widget().grid(row=5, column=0)
        self.canvas1.draw()
        toolbarFrame1 = Frame(self)
        toolbarFrame1.grid(row=6, column=0)
        toolbar1 = NavigationToolbar2Tk(self.canvas1, toolbarFrame1)
        toolbar1.update()

        # Espectros
        self.canvas2 = FigureCanvasTkAgg(fig2, self)
        self.canvas2.get_tk_widget().grid(row=5, column=1)
        self.canvas2.draw()
        toolbarFrame2 = Frame(self)
        toolbarFrame2.grid(row=6, column=1)
        toolbar2 = NavigationToolbar2Tk(self.canvas2, toolbarFrame2)
        toolbar2.update()

    def setFolderPath(self):
        self.folder = filedialog.askdirectory()
        self.folderPath.set(self.folder)
        self.refresh_files_list()

    # @property
    # def folder_path(self):
        # return self.folderPath.get()

    def refresh_files_list(self):
        self.file_list = []
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                if file.endswith(".mat"):
                    self.lbox.insert(END,os.path.join(root, file))
                    self.file_list.append(os.path.join(root, file))

    def OnSelect(self, event):
        file_ = event.widget.get(event.widget.curselection()[0])
        time_, fft_, snr_ = series_fft(file_)
        self.Plot(time_, fft_, snr_)

    def Plot(self, time, fft, snr):
        for serie, ax1, ax2 in zip(time.columns, self.axis1.flat,
                                   self.axis2.flat):
            ax1.clear()
            ax2.clear()
            ax1.plot(time[serie])
            ax2.plot(fft['f'], fft[serie])
            ax2.set_title('FFT {0} SNR = {1:2.2f}'.format(serie, snr[serie]))
            ax2.set_xlim(-10, 500)
            self.canvas1.draw()
            self.canvas2.draw()


def main():
    root = Tk()
    root.title('Base de datos de registros vocales')
    root.geometry('800x350')
    gui(root)
    root.mainloop()



if __name__ == '__main__':
    main()
