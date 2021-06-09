import cv2
import numpy as np
import pyautogui
import tkinter as tk
import threading
from time import perf_counter
from PIL import Image
from mss import mss
from multiprocessing import Queue
import os
import random
from string import ascii_lowercase

class Recorder:
    def __init__(self,outputFilename = "recorded.mp4"):
        self.keepRecording = False
        self.save_in_every = 1
        self.start = self.current = perf_counter()
        # distroy any pre exiting windows
        cv2.destroyAllWindows()

        self.outputFilename = outputFilename
        splited = os.path.splitext(self.outputFilename)
        self.outputFilename = "".join([splited[0]+"_0",splited[1]])

        if os.path.exists(self.outputFilename):
            splited = os.path.splitext(self.outputFilename)
            self.outputFilename =self.outputFilename.replace('_0',"".join([random.choice(ascii_lowercase) for _ in range(4)])+"_0")

        # moniter size 
        self.SCREEN_SIZE = pyautogui.size()
        self.monitor = {
            "top" : 0,
            "left" : 0,
            "width" : self.SCREEN_SIZE[0],
            "height" : self.SCREEN_SIZE[1]
            }
    
    def __enter__(self):
        return self
    
    def __exit__(self,a,b,c):
        self.keepRecording = False
        self.root.quit()
        try :
            # close it now
            while not self.queue.empty(): 
                try:
                    self.queue.get(timeout=0.001)
                except:
                    pass
            self.queue.close()
        except :
            pass

    def run(self):
        self.root = tk.Tk()
        self.root.geometry('300x300')
        self.root.title("Screen Recorder")
        labelFPSSetting = tk.Label(text = "Select FPS option")
        labelFPSSetting.place(x=90, y=40)


        self.fpsSettings = tk.ttk.Combobox(self.root)
        self.fpsSettings['values'] = (10, 15, 20, 25, 30,35,40, 45,50,55, 60)
        self.fpsSettings.current(4)
        self.fpsSettings.place(x=90, y=80,width = 115)


        self.btnStartRecording = tk.Button(self.root,
                                    text = "Start Recording",
                                    command = self.startRecording )
        self.btnStartRecording.place(x=90, y=120)

        self.btnStopRecording = tk.Button(self.root, 
                                    text = "Stop Recording",
                                    command = self.stopRecording)
        self.btnStopRecording.place(x=90,y=160)
        self.btnStopRecording["state"] = "disabled"

        self.root.mainloop()

    def updateFileName(self):
        """update the file name if exits"""
        splited = os.path.splitext(self.outputFilename)
        integer = int(splited[0][-1])
        if integer == 0 :
            num = '0'
        else:
            num = str(integer +1)
        self.outputFilename =  splited[0][:-1] + num + splited[1]

    def startRecording(self):
        # notmatize the name of the file
        self.updateFileName()

        self.btnStartRecording["state"] = "disabled"
        self.btnStopRecording["state"] = "normal"
        self.keepRecording = True
        # minimize the panel window 
        self.root.iconify()
        self.recordScreen()

    def stopRecording(self):
        self.keepRecording = False
        self.btnStartRecording["state"] = "normal"
        self.btnStopRecording["state"] = "disabled"

    def recordScreen(self):
        """read and save the screen at the given FPS"""
        output = cv2.VideoWriter(self.outputFilename,
                    cv2.VideoWriter_fourcc(*"mp4v"),
                    float(self.fpsSettings.current()*5+10),
                    self.SCREEN_SIZE)
        sct = mss()
        self.queue = Queue()
        rec = threading.Thread(target=self.ScreenReader,
                        args=[sct,self.queue], daemon=True)
        rec.start()
        scr  = threading.Thread(target=self.ScreenWriter,
                        args=[output,self.queue], daemon=True)
        scr.start()

    def ScreenReader(self, sct, queue):
        """read the screen and pass to writter in thread"""
        # print(f"Frames saved.")
        while self.keepRecording == True:
            queue.put(
                np.array(
                    sct.grab(self.monitor)
                    )
                )
            if (self.current-self.start) > self.save_in_every :
                self.start = self.current
            self.current = perf_counter()
        queue.put(None)

    def ScreenWriter(self, output, queue):
        """save the frames to the video file"""
        while self.keepRecording == True:
            img = queue.get()
            if img is None:
                output.release()
                break
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            output.write(img)
        output.release()

    @classmethod
    def runner(cls):
        with cls() as cl:
            cl.run()

if __name__ == "__main__":
    Recorder.runner()