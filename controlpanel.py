import tello
import time
import cv2
import threading
from tkinter import *

billy = tello.Tello()
billy.send("command", 1)

# billy.stream_video()
# recvThread = threading.Thread(target=billy.recv)
# recvThread.start()

top = Tk()
top.title('Drone')

distance = 0.1
degree = 0.1

def autoplan():
    # Travel to/from starting checkpoint 0 from/to the charging base
    frombase = ["forward", 50, "ccw", 150]
    tobase = ["ccw", 150, "forward", 50]

    # Flight path to Checkpoint 1 to 5 and back to Checkpoint 0 sequentially
    checkpoint = [[1, "cw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
                  [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]
    # Put Tello into command mode

    billy.send("command", 3)
    # Send the takeoff command
    print(billy.send("takeoff", 7))

    print("\n")

    # Start at checkpoint 1 and print destination
    print("From the charging base to the starting checkpoint of sweep pattern.\n")

    billy.send(frombase[0] + " " + str(frombase[1]), 4)
    billy.send(frombase[2] + " " + str(frombase[3]), 4)

    print("Current location: Checkpoint 0 " + "\n")

    # Billy's flight path
    for i in range(len(checkpoint)):
        if i == len(checkpoint)-1:
            print("Returning to Checkpoint 0. \n")

        billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
        billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

        print("Arrived at current location: Checkpoint " +
              str(checkpoint[i][0]) + "\n")
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


def takeOff():
    billy.send("takeoff", 3)


def land():
    billy.send("land", 3)

def updateDistancebar():
    distance = distance_bar.get()
    print ('reset distance to %.2f' % distance)

def updateDegreebar():
    degree = degree_bar.get()
    print ('reset degree to %d' % degree)

def on_keypress_w(event):
    distance = distance_bar.get()
    print ('up %.2f m' % distance)
    billy.send("up %.2f" % distance, 1)

def on_keypress_s(event):
    distance = distance_bar.get()
    print ('down %.2f m' % distance)
    billy.send("down %.2f" % distance, 1)

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
    print ('forward %.2f m' % distance)
    billy.send("forward %.2f" % distance, 1)

def on_keypress_down(event):
    distance = distance_bar.get()
    print ('back %.2f m' % distance)
    billy.send("back %.2f" % distance, 1)

def on_keypress_left(event):
    distance = distance_bar.get()
    print ('left %.2f m' % distance)
    billy.send("left %.2f" % distance, 1)

def on_keypress_right(event):
    distance = distance_bar.get()
    print ('right %.2f m' % distance)
    billy.send("right %.2f" % distance, 1)


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
            'A - Rotate Tello Counter-Clockwise\tArrow Left - Move Tello Left\n'
            'D - Rotate Tello Clockwise\t\tArrow Right - Move Tello Right',
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

autoplane = Button(top, text="Auto Plane", command=autoplan)
autoplane.pack(side="bottom", fill="both", expand="yes", padx=10, pady=5)

distance_bar = Scale(top, from_=0.02, to=5, tickinterval=0.01, digits=3, label='Distance(m)',
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

top.mainloop()
