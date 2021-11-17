from cv2 import cv2
from mediapipe import mediapipe
import time


class handDetector:
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionConfidence=0.5, trackConfidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionConfidence
        self.trackCon = trackConfidence

        self.mpHands = mediapipe.mediapipe.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mediapipe.mediapipe.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLandMarkers in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandMarkers,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        landMarker_List = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for Id, landMarker in enumerate(myHand.landmark):
                # print(id, landMarker)
                h, w, c = img.shape
                cx, cy = int(landMarker.x * w), int(landMarker.y * h)
                # print(id, cx, cy)
                landMarker_List.append([Id, cx, cy])
                if draw:
                    cv2.putText(img, str(int(Id)), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1,
                                (0, 0, 0), 1)

        return landMarker_List


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detector = handDetector(maxHands=1, detectionConfidence=.5, trackConfidence=.7)
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1,
                    (0, 255, 0), 1)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


if __name__ == "__main__":
    main()
