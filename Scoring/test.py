import cv2
import numpy as np
import mediapipe as mp
import pandas as pd
import os
import glob

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

def findPose(img, df,frame, columns):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        h, w, c = img.shape

        landmark_points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
        flat_landmarks = [coord for point in landmark_points for coord in point]
        frame_data = {"frame_number": frame, **dict(zip(columns[1:],flat_landmarks))}
        df = pd.concat([df, pd.DataFrame(frame_data, index=[0])], ignore_index=True)

    return img,df


def main():
    columns = ["frame_number", "nose_x", "nose_y", "left_eye_inner_x", "left_eye_inner_y", "left_eye_x",
               "left_eye_y", "left_eye_outer_x", "left_eye_outer_y", "right_eye_inner_x", "right_eye_inner_y",
               "right_eye_x", "right_eye_y", "right_eye_outer_x", "right_eye_outer_y", "left_ear_x", "left_ear_y",
               "right_ear_x", "right_ear_y", "mouth_left_x", "mouth_left_y", "mouth_right_x", "mouth_right_y",
               "left_shoulder_x", "left_shoulder_y", "right_shoulder_x", "right_shoulder_y", "left_elbow_x",
               "left_elbow_y", "right_elbow_x", "right_elbow_y", "left_wrist_x", "left_wrist_y", "right_wrist_x",
               "right_wrist_y", "left_pinky_x", "left_pinky_y", "right_pinky_x", "right_pinky_y", "left_index_x",
               "left_index_y", "right_index_x", "right_index_y", "left_thumb_x", "left_thumb_y", "right_thumb_x",
               "right_thumb_y", "left_hip_x", "left_hip_y", "right_hip_x", "right_hip_y", "left_knee_x", "left_knee_y",
               "right_knee_x", "right_knee_y", "left_ankle_x", "left_ankle_y", "right_ankle_x", "right_ankle_y",
               "left_heel_x", "left_heel_y", "right_heel_x", "right_heel_y", "left_foot_index_x", "left_foot_index_y",
               "right_foot_index_x", "right_foot_index_y"]
    df = pd.DataFrame(columns=columns)

    cap = cv2.VideoCapture('ayush_1.mov')
    frame =0
    while True:
        frame+=1
        success, img = cap.read()

        if not success:
            print("Error: Failed to capture a frame.")
            break
        if not img.size == 0:
            resized_img = cv2.resize(img, (406, 720))

            img, df = findPose(resized_img,df,frame, columns)

    cap.release()
    cv2.destroyAllWindows()
    df.to_csv('ayush_test.csv', index=False)
if __name__ == "__main__":
    main()