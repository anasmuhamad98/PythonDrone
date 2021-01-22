import tello
import time
import cv2
import threading
from tkinter import *
from PyQt5.QtWidgets import QApplication

import tello
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import traceback, sys

billy = tello.Tello()
billy.send("command", 1)

# billy.stream_video()
# recvThread = threading.Thread(target=billy.recv)
# recvThread.start()

top = Tk()
top.title('Drone')

distance = 20
degree = 1

def takeOff():
    billy.send("takeoff", 3)


def land():
    billy.send("land", 3)

def updateDistancebar():
    distance = distance_bar.get()
    print ('reset distance to %d' % distance)

def updateDegreebar():
    degree = degree_bar.get()
    print ('reset degree to %d' % degree)

def on_keypress_w(event):
    distance = distance_bar.get()
    print ('up %d m' % distance)
    billy.send("up %d" % distance, 1)

def on_keypress_s(event):
    distance = distance_bar.get()
    print ('down %d m' % distance)
    billy.send("down %d" % distance, 1)

def on_keypress_a(event):
    degree = degree_bar.get()
    print ('ccw %d degree' % degree)
    billy.send("ccw %d" % degree, 1)

def on_keypress_d(event):
    degree = degree_bar.get()
    print ('cw %d degree' % degree)
    billy.send("cw %d" % degree, 1)

def on_keypress_up(event):
    distance = distance_bar.get()
    print ('forward %d m' % distance)
    billy.send("forward %d" % distance, 1)

def on_keypress_down(event):
    distance = distance_bar.get()
    print ('back %d m' % distance)
    billy.send("back %d" % distance, 1)

def on_keypress_left(event):
    distance = distance_bar.get()
    print ('left %d m' % distance)
    billy.send("left %d" % distance, 1)

def on_keypress_right(event):
    distance = distance_bar.get()
    print ('right %d m' % distance)
    billy.send("right %d" % distance, 1)


def openflip():
    panel = Toplevel(top)
    panel.title('Flip')

    flipR = Button(panel, text="Flip Right", command=flipr)
    flipR.pack(side="bottom", fill="both", expand="yes", padx=10, pady=5)

    flipF = Button(panel, text="Flip Forward", command=flipf)
    flipF.pack(side="bottom", fill="both", expand="yes", padx=10, pady=5)

    flipL = Button(panel, text="Flip Left", command=flipl)
    flipL.pack(side="bottom", fill="both", expand="yes", padx=10, pady=5)

    flipB = Button(panel, text="Flip Backward", command=flipb)
    flipB.pack(side="bottom", fill="both", expand="yes", padx=10, pady=5)

def flipf():
    billy.send("flip f", 1)

def flipb():
    billy.send("flip b", 1)


def flipl():
    billy.send("flip l", 1)


def flipr():
    billy.send("flip r", 1)


text0 = Label(top,
              text='This Controller map keyboard inputs to Tello control commands\n'
              'Adjust the trackbar to reset distance and degree parameter',
              font='Helvetica 10 bold')
text0.pack(side='top')

text1 = Label(top, text=
            'W - Move Tello Up\t\t\tArrow Up - Move Tello Forward\n'
            'S - Move Tello Down\t\t\tArrow Down - Move Tello Backward\n'
            'A - Rotate Tello Counter-Clockwise\t\tArrow Left - Move Tello Left\n'
            'D - Rotate Tello Clockwise\t\t\tArrow Right - Move Tello Right',
            justify="left")
text1.pack(side='top')

        # binding arrow keys to drone control
tmp_f = Frame(top, width=100, height=2)
tmp_f.bind('<KeyPress-w>', on_keypress_w)
tmp_f.bind('<KeyPress-s>', on_keypress_s)
tmp_f.bind('<KeyPress-a>', on_keypress_a)
tmp_f.bind('<KeyPress-d>', on_keypress_d)
tmp_f.bind('<KeyPress-Up>', on_keypress_up)
tmp_f.bind('<KeyPress-Down>', on_keypress_down)
tmp_f.bind('<KeyPress-Left>', on_keypress_left)
tmp_f.bind('<KeyPress-Right>', on_keypress_right)
tmp_f.pack(side="bottom")
tmp_f.focus_set()

landind = Button(top, text="Land", command=land)
landind.pack(side="bottom", fill="both", expand="yes", padx=10, pady=5)

flip = Button(top, text="Flip", command=openflip)
flip.pack(side="bottom", fill="both", expand="yes", padx=10, pady=5)

takeoff = Button(top, text="Take Off", command=takeOff)
takeoff.pack(side="bottom", fill="both", expand="yes", padx=10, pady=5)

distance_bar = Scale(top, from_=20, to=500, tickinterval=50, digits=3, label='Distance(cm)',
                                  resolution=0.01)
distance_bar.set(0.2)
distance_bar.pack(side="left")

btn_distance = Button(top, text="Reset Distance", relief="raised", command=updateDistancebar)
btn_distance.pack(side="left", fill="both", expand="yes", padx=10, pady=5)

degree_bar = Scale(top, from_=1, to=360, tickinterval=10, label='Degree',)
degree_bar.set(30)
degree_bar.pack(side="right")

