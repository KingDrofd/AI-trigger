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
        print(lmList[0], lmList[4], lmList[8], lmList[12], lmList[16], lmList[20])
        thumbX, thumbY = lmList[4][1], lmList[4][2]
        indexX, indexY = lmList[8][1], lmList[8][2]
        mFingerX, mFingerY = lmList[12][1], lmList[12][2]
        rFingerX, rFingerY = lmList[16][1], lmList[16][2]
        pinkyX, pinkyY = lmList[20][1], lmList[20][2]
        wristX, wristY = lmList[0][1], lmList[0][2]

        tipSumX = indexX + mFingerX + rFingerX + pinkyX
        tipSumY = indexY + mFingerY + rFingerY + pinkyY

        midPoint_TW_X, midPoint_TW_Y = (tipSumX+wristX) // 5, (tipSumY+wristY) // 5


        thumbMidX, thumbMidY = (thumbX + mFingerX) // 2, (thumbY + mFingerY) // 2
        indexMidX, indexMidY = (indexX + wristX) // 2, (indexY + wristY) // 2
        mFingerMidX, mFingerMidY = (mFingerX + wristX) // 2, (mFingerY + wristY) // 2
        rFingerMidX, rFingerMidY = (rFingerX + wristX) // 2, (rFingerY + wristY) // 2
        pinkyMidX, pinkyMidY = (pinkyX + wristX) // 2, (pinkyY + wristY) // 2

        # Highlighting Tips
        # cv2.circle(img, (thumbX, thumbY), 5, (0, 0, 0), 5)
        # cv2.circle(img, (indexX, indexY), 5, (0, 0, 0), 5)
        # cv2.circle(img, (mFingerX, mFingerY), 5, (0, 0, 0), 5)
        # cv2.circle(img, (rFingerX, rFingerY), 5, (0, 0, 0), 5)
        # cv2.circle(img, (pinkyX, pinkyY), 5, (0, 0, 0), 5)
        cv2.circle(img, (wristX, wristY), 5, (0, 0, 0), 5)
        # cv2.circle(img, (thumbMidX, thumbMidY), 5, (0, 0, 255), 4)
        # cv2.circle(img, (indexMidX, indexMidY), 5, (0, 0, 255), 4)
        # cv2.circle(img, (mFingerMidX, mFingerMidY), 5, (0, 0, 255), 4)
        # cv2.circle(img, (rFingerMidX, rFingerMidY), 5, (0, 0, 255), 4)
        # cv2.circle(img, (pinkyMidX, pinkyMidY), 5, (0, 0, 255), 4)
        cv2.circle(img, (midPoint_TW_X, midPoint_TW_Y), 5, (255, 255, 255), 8)
        # Drawing lines between tips
        cv2.line(img, (thumbX, thumbY), (mFingerX, mFingerY), (0, 0, 0), 2)
        cv2.line(img, (indexX, indexY), (wristX, wristY), (0, 0, 0), 2)
        cv2.line(img, (mFingerX, mFingerY), (wristX, wristY), (0, 0, 0), 2)
        cv2.line(img, (rFingerX, rFingerY), (wristX, wristY), (0, 0, 0), 2)
        cv2.line(img, (pinkyX, pinkyY), (wristX, wristY), (0, 0, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 255, 0), 1)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
