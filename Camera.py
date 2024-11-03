import cv2
import dlib
from scipy.spatial import distance as dist
import numpy as np

def calculate_EAR(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def camera(ear_threshold=0.25, ear_consec_frames=20):
    times_activated = 0
    counter = 0
    is_sleepy = False

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    (lStart, lEnd) = (42, 48)
    (rStart, rEnd) = (36, 42)

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray, 0)

        for face in faces:
            shape = predictor(gray, face)
            shape = np.array([[shape.part(i).x, shape.part(i).y] for i in range(68)])
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            left_ear = calculate_EAR(leftEye)
            right_ear = calculate_EAR(rightEye)
            ear = (left_ear + right_ear) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear < ear_threshold:
                counter += 1
                if counter >= ear_consec_frames:
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    times_activated += 1
                    is_sleepy = True
            else:
                counter = 0

        cv2.imshow('Driver Monitoring', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return times_activated, is_sleepy
