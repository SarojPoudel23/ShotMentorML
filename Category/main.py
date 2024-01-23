import cv2
import pandas as pd
from video_df import video_to_df
from predict_category import predict_category
from poseModule import poseDetector
from preProcessing import pre_processing
import time

def poseDetection(category_dictionary, cap):
    processed_frames = []
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    detector = poseDetector()
    # for category, frames in category_dictionary.items():
    #     for img in frames:
    #         if not img.size == 0:
    #             frame_copy = img.copy()
    #             # resized_img = cv2.resize(frame_copy, (406, 720))
    #             resized_img = cv2.resize(frame_copy, (width, height))
    #             resized_img = detector.findPose(resized_img)
    #
    #             # Add category name as text at the top of the frame
    #             cv2.putText(resized_img, f'Category: {category}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
    #                         (255, 255, 255), 2, cv2.LINE_AA)
    #
    #             processed_frames.append(resized_img)
    #             # cv2.imshow("Image", resized_img)
    #             # cv2.waitKey(20)
    #             # out.write(resized_img)
    for index, row in category_dictionary.iterrows():
        frame_number = row['frame_number']
        # Set the video capture to the frame_number
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # Read the frame
        ret, frame = cap.read()

        if not ret:
            print(f"Couldn't read frame for category {row['category']}")
            continue

        # Resize and process the frame
        resized_img = cv2.resize(frame, (width, height))
        resized_img = detector.findPose(resized_img)

        # Add category name as text at the top of the frame
        category = row['category']
        cv2.putText(resized_img, f'Category: {category}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 255, 255), 2, cv2.LINE_AA)

        processed_frames.append(resized_img)
    return processed_frames

def main():

    start = time.time()

    cap = cv2.VideoCapture('Videos/test_9.mov')
    df= pd.DataFrame()

    df = video_to_df(cap)

    df_category = predict_category(df)

    df['category'] = df_category['category']
    # df.to_csv('test_9.csv', index=False)
    category_dictionary = pre_processing(df, cap)
    frames = poseDetection(category_dictionary, cap)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter('y6.mp4', fourcc, original_fps, (width,height))
    # out = cv2.VideoWriter('y.mp4', fourcc, original_fps, (406, 720))

    for frame in frames:
        out.write(frame)
    cap.release()
    end = time.time()
    print(end-start)

if __name__ == "__main__":
    main()