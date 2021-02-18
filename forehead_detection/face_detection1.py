import numpy as np
import cv2
heart_rate_variation_check_flag=0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
arr=[]
import json 
import requests

TOKEN = "648102285:AAF-KX_aHMxkfAfaCEqUc7ObDoUXTiOVrOg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
chat=749919631


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]    
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)
def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    

text, chat = get_last_chat_id_and_text(get_updates())




cap = cv2.VideoCapture(0)
check_status=0 
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
	blur_low = cv2.GaussianBlur(green_channel,(1,1),0)  #(5,5)is sigma x and sigma y(ie, standard deviation)
	blur_high= cv2.GaussianBlur(green_channel,(5,5),0) #(10,10)is sigma x and sigma y(ie, standard deviation)
	#bandpass filter=gaussian noise of high variance - gaussian noise of low variance
	bandpass_filter= blur_high- blur_low
	#plt.subplot(1,2,2)
	#plt.imshow(bandpass_filter)
	#plt.title('Bandpass filter')
	#plt.xticks([])
        #plt.yticks([])
	#plt.show()
	# Find contours
        contours, hierarchy = cv2.findContours(bandpass_filter, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
	mean_gray=np.average(roi_gray)
        mean_color=np.average(roi_color)

	if len(faces)>0:
                print "heart rate="
                print mean_gray
                print mean_color
		if ((mean_color<=80) and (mean_color>=60)):
			print "Normal heart rate"
		#elif ((mean_color<=100) && (mean_color>80)):
		elif ((mean_color<=100) and (mean_color>80)):
			arr.append(mean_color)
			#print "Variation in heart rate="
			check_status=1
	#print arr
	#Sort the list in descending order
        #arr.sort(reverse=True)
        #print "sorted list is"
        #print arr
	if check_status==1:			
		if len(arr)>1 :
    			print arr
			#Sort the list in descending order
			arr.sort(reverse=True)
			print "sorted list is"
			print arr
			check_status=0
			first_peak=arr[0]
			second_peak=arr[1]
			heart_rate_variation=first_peak-second_peak
			print "Variation in heart rate="
			print heart_rate_variation
			rmssd = np.sqrt(np.mean(pow(heart_rate_variation,2)))
			print "rmssd="
			print rmssd
			if rmssd>0.5:
				print "AF"
				send_message("Danger.....",chat)
                                send_message("AF",chat)

		else:
			print arr
                	#Sort the list in descending order
                	arr.sort(reverse=True)
                	print "sorted list is"
                	print arr

			check_status=0
			first_peak=arr[0]
			second_peak=0
			heart_rate_variation=first_peak-second_peak
			print "Variation in heart rate="
                	print heart_rate_variation
			rmssd = np.sqrt(np.mean(pow(heart_rate_variation,2)))
			print "rmssd="
			print rmssd
			if rmssd>0.5:
                                print "AF"
				send_message("Danger.....",chat)
				send_message("AF",chat)

    print "found " +str(len(faces)) +" face(s)"
    
       

    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff

    if k == 27:

        break

cap.release()

cv2.destroyAllWindows()

print arr
