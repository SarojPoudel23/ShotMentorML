import cv2
from PoseModule import poseDetector

def main():
    cap = cv2.VideoCapture(0)  # Use camera index 0 for default camera
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    original_fps = 30.0  # Set the desired output frame rate (adjust as needed)

    # out = cv2.VideoWriter('output.mp4', fourcc, original_fps, (406, 720))

    detector = poseDetector()

    while True:
        success, img = cap.read()

        if not success:
            print("Error: Failed to capture a frame.")
            break
        if not img.size == 0:
            # resized_img = cv2.resize(img, (1920, 1080))

            img = detector.findPose(img)

            # out.write(img)
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
