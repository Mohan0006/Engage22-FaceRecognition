import numpy as np
import cv2
import sklearn
import pickle
from django.conf import settings 
import os

STATIC_DIR = settings.STATIC_DIR


# face detection
face_detector_model = cv2.dnn.readNetFromCaffe(os.path.join(STATIC_DIR,'models/deploy.prototxt.txt'),
                                               os.path.join(STATIC_DIR,'models/res10_300x300_ssd_iter_140000.caffemodel'))
# feature extraction
face_feature_model = cv2.dnn.readNetFromTorch(os.path.join(STATIC_DIR,'models/openface.nn4.small2.v1.t7'))
# face recognition
face_recognition_model = pickle.load(open(os.path.join(STATIC_DIR,'models/machinelearning_face_person_identity.pkl'),
                                          mode='rb'))
# emotion recognition model
emotion_recognition_model = pickle.load(open(os.path.join(STATIC_DIR,'models/machinelearning_face_emotion.pkl'),mode='rb'))


def pipeline_model(path):
    # pipeline model
    img = cv2.imread(path)
    image = img.copy()
    h,w = img.shape[:2]
    # face detection
    img_blob = cv2.dnn.blobFromImage(img,1,(300,300),(104,177,123),swapRB=False,crop=False)
    face_detector_model.setInput(img_blob)
    detections = face_detector_model.forward()
    
    # machcine results
    machinlearning_results = dict(face_detect_score = [], 
                                 face_name = [],
                                 face_name_score = [],
                                 emotion_name = [],
                                 emotion_name_score = [],
                                 count = [],cust_faces=[],loyal_faces=[],sad_faces=[],happy_faces=[],angry_faces=[],suprise_faces=[],disgust_faces=[],neutral_faces=[],fear_faces=[])
    count = 1
    sad_count = 0
    happy_count = 0
    angry_count = 0
    neutral_count = 0
    fear_count = 0
    disgust_count = 0
    suprise_count = 0
    loyal_count = 0
    if len(detections) > 0:
        for i , confidence in enumerate(detections[0,0,:,2]):
            if confidence > 0.7:
                box = detections[0,0,i,3:7]*np.array([w,h,w,h])
                startx,starty,endx,endy = box.astype(int)
                
                cv2.rectangle(image,(startx,starty),(endx,endy),(0,255,0),3)

                # feature extraction
                face_roi = img[starty:endy,startx:endx]
                face_blob = cv2.dnn.blobFromImage(face_roi,1/255,(96,96),(0,0,0),swapRB=True,crop=True)
                face_feature_model.setInput(face_blob)
                vectors = face_feature_model.forward()

                # predict with machine learning
                face_name = face_recognition_model.predict(vectors)[0]
                face_score = face_recognition_model.predict_proba(vectors).max()
                # EMOTION 
                emotion_name = emotion_recognition_model.predict(vectors)[0]
                emotion_score = emotion_recognition_model.predict_proba(vectors).max()
  
                # text_face = '{} : {:.0f} %'.format(face_name,100*face_score)
                # text_emotion = '{} : {:.0f} %'.format(emotion_name,100*emotion_score)
                print(face_score)
                if(face_score>0.44): 
                #  cv2.putText(image,text_face,(startx,starty),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)
                 machinlearning_results['face_name'].append(face_name)
                 machinlearning_results['face_name_score'].append(face_score)
                 loyal_count += 1 
                else:
                 
                 machinlearning_results['face_name'].append("Unknown")
                 machinlearning_results['face_name_score'].append("0")
                 
                # cv2.putText(image,text_emotion,(startx,endy),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),1)


                cv2.imwrite(os.path.join(settings.MEDIA_ROOT,'ml_output/process.jpg'),image)
                cv2.imwrite(os.path.join(settings.MEDIA_ROOT,'ml_output/roi_{}.jpg'.format(count)),face_roi)
                if(emotion_name=='sad'):
                    sad_count += 1
                if(emotion_name=='happy'):
                    happy_count += 1    
                if(emotion_name=='angry'):
                    angry_count += 1 
                if(emotion_name=='disgust'):
                    disgust_count += 1 
                if(emotion_name=='neutral'):
                    neutral_count += 1 
                if(emotion_name=='fear'):
                    fear_count += 1 
                if(emotion_name=='suprise'):
                    suprise_count += 1
                
                            
                machinlearning_results['count'].append(count)
                machinlearning_results['face_detect_score'].append(confidence)
                machinlearning_results['emotion_name'].append(emotion_name)
                machinlearning_results['emotion_name_score'].append(emotion_score) 
        
                
                count += 1
                
    machinlearning_results['cust_faces'].append(count-1)  
    machinlearning_results['loyal_faces'].append(loyal_count)  
    machinlearning_results['sad_faces'].append(sad_count)  
    machinlearning_results['happy_faces'].append(happy_count)  
    machinlearning_results['neutral_faces'].append(neutral_count)  
    machinlearning_results['angry_faces'].append(angry_count)  
    machinlearning_results['suprise_faces'].append(suprise_count)  
    machinlearning_results['fear_faces'].append(fear_count)  
    machinlearning_results['disgust_faces'].append(disgust_count)        
    return machinlearning_results
