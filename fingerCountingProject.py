import cv2
import os
import time
import handTrackingModule as htm
import pygame

pygame.init()
water_path = "water_audio.opus"
water_sound = pygame.mixer.Sound(water_path)

food_path = "food_audio.opus"
food_sound = pygame.mixer.Sound(food_path)

sleepy_path = "sleepy_audio.opus"
sleepy_sound = pygame.mixer.Sound(sleepy_path)

rest_path = "rest_audio.opus"
rest_sound = pygame.mixer.Sound(rest_path)

fruits_path = "fruits_audio.opus"
fruits_sound = pygame.mixer.Sound(fruits_path)



global_variable = None


def getNumber(ar):
    global global_variable
    s=""
    for i in ar:
       s+=str(ar[i]);
       
    if(s=="00000"):
        return (0)
    elif(s=="01000"):
        water_sound.play()
        pygame.time.delay(int(water_sound.get_length() * 1000))
        global_variable = water_sound
        return(1)
    elif(s=="01100"):
        food_sound.play()
        pygame.time.delay(int(food_sound.get_length() * 1000))
        global_variable = food_sound
        return(2)
    elif(s=="01110"):
        sleepy_sound.play()
        pygame.time.delay(int(sleepy_sound.get_length() * 1000))
        global_variable = sleepy_sound
        return(3)
    elif(s=="01111"):
        rest_sound.play()
        pygame.time.delay(int(rest_sound.get_length() * 1000))
        global_variable = rest_sound
        return(4)
    elif(s=="11111"):
        fruits_sound.play()
        pygame.time.delay(int(fruits_sound.get_length() * 1000))
        global_variable = fruits_sound
        return(5)
    elif(s=="01001"):
        return(6)
    elif(s=="01011"):
        return(7)      

wcam,hcam=640,480
cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pTime=0
detector = htm.handDetector(detectionCon=1)
while True:
    success,img=cap.read()
    img = detector.findHands(img, draw=True )
    lmList=detector.findPosition(img,draw=False)
    #print(lmList)
    tipId=[4,8,12,16,20]
    if(len(lmList)!=0):
        fingers=[]
        #thumb
        if(lmList[tipId[0]][1]>lmList[tipId[0]-1][1]):
                fingers.append(1)
        else :
                fingers.append(0)
        #4 fingers
        for id in range(1,len(tipId)):
            
            if(lmList[tipId[id]][2]<lmList[tipId[id]-2][2]):
                fingers.append(1)
            
            else :
                fingers.append(0)
        
           
        cv2.rectangle(img,(20,255),(170,425),(0,255,0),cv2.FILLED)   
        cv2.putText(img,str(getNumber(fingers)),(45,375),cv2.FONT_HERSHEY_PLAIN,
                                     10,(255,0,0),20)  
        
     
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,0),3)
    cv2.imshow("image",img)
    if(cv2.waitKey(1) & 0xFF== ord('q')):
        break

