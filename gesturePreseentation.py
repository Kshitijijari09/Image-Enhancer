import cv2
import os
from cvzone.HandTrackingModule import HandDetector
# variables

width, height = 1280, 720
folderPath = "Presentation"
imageNumber = 1
hs, ws = int(120*1), int(213*1)  # small screen on slides of video
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
# camera setup

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)


# Getting the list of images
pathImages = sorted(os.listdir(folderPath), key=len)
# print(pathImages)


# HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)


while True:
    # Import images
    success, img = cap.read()
    pathFullImage = os.path.join(folderPath, pathImages[imageNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands, img = detector.findHands(img)

    cv2.line(img, (0, gestureThreshold),
             (width, gestureThreshold), (0, 255, 0), 10)

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx, cy = hand['center']
        lmList = hand['lmList']
        indexFinger = lmList[8][0], lmList[8][1]

        if cy <= gestureThreshold:  # if hand is at the hand of the face

            # gestureNo1 - Left
            if fingers == [1, 0, 0, 0, 0]:
                print("left")
                if imageNumber > 0:
                    buttonPressed = True
                    imageNumber -= 1

            # gestureNo1 - RIGHT
            if fingers == [0, 0, 0, 0, 1]:
                print("RIGHT")
                if imageNumber < 4:
                    buttonPressed = True
                    imageNumber += 1

        # gestureNo3 - pointer
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

    # Button Pressed iteration
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    # adding webcam image on slides
    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgSmall.shape
    imgCurrent[0:hs, w-ws:w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
