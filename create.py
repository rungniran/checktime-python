import cv2, sys, numpy, os
#_______________________________________________________________________________________________________________________
name = input("Name = ")
numberPersonnel = input("numbelPersonnel = ")
path = os.path.join('imagePersonnel')
if not os.path.isdir(path):
    os.mkdir(path)
width, height = (500, 500)
#_______________________________________________________________________________________________________________________

print(name + numberPersonnel + ' loading ...')
haar_file = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(0)
#_______________________________________________________________________________________________________________________
count = 1
while count < 5:
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    for (x,y,w,h) in faces:
        cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
        face = gray[y-130:y+h+130, x-80:x+w+80][:, :, ::-1]
        face_resize = cv2.resize(face, (width, height))
        cv2.imwrite('%s/%s %s_%s.jpg.jpg' % (path, numberPersonnel, name, count), face_resize)
        print(numberPersonnel + name, count)
    count += 1
    cv2.imshow('OpenCV', im)
    cv2.waitKey(300)
