#Libraries
import RPi.GPIO as GPIO
import numpy as np
import imutils
import cv2
import time
import pyttsx3

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

engine = pyttsx3.init()

prototxt ="MobileNetSSD_deploy.prototxt.txt"
model ="MobileNetSSD_deploy.caffemodel"
confThresh = 0.2

CLASSES=["background","aeroplane","bicycle","bird","boat",
       "bottle","bus","car","cat","chair","cow","diningtable",
       "dog","horse","motorbike","person","spectacles","pen","handkerchief",
         "earphones","note book","Mouse","keyboard","TvMonitor","box","sofa","train","steps"]
COLORS=np.random.uniform(0, 225, size=(len(CLASSES), 3))
print("loading model...")
net=cv2.dnn.readNetFromCaffe(prototxt , model)
print("starting camera feed....")
vs=cv2.VideoCapture(0)
time.sleep(0.2)


def camera():
    __,frame=vs.read()
    frame = imutils.resize(frame, width=500)
    (h, w) = frame.shape[:2]
    imResize=cv2.resize(frame, (300, 300))
    blob=cv2.dnn.blobFromImage(imResize,0.007843,(300,300),127.5)
    net.setInput(blob)
    detections=net.forward()
    detShape=detections.shape[2]
    for i in np.arange(0,detShape):
        confidence=detections[0,0,i,2]

        if confidence > confThresh:
            idx=int(detections[0,0,i,1])
            #print("ClassId",detections[0,0,i,1])
            #print(COLORS[idx])
            box=detections[0,0,i,3:7] * np.array([w,h,w,h])
            (startX, startY, endX, endY)= box.astype("int")
            label="{}:{:.2f}%".format(CLASSES[idx],confidence*100)
            cv2.rectangle(frame,(startX,startY),(endX,endY),COLORS[idx],2)
            y=0
            if startY-15>15:
                y=startY-15
            else:
                startY+15
##            cv2.putText(frame,label,(startX, y),
##                        cv2.FONT_HERSHEY_SIMPLEX,0.5,COLORS[idx],2)
            obj="{}".format(CLASSES[idx])
            print(obj)
            cv2.putText(frame,label,(startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,COLORS[idx],2)
            engine.say(obj)
            engine.runAndWait()
##    cv2.imshow("frame",frame)
##    key=cv2.waitKey(1)
##
##    if key==27:
##        break
##vs.release()
##cv2.destroyAllWindows()

while True:
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    print ("Measured Distance = %.1f cm" % distance)
    if distance<20 and distance>3:
        camera()
    else:
        print("NO object in range")

    time.sleep(5)
        
    
