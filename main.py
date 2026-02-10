import cv2
import numpy as np
import mediapipe as mp
import math

def FindAngle(img,p1,p2,p3,lmList,draw=True):
    x1,y1 = lmList[p1][1:]
    x2,y2 = lmList[p2][1:]
    x3,y3 = lmList[p3][1:]
    
    
    # açı hesaplamak için:
    angle = math.degrees(math.atan2(y3-y2 , x3-x2) - math.atan2(y1-y2 , x1-x2))
    
    if angle < 0:
        angle +=360
    
    if draw:
        # noktalar arası çizgiler
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)
        cv2.line(img,(x2,y2),(x3,y3),(0,0,255),3)
        
        # noktaları belirtmek için içi dolu sarı noktalar
        cv2.circle(img,(x1,y1),10,(0,255,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(0,255,255),cv2.FILLED)
        cv2.circle(img,(x3,y3),10,(0,255,255),cv2.FILLED)
        
        # daha güzel görünmesi için içi dolu noktaların etrafıniçi boş noktalar:
        cv2.circle(img,(x1,y1),15,(0,255,255)) #15 yani biraz daha kalın bu sayede etrafında duruyor
        cv2.circle(img,(x2,y2),15,(0,255,255))
        cv2.circle(img,(x3,y3),15,(0,255,255))
        
        # açıyı yazdır
        cv2.putText(img, str(int(angle)), (x2-40 , y2+40),cv2.FONT_HERSHEY_PLAIN,2,(0,255,255),2)
    return angle


    
cap = cv2.VideoCapture("video1.mp4")

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

dir = 0
count=0

while True:
    success,img = cap.read()
    
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = pose.process(imgRGB)
    
    lmList = []
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)
        
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,_ = img.shape
            cx,cy = int(lm.x*w), int(lm.y*h)
            
            lmList.append([id,cx,cy])
    print(lmList)
    
    if len(lmList) != 0:
        
        # şınav çektiğini anlayabilmek için 11,13 ve 15 numaralı noktaların birbiiyle yaptığı açıyı buldurup ondan faydalanacaz.
        angle = FindAngle(img, 11, 13, 15, lmList)
        per = np.interp(angle,(185,245),(0,100)) #185 derece kalktığı, 245 derece ise yere eğildiği zaman ortaya çıkan bizim sınır alabileceğimiz açı değerleri. Bu değerleri de 0 v 100 olarak belirledik. interpolasyon yaptık.
        print(angle)
        
        # eğildiği zaman yarım şınav say dedik
        if per == 100:
            if dir ==0:
                count+=0.5
                dir=1 
        
        # kalktığı zaman yarım şınav daha ekledik
        if per == 0:
            if dir ==1: #yani üstteki hareketi yapmış bitirmişse, yerde bekliyor da olabilir. buna karşı önlem
                count+=0.5
                dir=0 #dir dediğimiz şey hareketi tamamlayıp tamamlamadığını kontrol ettiğimiz değişken
            
        cv2.putText(img, str(int(count)), (45,125), cv2.FONT_HERSHEY_PLAIN, 10,(255,0,0),10)
    
    cv2.imshow("image",img)
    cv2.waitKey(25)