import cv2
#print(cv2.__version__)
## below is the parameter for 'gframer'
frame = cv2.imread('/home/pi/Desktop/Training/cv.png')
frameSmall=cv2.resize(frame,(320,240))  #resize function

while True:
    cv2.imshow('nanoCam',frameSmall)
##    cv2.moveWindow('nanoCam',100,0)
    if cv2.waitKey(1)==ord('q'):
        break
##cam.release()
cv2.destroyAllWindows()
