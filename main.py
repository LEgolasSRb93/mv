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
        print(circles.shape[0])
        if circles.shape[0] == 18:
            circles = circles[circles[:,0].argsort()]
            circlesFirst = circles[:6]
            circlesFirst = circlesFirst[circlesFirst[:,1].argsort()]
            circlesSecond = circles[6:12]
            circlesSecond = circlesSecond[circlesSecond[:,1].argsort()]
            circlesThird = circles[12:]
            circlesThird = circlesThird[circlesThird[:,1].argsort()]
            circles = np.vstack((circlesFirst, circlesSecond, circlesThird))
            print(circles)
            #  circles[:6] = circlesFirst
            #  circles[6:12] = circlesSecond
            #  circles[12:] = circlesThird
            #  for i in circles[:]:
                #  # draw the outer circle
                #  cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                #  # draw the center circle
                #  cv2.circle(frame,(i[0],i[1]),1,(0,0,255),2)
            count = count + 1
    else:
        circles = np.zeros([18,3], dtype=int)

    return frame,count,circles

### Live stream

cap = cv2.VideoCapture(0)

count = 0
i = 0

circlesAll = np.zeros([18,3], dtype=int)
diodeState = np.zeros([18,1], dtype=int)

while(True):

    ### calibration part
    while count<10:
        #  print(count)
        frame, count, circlesTemp = calibration(cap, count)
        if circlesTemp.shape[0] == 18:
            circlesAll += circlesTemp

    if count == 10:
        circlesAll = np.uint16(np.around(circlesAll/10))
        print(circlesAll)
        count = 100

    #  ### processing part
    # getting one frame from camera input
    ret, frame = cap.read()
    # make gray image
    grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # equilize histogram
    modifiedImg = cv2.equalizeHist(grayImg)
    # smoth equilized image
    smothedImg = cv2.GaussianBlur(modifiedImg, (5, 5), 1.5)
    # get only brightest parts of image
    ret,binImg = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY)

    os.system('clear')

    #  print(circlesAll)
    # ask for
    for i in range(0, 18):
        # ask for every found diode is it white or black (on or off)
        if binImg[circlesAll[i][1],circlesAll[i][0]] == 255:
            diodeState[i] = 1
            #  print("jedna upaljena")
        else:
            diodeState[i] = 0
            #  print("jedna ugasena")
    print(diodeState)

    ### drawing positions of diodes calibration have found
    for i in circlesAll[:]:
        # draw the outer circle
        #  cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center circle
        cv2.circle(frame,(i[0],i[1]),1,(0,0,255),2)


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

