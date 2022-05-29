import cv2
from cv2 import namedWindow

cam=cv2.VideoCapture(0)

cv2.namedWindow("Screenshot app")

img_counter=0
while True:
    ret, frame = cam.read()

    if not ret:
        print("Failed")
        break

    cv2.imshow("test", frame)

    k=cv2.waitKey(1)
    if k%256 == 27:
        print("Escape hit, closing")
        break

    elif k%256 == 32:
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name,frame)
        print("Screenshot taken")
        img_counter+=1

cam.release()

cam.destroyAllWindows()