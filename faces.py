import cv2, numpy as np, dlib, pickle
import datetime
import os
import pymysql
#_______________________________________________________________________________________________________________
cap = cv2.VideoCapture(0)
times = datetime.datetime.now()
width, height = (400, 400)

datasets = 'database\\' + times.strftime("%A-%d-%m-%Y")
path = os.path.join(datasets)
if not os.path.isdir(path):
    os.mkdir(path)
#_______________________________________________________________________________________________________________________
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
FACE_DESC, FACE_NAME = pickle.load(open('dataFacePersonnel.pk', 'rb'))
#_______________________________________________________________________________________________________________________
print(times.strftime("%A/%d/%m/%Y"))
while (True):
    _, frame = cap.read()
    times = datetime.datetime.now()
    cv2.line(frame, (0, 20), (650, 20), (255, 128, 0), 50)
    cv2.putText(frame, times.strftime(" (%d/%m/%Y) %H:%M:%S"), (7, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in faces:
         img = frame[y-10:y+h+10, x-10:x+w+10][:, :, ::-1]
         dets = detector(img, 1)
         for k, d in enumerate(dets):
              shape = sp(img, d)
              face_desc0 = model.compute_face_descriptor(img, shape, 1)
              d = []
              for face_desc in FACE_DESC:
                   d.append(np.linalg.norm(np.array(face_desc) - np.array(face_desc0)))
                   idx = np.argmin(d)
                   if d[idx] < 0.5:
                        names = FACE_NAME[idx]
                        name  = names[10:30]
                        numberPersonnel = names[0:9]
                        day = times.strftime("%d")
                        month = times.strftime("%m")
                        year  = times.strftime("%Y")
                        cv2.putText(frame, names, (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (250, 0, 0), 1)
                        cv2.imwrite('%s/%s.jpg' % (path, name), frame)
                        con = pymysql.connect(host = "localhost", user = "root", password = "", db = "checktime")
                        mycursor = con.cursor()
                        val = (numberPersonnel, day, month, year)
                        sql = "SELECT * FROM worktime WHERE numberPersonnel = (%s) and day = (%s) and month = (%s) and year = (%s)"
                        mycursor.execute(sql, val)
                        result = mycursor.rowcount
                        if result == 0:
                            T  = times.strftime("%H:%M")
                            val = (numberPersonnel, name, T, day, month, year)
                            sql = "INSERT INTO worktime (numberPersonnel, name, T, day, month, year) VALUES (%s, %s, %s, %s, %s, %s)"
                            mycursor.execute(sql, val)
                            print(names, times.strftime("%H:%M %d/%m/%Y"))
                            con.commit()
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
