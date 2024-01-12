import cv2
import mediapipe as mp
import numpy as np

class poseDetector():

    def __init__(self, mode=False, modelComplex=1, smoothLandmark=True, enableSegmentation =False,smoothSegmentation = True, detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.modelComplex = modelComplex
        self.smoothLandmark = smoothLandmark
        self.enableSegmentation = enableSegmentation
        self.smoothSegmentation = smoothSegmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.modelComplex, self.smoothLandmark, self.enableSegmentation, self.smoothSegmentation, self.detectionCon, self.trackCon)

    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(imgRGB)

        if results.pose_landmarks:
            if draw:
                landmarks = results.pose_landmarks.landmark

                h, w, c = img.shape

                landmark_points_with_face = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
                landmark_points = []
                for id, lm in enumerate(landmark_points_with_face):
                    lm1 = lm
                    if id == 0:
                        face = [lm1]
                        lm = (0, 0)
                    if id < 9:
                        face.append(lm1)
                        lm = (0, 0)
                    if id == 9 or id == 10:
                        lm = (0, 0)
                        pass

                    landmark_points.append(lm)
                    # print(landmark_points)
                face_array = np.array(face)

                min_x, min_y = np.min(face_array, axis=0)
                max_x, max_y = np.max(face_array, axis=0)

                offset = 12

                min_x -= offset
                min_y -= offset
                max_x += offset
                max_y += offset

                cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

                connections = self.mpPose.POSE_CONNECTIONS

                for connection in connections:
                    try:
                        start_point = landmark_points[connection[0]]
                        end_point = landmark_points[connection[1]]
                        cv2.line(img, start_point, end_point, (255, 255, 255), 2)
                    except IndexError as err:
                        print(str(err))

                for id, lm in enumerate(landmark_points):
                    cv2.circle(img, lm, 5, (255, 255, 255), cv2.FILLED)
        return img