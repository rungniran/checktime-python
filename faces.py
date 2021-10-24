import cv2, numpy as np, dlib, pickle
import datetime
import os
import pymysql
import keyboard
import sys
import time as reattime



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
mycursor = con.cursor()

if not os.path.isdir(path):
    os.mkdir(path)


def function_querysetup():
    mycursor = con.cursor()
    sql = "SELECT * FROM setup"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    timeinset = result[1]
    timeoutset = result[2]
    return timeinset, timeoutset
    



def function_frame(frame):
    cv2.imshow('frame', frame)
    cv2.waitKey(1)



# def function_attend():
#     _, frame = cap.read()
#     times = datetime.datetime.now()
#     cv2.line(frame, (0, 20), (650, 20), color, 50)
#     cv2.putText(frame, " Attend " + times.strftime("(%d/%m/%Y)  %H:%M"), (7, 30), font, 0.6, (255, 255, 255), 1)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_detector.detectMultiScale(gray, 1.3, 5)
#     for(x, y, w, h) in faces:
#         img = frame[y-10:y+h+10, x-10:x+w+10][:, :, ::-1]
#         dets = detector(img, 1)
#         for k, d in enumerate(dets):
#             shape = sp(img, d)
#             face_desc0 = model.compute_face_descriptor(img, shape, 1)
#             d = []
#             for face_desc in FACE_DESC:
#                 d.append(np.linalg.norm(np.array(face_desc) - np.array(face_desc0)))
#             d = np.array(d)     
#             idx = np.argmin(d)
#             if d[idx] < 0.5:
#                 names = FACE_NAME[idx]
#                 percent = d[idx]
#                 name  = names[10:30]
#                 numberPersonnel = names[0:9]
#                 day = times.strftime("%d")
#                 month = times.strftime("%m")
#                 year  = times.strftime("%Y")
#                 cv2.putText(frame, names, (x, y-10), font, 0.5, color, 2)
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#                 mycursor = con.cursor()
#                 val = (numberPersonnel, day, month, year)
#                 sql = "SELECT * FROM worktime WHERE idListPersonnel = (%s) and day = (%s) and month = (%s) and year = (%s)"
#                 mycursor.execute(sql, val)
#                 result = mycursor.rowcount
#                 if result == 0:
#                     cv2.imwrite('%s/%s.jpg' % (path, name), frame)
#                     T  = times.strftime("%H:%M")
#                     val = (numberPersonnel,  T, day, month, year)
#                     sql = "INSERT INTO worktime (idListPersonnel,  T, day, month, year) VALUES (%s, %s, %s, %s, %s)"
#                     mycursor.execute(sql, val)
#                     print(names, times.strftime("%H:%M %d/%m/%Y"))
#                     con.commit()
#     function_frame(frame)


def function_getout(result, timeoutset, timeinset):
        value = int(result[0:2])
        time_in = int(timeinset[0:2])
        time_out = int(timeoutset[0:2])
        mod = result[6:8]
        _, frame = cap.read()
        times = datetime.datetime.now()
        cv2.line(frame, (0, 20), (650, 20), color, 50)
        if value >= time_in and mod == "AM" :
            cv2.putText(frame, " Attend " + times.strftime("(%d/%m/%Y)  %H:%M"), (7, 30), font, 0.6, (255, 255, 255), 1)
        elif value + 12 >= time_out and mod == "PM" :
            cv2.putText(frame, " Leave work " + times.strftime("(%d/%m/%Y)  %H:%M"), (7, 30), font, 0.6, (255, 255, 255), 1)
        else :
             cv2.putText(frame, " Close Program " + times.strftime("(%d/%m/%Y)  %H:%M"), (7, 30), font, 0.6, (255, 255, 255), 1)
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
                    cv2.putText(frame, names, (x, y-10), font, 0.5, color, 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    val = (numberPersonnel, day, month, year)
                    sql = "SELECT * FROM worktime WHERE idListPersonnel = (%s) and day = (%s) and month = (%s) and year = (%s)"
                    mycursor.execute(sql, val)
                    result = mycursor.rowcount
                    row = mycursor.fetchall()
                    if value >= time_in and mod == "AM" :
                        if result == 0:
                            cv2.imwrite('%s/%s.jpg' % (path, name), frame)
                            T  = times.strftime("%H:%M")
                            val = (numberPersonnel,  T, day, month, year)
                            sql = "INSERT INTO worktime (idListPersonnel,  T, day, month, year) VALUES (%s, %s, %s, %s, %s)"
                            mycursor.execute(sql, val)
                            print(names, times.strftime("%H:%M %d/%m/%Y"), "satatus: Attend")
                            con.commit()
                    elif value + 12 >= time_out and mod == "PM" :
                        if result == 1 and row[0][3] == '' :
                            cv2.imwrite('%s/%s.jpg' % (path, name), frame)
                            idWorkTime = row[0][0]
                            T  = times.strftime("%H:%M ")
                            val = (T, idWorkTime)
                            sql = "UPDATE worktime  SET  Off_T  = (%s) WHERE idWorkTime = (%s)"
                            mycursor.execute(sql, val)
                            con.commit()
                            print(names, times.strftime("%H:%M %d/%m/%Y"),  "satatus: leave work")
        function_frame(frame)


                            
# def function_contoll(result):
#     value = int(result[0:2])
#     time_in = int(timeinset[0:2])
#     time_out = int(timeoutset[0:2])
#     mod = result[6:8]
#     if value >= time_in and mod == "AM" :
#         print('Attend')
#         while (True):
#             function_attend()
#     elif value >= time_out and mod == "PM" :
#         print('get out')
#         while (True):
#             function_getout()

# previous_rows_count = 0
# while True:
#     mycursor.execute("SELECT * FROM setup")
#     rows_count = mycursor.rowcount
#     if rows_count > previous_rows_count:
#         rows = mycursor.fetchall()
#         print (row[1])
   
#     reattime.sleep(1)


while True:
    localtime = reattime.localtime()
    result = reattime.strftime("%I:%M/%p", localtime)
    timeinset, timeoutset = function_querysetup()
    function_getout(result, timeoutset, timeinset)
    reattime.sleep(1)

cap.release()
destroyAllWindows()
  