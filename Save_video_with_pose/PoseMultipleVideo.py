import cv2
from PoseModuleMultiple import poseDetector
import os
def main():
    input_folder = 'test'
    output_folder = 'output_test'

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all video files in the input folder
    for video_file in os.listdir(input_folder):
        if video_file.endswith('.mov'):  # Assuming the videos have .mp4 extension
            input_path = os.path.join(input_folder, video_file)
            output_path = os.path.join(output_folder, f"processed_{video_file}")


            cap = cv2.VideoCapture(input_path)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            original_fps = cap.get(cv2.CAP_PROP_FPS)

            out = cv2.VideoWriter(output_path, fourcc, original_fps, (406, 720))

            detector = poseDetector()

            while True:
                success, img = cap.read()

                if not success:
                    print("Error: Failed to capture a frame.")
                    break
                if not img.size == 0:
                    resized_img = cv2.resize(img, (406, 720))

                    img = detector.findPose(resized_img)

                    out.write(img)
                cv2.imshow("Image", resized_img)

                cv2.waitKey(20)

            cap.release()
            out.release()
            cv2.destroyAllWindows()







if __name__ == "__main__":
    main()


