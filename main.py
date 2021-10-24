
import cv2
import numpy as np
import winsound
import datetime


now = datetime.datetime.now()
video = cv2.VideoCapture(0)
if (video.isOpened() == False):
    print("Error reading video file")
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
out = cv2.VideoWriter('filename.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)

#print(video.get(cv2.CAP_PROP_FRAME_WIDTH))
#print(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
#video.set(3, 3000)
#video.set(4, 3000)
#print(video.get(3))
#print(video.get(4))
while video.isOpened():
    ret, frame1 = video.read()
    ret, frame2 = video.read()

    #gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = 'width:' + str(video.get(1)) +'height:' + str(video.get(2))
    datet = str(datetime.datetime.now())
    #frame1 = cv2.putText(frame1, text, (10, 50), font, 2, (255, 255, 255), 1, cv2.LINE_AA)
    frame1 = cv2.putText(frame1, datet, (20, 40), font, 2, (25, 25, 25), 3, cv2.LINE_AA)
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame1, contours, -1, (255, 251, 0), 3)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (255, 255, 255), 5)
        #cv2.rectangle(blur, (x, y), (x+w, y+h), (0, 3, 25), 4)
        window_name = 'frame1'
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (350, 350)
        fontScale = 1.3
        color = (37, 150, 190)
        thickness = 4

        image = cv2.putText(frame1, 'VINAY ', org, font,
                            fontScale, color, thickness, cv2.LINE_AA)

        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
    if cv2.waitKey(10) == ord('v'):
        break
    out.write(frame1)

    cv2.imshow(' safe house hidden cam', frame1)
    #cv2.imshow('vinay', blur)
