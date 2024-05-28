import cv2      #Importing OpenCV
import time
import numpy as np      
import handtrackingmodule as htm        
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume        #Module to control volume setting of Windows.
from pynput.mouse import Button, Controller         #Importing module to control the mouse

def hand_function(showCamera,p1,p2):

    mouse = Controller()

    #Resolution Of the screen
    ####################################
    wCam, hCam = 1920, 1080
    ####################################
    
    cap = cv2.VideoCapture(0)
    cap.set(3,wCam)
    cap.set(4,hCam)
    pTime = 0

    detector = htm.handDetector(detectionCon= 0.9,maxHands = 1)         #Setting the detection confidence and specifying the maximum number of hands


    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    #volume.GetMute()
    #volume.GetMasterVolumeLevel()
    volRange = volume.GetVolumeRange()

    minVol = volRange[0]
    maxVol = volRange[1]


    while True:         #To keep the application running
        success, img = cap.read()
        img = detector.findHands(img)       #To find the hands on the screen
        lmList = detector.findPosition(img, draw = False)
        if len(lmList) != 0:
            #print(lmList[4],lmList[8])

            x1, y1 = lmList[p1][1],lmList[p1][2]
            x2, y2 = lmList[12][1], lmList[12][2]
            x3, y3 = lmList[p2][1], lmList[p2][2]
            cx, cy = (x1+x2)//2, (y1+y2)//2

            cv2.circle(img, (x1,y1), 15, (255,0,255),cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1,y1),(x2,y2),(255,0,255),3)

            length = math.hypot(x2-x1,y2-y1)
            length_vol = math.hypot(x3 - x1, y3 - y1)

            vol = np.interp(length_vol,[20,200],[minVol,maxVol])
            volume.SetMasterVolumeLevel(vol, None)

            m_x = np.interp(x3,[0,600],[0,1536])
            m_y = np.interp(y3,[0,400],[0,864])

            mouse.position = (m_x, m_y)

            if length<50:
                mouse.click(Button.left,1)
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)


        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        if showCamera == 1:
            cv2.imshow("Image",img)         #To show the camera output on the screen


        cv2.putText(img,f'FPS: {int(fps)}',(30,60),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        cv2.waitKey(1)
