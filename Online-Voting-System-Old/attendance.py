import cv2
from cv2 import line
import numpy as np
import face_recognition
import os
from datetime import datetime

path = '../Online-Voting-System/images1'
images = []
personName = []
myList = os.listdir(path)
print(myList)
for cu_Img in myList:
    current_Img = cv2.imread(f'{path}/{cu_Img}')
    images.append(current_Img)
    personName.append(os.path.splitext(cu_Img)[0])
print(personName)


def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = faceEncodings(images)
print("All Encodings Complete!!!")

def attendance(name):
    with open ('../Online-Voting-System/Attendance.csv','r+') as f:
        myDataList= f.readlines()
        nameList=[]
        for line in myDataList:
            entry=line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            current=datetime.now()
            dt_string=current.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dt_string}')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(faces)
    encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = personName[matchIndex].upper()
            print(name)
            y1, x2, y2, y1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, y1*4
            cv2.rectangle(frame, (x1,y1),(x2,y2), (0,255,0), 2)
            cv2.rectangle(frame, (x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame,'press enter to exit',(200,20),cv2.FONT_HERSHEY_COMPLEX,0.75,(255,0,0),2)
            attendance(name)

    cv2.imshow("Camera", frame)
    if cv2.waitKey(10) == 13:
        break
cap.release()
cv2.destroyAllWindows()
