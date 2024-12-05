import cv2
import numpy as np
import dlib
from imutils import face_utils
import pyttsx3
import threading

print("-> Starting <-")
engine = pyttsx3.init()

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"C:\Users\sayak\Desktop\shape_predictor_68_face_landmarks.dat")

sleep = 0
drowsy = 0
active = 0
status=""
color=(0,0,0)



def run():
    try:
        engine.runAndWait()
    except Exception:
        pass
    
def speak(words):
    engine.say(words)
    threading.Thread(target=run).start()
    
def compute(ptA,ptB):
	dist = np.linalg.norm(ptA - ptB)
	return dist

def blinked(a,b,c,d,e,f):
	up = compute(b,d) + compute(c,e)
	down = compute(a,f)
	ratio = up/(2.0*down)

	if(ratio>0.30):
		return 2
	elif(ratio>0.21 and ratio<=0.30):
		return 1
	else:
		return 0

def lip_distance(shape):
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))

    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    distance = abs(top_mean[1] - low_mean[1])
    return distance



while True:
    _, frame = cap.read()
    _, face_frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    yawn_thresh = 28
    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_blink = blinked(landmarks[36],landmarks[37], 
	    landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42],landmarks[43], 
	    landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        distance = lip_distance(landmarks)
        if(left_blink==0 or right_blink==0):
            sleep+=1
            drowsy=0
            active=0
            if(sleep>6):
                status="*** SLEEPING ***"
                speak('You are Sleeping Please Wake Up')
                color = (0,0,255)
                    
        elif(left_blink==1 or right_blink==1):
            sleep=0
            active=0
            drowsy+=1
            if(drowsy>6):
                if(distance > yawn_thresh):
                    status="Drowsy and Yawning"
                    speak('You are Drowsy and Yawning Please Refresh Yourself')
                    color = (0,255,255)                        
                else:
                    status="Drowsy"
                    speak('You are Drowsy Please Refresh Yourself')
                    color = (0,255,255)
        else:
            drowsy=0
            sleep=0
            active+=1
            if(active>6):
                if(distance > yawn_thresh):
                    status="Yawning"
                    speak('You are Yawning Please Refresh Yourself')
                    color = (0,255,255)                        
                else:
                    status="Active"
                    color = (0,255,0)
			
        cv2.putText(frame, status, (100,100), cv2.FONT_HERSHEY_COMPLEX, 1.2, color,3)
		
        for n in range(0, 68):
            (x,y) = landmarks[n]
            cv2.circle(face_frame,(x, y),1,(255, 255, 255),-1)

    cv2.imshow("Face Analysis", frame)
    cv2.imshow("Detector", face_frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
            cv2.destroyAllWindows()
            exit()
