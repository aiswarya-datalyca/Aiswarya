import numpy as np

import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


cap = cv2.VideoCapture(0)
while 1:

    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.5, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        roi_gray = gray[y:y+h, x:x+w]

        roi_color = img[y:y+h, x:x+w]
	convert_to_rgb_format = cv2.cvtColor(roi_gray, cv2.COLOR_GRAY2RGB)
	#cv2.imshow("color", convert_to_rgb_format) 
	

	#extract green channel
	green_channel = convert_to_rgb_format[:,:,0]
	green_channel = convert_to_rgb_format[:,:,2]


	cv2.imshow("Extracted green channel", green_channel)
    print "found " +str(len(faces)) +" face(s)"
   
    


    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff

    if k == 27:

        break

cap.release()

cv2.destroyAllWindows()


