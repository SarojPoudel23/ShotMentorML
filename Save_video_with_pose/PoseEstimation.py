import cv2
from PoseModule import poseDetector

def main():
    cap = cv2.VideoCapture('test_9.mov')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    original_fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter('y.mp4', fourcc, original_fps, (406, 720))

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