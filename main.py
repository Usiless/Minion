from os import system, mkdir
import time
import cv2
from pathlib import Path
from pygame import mixer
#from playsound import playsound
mixer.init()
mixer.music.load("banana.mp3")
MAX_FOTOS = 5
MAX_FOTOS_TOTALES = 500
TIEMPO_ENTRE_FOTOS = 15
SENSIBILIDAD = 350

def detect_banana(bananas, img, cnt, cnt_tot):
    for (x,y,w,h) in bananas:
        cnt += 1
        cnt_tot += 1
        print((x,y))
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0), 2)
        cv2.putText(img, "BANANA!", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 2, (41, 224, 252), 3, cv2.LINE_AA)
        print("Image "+str(cnt_tot)+" Saved")
        Path('images').mkdir(parents=False, exist_ok=True)
        path=r'images\img'+str(cnt_tot)+'.jpg'
        if cnt == 1:
            mixer.music.play()
        cv2.imwrite(path,img)
        #system("lp -d ZJ-58-2 /home/tercercurso/Desktop/minion/" + path)
        break
    return cnt, cnt_tot, img

def agg_txt(img, prev_frame_time, new_frame_time, tiempo, cnt, cnt_tot):
    font = cv2.FONT_HERSHEY_SIMPLEX
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time

    fps = f"fps: {int(fps)}"
    if tiempo <= 0:
       t =  f"Esperando bananas"
       c =  f"Fotos disponibles: {int(MAX_FOTOS)}"
    else:
       t =  f"Tiempo hasta siguientes fotos: {tiempo}"
       c =  f"Fotos disponibles: {int(MAX_FOTOS) - int(cnt)}"
    m = f"Fotos totales disponibles: {int(MAX_FOTOS_TOTALES) - int(cnt_tot)}"
    cv2.putText(img, t, (7,25), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, c, (7,75), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, fps, (7, 125), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, m, (7, 575), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
    return img, prev_frame_time, new_frame_time

def main():
    time_function_done = time.time()
    #video = cv2.VideoCapture(0)
    video = cv2.VideoCapture('vid/1.mp4')
    banana_cascade = cv2.CascadeClassifier('dataset/BananaCascade.xml')
    prev_frame_time = 0
    new_frame_time = 0
    cnt=0
    cnt_tot=0
    #xd = 1
    while True:
        success,img = video.read()
        #if not success:
        #    video = cv2.VideoCapture(f'vid/{xd}.mp4')
        #    xd+=1
        #    success,img = video.read()
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Si da error acá, es porque termina el video
        bananas = banana_cascade.detectMultiScale(grayImg,50,SENSIBILIDAD)
        keyPressed = cv2.waitKey(1)
        if cnt>=MAX_FOTOS:
            if ((time_function_done + TIEMPO_ENTRE_FOTOS) < time.time()):
                cnt = 0
                time_function_done = time.time()
        else:
            cnt, cnt_tot, img = detect_banana(bananas, img, cnt, cnt_tot)
        tiempo = round (time_function_done + TIEMPO_ENTRE_FOTOS - time.time())
        img = cv2.resize(img, (600, 600))
        img, prev_frame_time, new_frame_time = agg_txt(img, prev_frame_time, new_frame_time, tiempo, cnt, cnt_tot)
        
        cv2.imshow('Banacamara',img)

        if(keyPressed & 0xFF==ord('q') or cnt_tot>=MAX_FOTOS_TOTALES):
            break

    video.release()                                  
    cv2.destroyAllWindows() 

main()