btn_distance = Button(top, text="Reset Degree", relief="raised", command=updateDegreebar)
btn_distance.pack(side="right", fill="both", expand="yes", padx=10, pady=5)




# Used for going back
previ = 0

# directional counts
upcount = 0
downcount = 0
forwardcount = 0
backwardcount = 0
leftcount = 0
rightcount = 0

# Flip counts
flpl = 0
flpr = 0
flpf = 0
flpb = 0

# Rotation counts
clkw = 0
cclkw = 0

# Check if override button is clicked
override_chck = 0

# Check if takeoff button is clicked
takeoff_chck = 0

persweepclicked = 0

# Check if manual control is on or not
manucontrol = 1

referarr = []
referarr2 = []
print("Drone is in Manual Mode.")

class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)


class Ui_MainWindow(object):

    def __init__(self, *args, **kwargs):
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    # Stop in Air
    def stopinair(self):
        if manucontrol == 1 or override_chck == 1:
            billy.send("stop", 3)
            print("Drone is paused in air.")
        else:
            print("You are in Autonomous mode.")

    # ----------------------------- Overriding perimeter sweep and also going back to the place where drone stopped------------------------------
    def override(self):
        global referarr2
        referarr2=[]
        if persweepclicked == 0:
            print("Nothing to override.")
            return
        global referarr
        global override_chck
        global previ
        if override_chck == 0:
            override_chck = 1
            return
        elif override_chck == 1:
            override_chck = 0
            print()
            #print("i was " + str(previ))
            print("Going back to the point where perimeter sweep was overriden.")
            referarr.reverse()
            for r in range(0, len(referarr)):
                if referarr[r] == "u":
                    self.down()
                elif referarr[r] == "d":
                    self.up()
                elif referarr[r] == "l":
                    self.right()
                elif referarr[r] == "r":
                    self.left()
                elif referarr[r] == "f":
                    self.back()
                elif referarr[r] == "b":
                    self.forward()
                elif referarr[r] == "clkw":
                    self.ccw()
                elif referarr[r] == "cclkw":
                    self.cw()
                elif referarr[r] == "flpf":
                    self.flipback()
                elif referarr[r] == "flpb":
                    self.flipforward()
                elif referarr[r] == "flpl":
                    self.flipright()
                elif referarr[r] == "flpr":
                    self.flipleft()
            print("Reached the point where perimeter sweep was overriden.")
            referarr = []
            print()
            print("Continuing perimeter sweep.")
            self.persweepcont_exec()

    # ------------------------------------------------Perimeter sweep-------------------------------------------------------
    def persweep(self):
        global persweepclicked
        persweepclicked = 1
        global previ
        global referarr2
        global referarr
        print()
        print("Manual Mode switched off.")
        print("Manual Controls locked.")
        print()
        print("Autonomous Mode started.")
        global manucontrol
        if manucontrol == 1:
            print()
            print("Going back to the starting point.")
            referarr2.reverse()
            for r in range(0, len(referarr2)):
                if referarr2[r] == "u":
                    self.down()
                elif referarr2[r] == "d":
                    self.up()
                elif referarr2[r] == "l":
                    self.right()
                elif referarr2[r] == "r":
                    self.left()
                elif referarr2[r] == "f":
                    self.back()
                elif referarr2[r] == "b":
                    self.forward()
                elif referarr2[r] == "clkw":
                    self.ccw()
                elif referarr2[r] == "cclkw":
                    self.cw()
                elif referarr2[r] == "flpf":
                    self.flipback()
                elif referarr2[r] == "flpb":
                    self.flipforward()
                elif referarr2[r] == "flpl":
                    self.flipright()
                elif referarr2[r] == "flpr":
                    self.flipleft()
            print("Reached the starting point.")
            referarr2 = []
            print(referarr2)
            print()

        manucontrol -= 1
        # Travel to/from starting checkpoint 0 from/to the charging base
        frombase = ["forward", 50, "ccw", 150]
        tobase = ["ccw", 150, "forward", 50]

        # Flight path to Checkpoint 1 to 5 and back to Checkpoint 0 sequentially
        checkpoint = [[1, "cw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
                      [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]

        print("Perimeter sweep started.")

        # Send the takeoff command
        if takeoff_chck == 0:
            billy.send("takeoff", 7)

        print("\n")

        # Start at checkpoint 1 and print destination
        print("From the charging base to the starting checkpoint of sweep pattern.\n")

        billy.send(frombase[0] + " " + str(frombase[1]), 4)
        billy.send(frombase[2] + " " + str(frombase[3]), 4)

        print("Current location: Checkpoint 0 " + "\n")

        # Billy's flight path
        for i in range(len(checkpoint)):
            QApplication.processEvents()
            if override_chck == 1:
                print("Manual mode initiated.")
                manucontrol = 1
                return
            if i == len(checkpoint) - 1:
                print("Returning to Checkpoint 0. \n")
                previ = 0

            billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
            billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

            print("Arrived at current location: Checkpoint " + str(checkpoint[i][0]) + "\n")

            previ = i
            time.sleep(4)

        # Reach back at Checkpoint 0
        print("Complete sweep. Return to charging base.\n")
        billy.send(tobase[0] + " " + str(tobase[1]), 4)
        billy.send(tobase[2] + " " + str(tobase[3]), 4)

        # Turn to original direction before land
        print("Turn to original direction before land.\n")
        billy.send("cw 180", 4)

        # Land
        billy.send("land", 3)

        # Close the socket
        # billy.sock.close() [Causes error as it is not connected with real drone]
        print("Perimeter sweep completed successfully.")
        print("Autonomous mode switched off.")
        print("You are now in manual mode.")
        manucontrol += 1
        persweepclicked = 0
        referarr2=[]
        referarr=[]

    def persweep_exec(self):
        # Pass the function to execute
        worker = Worker(self.persweep)  # Any other args, kwargs are passed to the run function

        # Execute
        self.threadpool.start(worker)

    def persweepcontinue(self):
        global referarr
        global referarr2
        global previ
        # Travel to/from starting checkpoint 0 from/to the charging base
        frombase = ["forward", 50, "ccw", 150]
        tobase = ["ccw", 150, "forward", 50]

        # Flight path to Checkpoint 1 to 5 and back to Checkpoint 0 sequentially
        checkpoint = [[1, "cw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
                      [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]
        i = previ
        print("Current location: Checkpoint " + str(checkpoint[i][0]) + "\n")
        i += 1
        # Billy's flight path
        while i < len(checkpoint):
            #print("test i" + str(i))
            if i == len(checkpoint) - 1:
                print("Returning to Checkpoint 0. \n")

            billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
            billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

            print("Arrived at current location: Checkpoint " + str(checkpoint[i][0]) + "\n")
            i += 1
            time.sleep(4)

        # Reach back at Checkpoint 0
        print("Complete sweep. Return to charging base.\n")
        billy.send(tobase[0] + " " + str(tobase[1]), 4)
        billy.send(tobase[2] + " " + str(tobase[3]), 4)

        # Turn to original direction before land
        print("Turn to original direction before land.\n")
        billy.send("cw 180", 4)

        # Land
        billy.send("land", 3)

        # Close the socket
        # billy.sock.close() [Causes error as it is not connected with real drone]
        print("Perimeter sweep completed successfully.")
        print("Autonomous mode switched off.")
        print("You are now in manual mode.")
        global persweepclicked
        persweepclicked = 0
        referarr2=[]
        referarr=[]

    def persweepcont_exec(self):
        # Pass the function to execute
        worker = Worker(self.persweepcontinue)  # Any other args, kwargs are passed to the run function

        # Execute
        self.threadpool.start(worker)

    # -------------------------------------------emergency------------------------------
    def emergency(self):
        if manucontrol == 1 or override_chck == 1:
            # Send the emergency stop command
            billy.send("emergency", 3)
            print("Emergency mode initiated, motor stopped.")
        else:
            print("You are in Autonomous mode.")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(200, 200)
        MainWindow.setStyleSheet("background-color:rgb(248, 249, 255)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.peribtn = QtWidgets.QPushButton(self.centralwidget)
        self.peribtn.setGeometry(QtCore.QRect(10, 10, 180, 50))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.peribtn.setFont(font)
        self.peribtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.peribtn.setStyleSheet("background-color: rgb(0, 170, 255);\n"
                                   "color: white;\n"
                                   "border-radius: 20px;")
        self.peribtn.setObjectName("peribtn")
        self.overrbtn = QtWidgets.QPushButton(self.centralwidget)
        self.overrbtn.setGeometry(QtCore.QRect(10, 70, 180, 50))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.overrbtn.setFont(font)
        self.overrbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.overrbtn.setStyleSheet("background-color: rgb(255, 206, 56);\n"
                                    "color: white;\n"
                                    "border-radius: 20px;")
        self.overrbtn.setObjectName("overrbtn")
        self.emergstopbtn = QtWidgets.QPushButton(self.centralwidget)
        self.emergstopbtn.setGeometry(QtCore.QRect(10, 130, 180, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.emergstopbtn.setFont(font)
        self.emergstopbtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.emergstopbtn.setStyleSheet("background-color: rgb(255, 32, 32);\n"
                                        "color: white;\n"
                                        "border-radius: 20px;")
        self.emergstopbtn.setObjectName("emergstopbtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # -------------------------------Connecting persweep method to persweep button---------------------------------
        self.peribtn.clicked.connect(self.persweep_exec)
        # -------------------------------Connecting emergency method to emergstop button-------------------------------
        self.emergstopbtn.clicked.connect(self.emergency)

        # -------------------------------Connecting override method to override button--------------------------
        self.overrbtn.clicked.connect(self.override)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tello Drone Control Panel"))
        self.peribtn.setText(_translate("MainWindow", "PERIMETER SWEEP"))
        self.overrbtn.setText(_translate("MainWindow", "OVERRIDE ROUTE"))
        self.emergstopbtn.setText(_translate("MainWindow", "Stop"))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    top.mainloop()
    sys.exit(app.exec_())
