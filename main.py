import os
import cv2
import numpy as np
import pdb

def calibration(cap, count):
    # getting one frame from camera input
    ret, frame = cap.read()
    circles = np.zeros([18,3], dtype=int)
    # switch to gray image
    grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # equilize histogram
    modifiedImg = cv2.equalizeHist(grayImg)
    # smoth equilized image
    smothedImg = cv2.GaussianBlur(modifiedImg, (5, 5), 1.5)
    # get only brightest parts of image
    ret,binImg = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY)
    # find circles in binarized image
    circles = cv2.HoughCircles(binImg,cv2.HOUGH_GRADIENT,1,18,
                              param1=200,param2=10,minRadius=5,maxRadius=10)

    if circles is not None:
        circles = np.uint16(np.around(circles[0]))
        if circles.shape[0] == 18:
            circles = circles[circles[:,0].argsort()]
            circlesFirst = circles[:6]
            circlesFirst = circlesFirst[circlesFirst[:,1].argsort()]
            circlesSecond = circles[6:12]
            circlesSecond = circlesSecond[circlesSecond[:,1].argsort()]
            circlesThird = circles[12:]
            circlesThird = circlesThird[circlesThird[:,1].argsort()]
            circles = np.vstack((circlesFirst, circlesSecond, circlesThird))
            count = count + 1
    else:
        circles = np.zeros([18,3], dtype=int)

    return frame,count,circles

### Live stream
cap = cv2.VideoCapture(0)

cv2.namedWindow('frame')
cv2.moveWindow('frame', 2720, 20)

### Added for substraction
# make structuring element for morph transformation of substracted image
# MORPH_OPEN with MORPH_ELLIPSE, to kill all noise from MOG2 substraction
# (errosion, then dilation), with this killed all noise
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
# getting the changes from live image in comparison with background created
# with MOG2 here. applying the subtractor after every frame taken in loop
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
### Added for substraction

count = 0
i = 0
mode = 1

if mode == 0:
    while(True):
        ### Testing mode
        # only for showing the image from camera, only made for positioning
        # the camera
        ret, frame = cap.read()

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    circlesAll = np.zeros([18,3], dtype=int)
    diodeState = np.zeros([18,1], dtype=int)

    print("Calibration started...")
    while(True):

        ### calibration part
        while count<10:
            frame, count, circlesTemp = calibration(cap, count)
            if circlesTemp.shape[0] == 18:
                circlesAll += circlesTemp

        if count == 10:
            print("Calibration ended...")
            circlesAll = np.uint16(np.around(circlesAll/10))
            print(circlesAll)
            count = 100

        # getting one frame from camera input
        ret, frame = cap.read()

        # use substractor on current frame, and morph on substracted image
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        # find contour features and draw rectangle if there is something
        output = cv2.connectedComponentsWithStats(fgmask, 4, cv2.CV_32S)
        for i in range(output[0]):
            if output[2][i][4] >= 8000 and output[2][i][4] <= 100000:
                cv2.rectangle(frame, (output[2][i][0], output[2][i][1]), (output[2][i][0] + output[2][i][2], output[2][i][1] + output[2][i][3]), (0, 255, 0), 2)

        if output[0] == 1:
            ### processing part
            # if there are no intrusions in current scene
            # make gray image
            grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # equilize histogram
            modifiedImg = cv2.equalizeHist(grayImg)
            # smoth equilized image
            smothedImg = cv2.GaussianBlur(modifiedImg, (5, 5), 1.5)
            # get only brightest parts of image
            ret,binImg = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY)
            os.system('clear')

            print("    ROW  |   COL   |   VALUE")
            # ask for
            for i in range(0, 18):
                # ask for every found diode is it white or black (on or off)
                if binImg[circlesAll[i][1],circlesAll[i][0]] == 255:
                    diodeState[i] = 1
                else:
                    diodeState[i] = 0
                row, col = divmod(i, 6)
                print("   ", row+1, "   |   ", col+1, "   |  ", diodeState[i])

            ### drawing positions of diodes calibration have found
            for i in circlesAll[:]:
                # draw the outer circle
                #  cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center circle
                cv2.circle(frame,(i[0],i[1]),1,(0,0,255),2)
        else:
            os.system('clear')
            print("Intrusion detected!")

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

