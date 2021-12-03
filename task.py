import cv2
import numpy as np

def none(args):
    pass

def getShapeName(edges, width, height):
    name = ''
    aspectRatio = float(height) / width

    if edges == 3:
        name = 'Triangle'
    elif edges == 4:
        if 0.9 < aspectRatio < 1.1:
            name = 'Square'
        else: 
            name = 'Rectangle'
    elif edges > 30:
        name = 'Unknown'
    else:
        if 0.9 < aspectRatio < 1.1:
            name = 'Circle'
        else:
            name = 'Ellipse'
    return name

def calcContoursArea(contours, minArea):
    areas = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > minArea:
            areas.append(area)
    list.sort(areas, reverse=True)
    return areas


def defineContours(img, imgContour):
    contours, hierarchy =  cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    minArea = cv2.getTrackbarPos('MinArea', 'Parameters')
    areas = calcContoursArea(contours, minArea)
    for c in contours:
        contourArea = cv2.contourArea(c)
        if contourArea > minArea:
            areaPos = areas.index(contourArea)+1

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.03 * peri, True)

            x, y, w, h = cv2.boundingRect(approx)
            name = getShapeName(len(approx), w, h)
            
            cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(imgContour, name, (x, y-15), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), thickness=2)
            cv2.putText(imgContour, 'Area #{0}'.format(areaPos), (x+w//2-60, y+h//2), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), thickness=2)

            # cv2.drawContours(imgContour, c, -1, (255, 255, 255), 2)
            cv2.drawContours(imgContour, approx, -1, (255, 255, 255), 20)
            cv2.drawContours(imgContour, [approx], -1, (255, 255, 255), 3)


cap = cv2.VideoCapture('video_new.mp4')
cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters', 640, 240)
cv2.createTrackbar('Treshhold1', 'Parameters', 45, 255, none)
cv2.createTrackbar('Treshhold2', 'Parameters', 60, 255, none)
cv2.createTrackbar('MinArea', 'Parameters', 8000, 10000, none)

while True:
    success, img = cap.read()
    imgContour = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (9, 9), 0)

    threshold1 = cv2.getTrackbarPos('Treshhold1', 'Parameters')
    threshold2 = cv2.getTrackbarPos('Treshhold2', 'Parameters')

    imgBrdrs = cv2.Canny(imgBlur, 45, 60)
    kernel = np.ones((5, 5))
    imgClosed = cv2.dilate(imgBrdrs, kernel, iterations=1)

    defineContours(imgClosed, imgContour)

    cv2.imshow('Result', imgContour)

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break