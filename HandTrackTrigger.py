import math
from cv2 import cv2
import time
import numpy as np
import HandTrackerModule as htm

camWidth, camHeight = 640, 480

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, camWidth)
cap.set(4, camHeight)
pTime = 0
cTime = 0

detector = htm.handDetector(maxHands=1)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[0], lmList[4], lmList[8], lmList[12], lmList[16], lmList[20])
        thumbX, thumbY = lmList[4][1], lmList[4][2]
        indexX, indexY = lmList[8][1], lmList[8][2]
        mFingerX, mFingerY = lmList[12][1], lmList[12][2]
        rFingerX, rFingerY = lmList[16][1], lmList[16][2]
        pinkyX, pinkyY = lmList[20][1], lmList[20][2]
        wristX, wristY = lmList[0][1], lmList[0][2]

        tipSumX = indexX + mFingerX + rFingerX + pinkyX
        tipSumY = indexY + mFingerY + rFingerY + pinkyY
        tipSumX_avg, tipSumY_avg = tipSumX//4, tipSumY//4

        midPoint_TW_X, midPoint_TW_Y = (tipSumX + wristX) // 5, (tipSumY + wristY) // 5

        thumbMidX, thumbMidY = (thumbX + mFingerX) // 2, (thumbY + mFingerY) // 2

        # Highlighting Tips
        cv2.circle(img, (wristX, wristY), 5, (0, 0, 0), 5)
        cv2.circle(img, (midPoint_TW_X, midPoint_TW_Y), 5, (25, 255, 255), 8)

        # Drawing lines between tips
        cv2.line(img, (thumbX, thumbY), (mFingerX, mFingerY), (0, 0, 0), 2)
        # cv2.line(img, (indexX, indexY), (wristX, wristY), (0, 0, 0), 2)
        # cv2.line(img, (mFingerX, mFingerY), (wristX, wristY), (0, 0, 0), 2)
        # cv2.line(img, (rFingerX, rFingerY), (wristX, wristY), (0, 0, 0), 2)
        # cv2.line(img, (pinkyX, pinkyY), (wristX, wristY), (0, 0, 0), 2)
        cv2.line(img, (tipSumX_avg, tipSumY_avg), (wristX, wristY), (0, 0, 0), 2)

        length = math.hypot(wristX - tipSumX_avg, wristY - tipSumY_avg)
        print(length)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 255, 0), 1)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
