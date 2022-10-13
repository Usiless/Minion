from os import system
import time
import cv2
from pygame import mixer
#from playsound import playsound
##mixer.init()
##mixer.music.load("banana.mp3")

video = cv2.VideoCapture(0)
video.set(3, 1000)
video.set(4, 1000)
#video = cv2.VideoCapture('C:/Users/ulise/Downloads/BananaClassifier-master/BananaClassifier-master/video/march28FourObjects.mp4')
banana_cascade = cv2.CascadeClassifier('dataset/BananaCascade.xml')
prev_frame_time = 0
new_frame_time = 0
cnt=1


while True:
    success,img = video.read()
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bananas = banana_cascade.detectMultiScale(grayImg,50,450)
    keyPressed = cv2.waitKey(1)
    for (x,y,w,h) in bananas:
        print((x,y))
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0), 2)
        print("Image "+str(cnt)+" Saved")
        path=r'images\img'+str(cnt)+'.jpg'
        cv2.imwrite(path,img)
        #mixer.music.play()
        #system("lp -d ZJ-58-2 /home/tercercurso/Desktop/minion/" +path)
        cnt +=1
        # if(cnt>=3):   
        #     break
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time

    fps = str(int(fps))
    cv2.putText(img, fps, (7, 70), font, 2, (100, 255, 0), 2, cv2.LINE_AA)
                
    cv2.imshow('live video',img)
    if(keyPressed & 0xFF==ord('q') or cnt >= 5):
        break

video.release()                                  
cv2.destroyAllWindows() 