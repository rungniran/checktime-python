import cv2, numpy as np, dlib, pickle
import datetime
import os
import pymysql


face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
FACE_DESC, FACE_NAME = pickle.load(open('dataFacePersonnel.pk', 'rb')) 
color = (189, 88, 0)
font = cv2.FONT_HERSHEY_SIMPLEX
con = pymysql.connect(host = "localhost", user = "root", password = "", db = "checktime")
cap = cv2.VideoCapture(0)
time = datetime.datetime.now()
datasets = 'database\\' + time.strftime("%A-%d-%m-%Y")
path = os.path.join(datasets)


if not os.path.isdir(path):
    os.mkdir(path)


print(time.strftime("%A/%d/%m/%Y"))



def function_face():
    cv2.putText(frame, names, (x, y-10), font, 0.5, color, 2)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    return


def function_frame():
    cv2.imshow('frame', frame)
    cv2.waitKey(1)



while (True):
    x = input("Attend (y) || Go out = (n) :")
    if x != 'y' or x != 'y':
        pass
    if x == 'y':
        print('Attend')
        while (True):
            _, frame = cap.read()
            times = datetime.datetime.now()
            cv2.line(frame, (0, 20), (650, 20), color, 50)
            cv2.putText(frame, " Attend " + times.strftime("(%d/%m/%Y)  %H:%M"), (7, 30), font, 0.6, (255, 255, 255), 1)
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
                    d = np.array(d)     
                    idx = np.argmin(d)
                    if d[idx] < 0.5:
                        names = FACE_NAME[idx]
                        percent = d[idx]
                        name  = names[10:30]
                        numberPersonnel = names[0:9]
                        day = times.strftime("%d")
                        month = times.strftime("%m")
                        year  = times.strftime("%Y")
                        function_face()
                        mycursor = con.cursor()
                        val = (numberPersonnel, day, month, year)
                        sql = "SELECT * FROM worktime WHERE idListPersonnel = (%s) and day = (%s) and month = (%s) and year = (%s)"
                        mycursor.execute(sql, val)
                        result = mycursor.rowcount
                        if result == 0:
                            cv2.imwrite('%s/%s.jpg' % (path, name), frame)
                            T  = times.strftime("%H:%M")
                            val = (numberPersonnel,  T, day, month, year)
                            sql = "INSERT INTO worktime (idListPersonnel,  T, day, month, year) VALUES (%s, %s, %s, %s, %s)"
                            mycursor.execute(sql, val)
                            print(names, times.strftime("%H:%M %d/%m/%Y"))
                            con.commit()
            function_frame()


    if x == 'n':
        print('get out')
        while (True):
            _, frame = cap.read()
            times = datetime.datetime.now()
            cv2.line(frame, (0, 20), (650, 20), color, 50)
            cv2.putText(frame, " get out " + times.strftime("(%d/%m/%Y)  %H:%M"), (7, 30), font, 0.6, (255, 255, 255), 1)
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
                    d = np.array(d)     
                    idx = np.argmin(d)
                    if d[idx] < 0.5:
                        names = FACE_NAME[idx]
                        percent = d[idx]*100
                        name  = names[10:30]
                        numberPersonnel = names[0:9]
                        day = times.strftime("%d")
                        month = times.strftime("%m")
                        year  = times.strftime("%Y")
                        function_face()
                        mycursor = con.cursor()
                        val = (numberPersonnel, day, month, year)
                        sql = "SELECT * FROM worktime WHERE idListPersonnel = (%s) and day = (%s) and month = (%s) and year = (%s)"
                        mycursor.execute(sql, val)
                        result = mycursor.rowcount
                        row = mycursor.fetchall()
                        if result == 1 and row[0][3] == '' :
                            cv2.imwrite('%s/%s.jpg' % (path, name), frame)
                            idWorkTime = row[0][0]
                            T  = times.strftime("%H:%M ")
                            val = (T, idWorkTime)
                            sql = "UPDATE worktime  SET  Off_T  = (%s) WHERE idWorkTime = (%s)"
                            mycursor.execute(sql, val)
                            con.commit()
                            print(names, times.strftime("%H:%M %d/%m/%Y"))
            function_frame()

