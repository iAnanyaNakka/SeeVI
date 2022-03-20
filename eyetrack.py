"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
#import pandas as pd
import cv2
from gaze_tracking import GazeTracking
c=0
with open("file.txt",'w') as f:
    f.write(' '.join(["lx","ly","rx","ry","view","frame no.","\n"]))

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
lf=[]
rh=[]
#df=pd.DataFrame()
while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    lf.append(left_pupil)
    rh.append(right_pupil)
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("output", frame)
    print("lf:::::::::::::",lf) 

    #print("rh**************",rh[-1])
    #df.to_csv("output.csv")
    #df['lf']=lf 
    #df.to_csv("lf.csv")
    c+=1
    print("hi:::::::::::::::::::::::::::::::::::::::::::::::::::::::",type(left_pupil))
    if left_pupil is not None and right_pupil is not None:
        with open("data_eye.txt",'a') as f:
            f.write(' '.join([str(list(left_pupil)[0]),str(list(left_pupil)[1]),str(list(right_pupil)[0]),str(list(right_pupil)[1]),str(text),str(c),"\n"]))
 
    
    if cv2.waitKey(1) == 27:
        break 
#webcam.release()
#cv2.destroyAllWindows()
