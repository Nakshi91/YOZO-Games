__author__ = "Enakshi Jana"
__copyright__ = ""
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Enakshi Jana"
__email__ = "enu.13jana@gmail.com"
__status__ = "Production"

import cv2
import sys
from keras.models import load_model
import time
import numpy as np
from decimal import Decimal
from model_utils import define_model, model_weights
from gaze_tracking import GazeTracking
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import os,cv2

live_model = load_model("livenessdetect/models/anandfinal.hdf5")

# runs the realtime emotion detection 
def realtime_emotions():
    gaze = GazeTracking()
    # load keras model
    model = define_model()
    model = model_weights(model)
    print('Model loaded')
    # save location for image
    save_loc = 'save_loc/1.jpg'
    # numpy matrix for stroing prediction
    result = np.array((1,7))
    # for knowing whether prediction has started or not
    once = False
    # load haar cascade for face
    faceCascade = cv2.CascadeClassifier(r'haarcascades/haarcascade_frontalface_default.xml')
    # list of given emotions
    EMOTIONS = ['Angry', 'Disgusted', 'Fearful', 'Happy', 'Sad', 'Surprised', 'Neutral']
    # store the emoji coreesponding to different emotions
    emoji_faces = []
    for index, emotion in enumerate(EMOTIONS):
        emoji_faces.append(cv2.imread('emojis/' + emotion.lower()  + '.png', -1))

    # set video capture device , webcam in this case
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 840)  # WIDTH
    video_capture.set(4, 880)  # HEIGHT
    # save current time
    prev_time = time.time()

    # start webcam feed
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        # mirror the frame
        frame = cv2.flip(frame, 1, 0)

        try:
            image = cv2.resize(frame, (128, 128))
            image = image.astype("float") / 255.0
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            (real, fake) = live_model.predict(image)[0]
            if fake > real:
                label = "fake"
                cv2.putText(frame, label, (510, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imshow('Video', frame)
                continue
            else:
                label = "real"
        except:
            continue
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except Exception as E:
            print (E)
            continue

        # find face in the frame
        faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            # required region for the face
            roi_color = frame[y-90:y+h+70, x-50:x+w+50]

            # save the detected face
            try:
                cv2.imwrite(save_loc, roi_color)
            except:
                continue
            # draw a rectangle bounding the face
            cv2.rectangle(frame, (x-10, y-70),
                            (x+w+20, y+h+40), (15, 175, 61), 4)

            # keeps track of waiting time for emotion recognition
            curr_time = time.time()
            # do prediction only when the required elapsed time has passed
            if curr_time - prev_time >=1:
                # read the saved image
                img = cv2.imread(save_loc, 0)

                if img is not None:
                    # indicates that prediction has been done atleast once
                    once = True
                    # resize image for the model
                    img = cv2.resize(img, (48, 48))
                    img = np.reshape(img, (1, 48, 48, 1))
                    # do prediction
                    result = model.predict(img)
                    print(EMOTIONS[np.argmax(result[0])])
                #save the time when the last face recognition task was done
                prev_time = time.time()

            if once == True:
                total_sum = np.sum(result[0])
                # select the emoji face with highest confidence
                emoji_face = emoji_faces[np.argmax(result[0])]
                for index, emotion in enumerate(EMOTIONS):
                    text = str(
                        round(Decimal(result[0][index]/total_sum*100), 2) ) + "%"
                    # for drawing progress bar
                    cv2.rectangle(frame, (100, index * 20 + 10), (100 +int(result[0][index] * 100), (index + 1) * 20 + 4),
                                    (255, 0, 0), -1)
                    # for putting emotion labels
                    cv2.putText(frame, emotion, (10, index * 20 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (7, 109, 16), 2)
                    # for putting percentage confidence
                    cv2.putText(frame, text, (105 + int(result[0][index] * 100), index * 20 + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

                # overlay emoji on the frame for all the channels
                for c in range(0, 3):
                    # for doing overlay we need to assign weights to both foreground and background
                    foreground = emoji_face[:, :, c] * (emoji_face[:, :, 3] / 255.0)
                    background = frame[350:470, 10:130, c] * (1.0 - emoji_face[:, :, 3] / 255.0)
                    frame[350:470, 10:130, c] = foreground + background
            break

        face = gaze.refresh(frame)
        frame = gaze.annotated_frame()
        text = ""
        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"
        cv2.putText(frame, text, (990, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, (147, 58, 31), 2)
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (990, 130), cv2.FONT_HERSHEY_DUPLEX, 0.7, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (990, 165), cv2.FONT_HERSHEY_DUPLEX, 0.7, (147, 58, 31),1)
        cv2.putText(frame, label, (510, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()
