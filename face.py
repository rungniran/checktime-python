import numpy as np, cv2, dlib, os, pickle
#_______________________________________________________________________________________________________________________


path = './imagePersonnel/'
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
print('create file = dataFacePersonnel.pk  loading...')
FACE_DESC = []
FACE_NAME = []


#_________________________________________[:, :, ::-1]______________________________________________________________________________



for fn in os.listdir(path):
    if fn.endswith('.jpg'):
         img = cv2.imread(path + fn)
         dets = detector(img, 1)
         for k, d in enumerate(dets):
              shape = sp (img, d)
              face_desc = model.compute_face_descriptor(img, shape, 4)
              FACE_DESC.append(face_desc)
              print('loading...', fn)
              FACE_NAME.append(fn[:fn.index('_')])
              cv2.imshow('image', img)
              cv2.waitKey(1)
pickle.dump((FACE_DESC, FACE_NAME), open('dataFacePersonnel.pk', 'wb'))

