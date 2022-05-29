import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import base64
path = 'images'
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
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            dStr = time_now.strftime('%d:%m:%Y')
            f.writelines(f'{name}, {tStr}, {dStr}')
import cv2
import numpy as np

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def recognise(data_uri):
    while True:
        img = data_uri_to_cv2_img(data_uri)
        facesCurrentFrame = face_recognition.face_locations(img)
        encodesCurrentFrame = face_recognition.face_encodings(img, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = personName[matchIndex].upper()
                return name
                print(name)
                attendance(name)

        if cv2.waitKey(10) == 13:
            break

