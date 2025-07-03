import cv2 as cv
import time
import os
import HandTrackingModule as htm

cap = cv.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.8)
#import the image
folderPath = 'finger'
myList = os.listdir(folderPath)
#print(myList)
overlayList = []
for imPath in myList:
    image = cv.imread(folderPath + '/' + imPath)
    overlayList.append(image)
#print(overlayList)

tipIds = [ 8, 12, 16, 20]
while True:
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)
    frame = detector.findHands(frame)
    #find the list og landmarks of the hand
    lmList = detector.findPosition(frame, draw=False)
    #print(lmList)
    #we will perform our task when the list is not empty
    if len(lmList) != 0:
        #so to count we can check  whether the point corresponding to the tip is above the points corrsonpding below it
        #this will tell whether the finger is opened or closed
        fingers = []
        #thumb
        if lmList[4][1] < lmList[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(len(tipIds)):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        #print(fingers)
        totalFingers = sum(fingers)
        print(totalFingers)
        cv.putText(frame, str(totalFingers), (110,50), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0),3)

        #to paste the image on the original frame
        h,w,c = overlayList[totalFingers].shape
        frame[0:h,0:w] = overlayList[totalFingers]

    cv.namedWindow("video", cv.WINDOW_NORMAL)
    cv.imshow("video", frame)
    if cv.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv.destroyAllWindows()