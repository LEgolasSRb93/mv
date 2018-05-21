import os
import cv2
import numpy as np
import pdb

def calibration(cap, count):
    # getting one frame from camera input
    ret, frame = cap.read()
    while(count<10):
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
                                  param1=200,param2=10,minRadius=5,maxRadius=14)

        if circles is not None:
            circles = np.uint16(np.around(circles[0]))
            circles = circles[circles[:,1].argsort()]
            circlesFirst = circles[:6]
            circlesFirst = circlesFirst[circlesFirst[:,0].argsort()]
            circlesSecond = circles[6:12]
            circlesSecond = circlesSecond[circlesSecond[:,0].argsort()]
            circlesThird = circles[12:]
            circlesThird = circlesThird[circlesThird[:,0].argsort()]
            circles[:6] = circlesFirst
            circles[6:12] = circlesSecond
            circles[12:] = circlesThird
            for i in circles[:]:
                # draw the outer circle
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center circle
                cv2.circle(frame,(i[0],i[1]),1,(0,0,255),2)
            #  os.system('clear')
            #  print(circles)

        print(circles.shape[0])
        if circles.shape[0] == 18:
            count = count + 1
            print(circles)
            #  print(count)
        #  else:
            #  print(count)

        return frame,count,circles

    circles = np.zeros([18,3], dtype=int)
    return frame,count,circles


### Live stream

cap = cv2.VideoCapture(0)

count = 0

circlesAll = np.zeros([18,3], dtype=int)

while(True):

    # getting one frame from camera input
    ret, frame = cap.read()

    # calibration part, first few frames are used for calibration
    #  if i < 5:
        #  circlesAll = calibration(frame)
    #  else:
        #  break
    #  i = i + 1

    #  heightOffset = 80
    #  widthOffset = 150

    ## process image
    #  crop image, to get only part of interest
    #  cropImg = frame[int(height/2-heightOffset):int(height/2+3*heightOffset),
                    #  int(width/2-widthOffset):int(width/2+widthOffset)]

    #  switch to gray image
    grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # equilize histogram
    modifiedImg = cv2.equalizeHist(grayImg)
    # smoth equilized image
    smothedImg = cv2.GaussianBlur(modifiedImg, (5, 5), 1.5)
    # get only brightest parts of image
    ret,binImg = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY)
    # find circles in binarized image
    circlesAll = cv2.HoughCircles(binImg,cv2.HOUGH_GRADIENT,1,10,
                              param1=200,param2=10,minRadius=4,maxRadius=10)[0]
    #  pdb.set_trace()
    if circlesAll is not None:
        #  circles = np.uint16(np.around(circles[0]))
        #  #  print(circles)

        #  circles = circles[circles[:,0].argsort()]
        #  print(circles)
        #  circlesFirst = circles[:6]
        #  circlesFirst = circlesFirst[circles[:,0].argsort()]
        #  circlesSecond = circles[6:12]
        #  circlesSecond = circlesSecond[circles[:,0].argsort()]
        #  circlesThird = circles[12:]
        #  circlesThird = circlesThird[circles[:,0].argsort()]
        # draw circles in original image
        for i in circlesAll[:]:
            # draw the outer circle
            cv2.circle(frame, (i[0],i[1]),i[2],(0,255,0),2)
            # draw the center circle
            cv2.circle(frame,(i[0],i[1]),1,(0,0,255),2)
    #  while count<10:
    #  img, count, circlesTemp = calibration(cap, count)
    #  if circlesTemp.shape[0] == 18:
        #  circlesAll += circlesTemp

    #  if count == 10:
        #  circlesAll = np.uint16(np.around(circlesAll/10))


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# sort found circles
# circles_sort = circles[circles[:,1].argsort()]
# find min and max in one part of found circles
# circles_sort[:6,1].min()
