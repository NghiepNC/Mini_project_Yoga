import  cv2, os
import time
import practices11 as pr

path_img = "AiTrainer/yoga_tu_the_chien_binh.jpg"
detector = pr.poseDetector()

while (True):
	img = cv2.imread(path_img)
	image = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_AREA)
	image = detector.findPose(image,False)
	lmList =detector.findPosition(image,False)
	if len(lmList) !=0:
		arm_r = detector.findAngle(image, 12, 14, 16)
		arm_l = detector.findAngle(image, 11, 13, 15)
		upbody_r =detector.findAngle(image,24,12,14)
		upbody_l = detector.findAngle(image, 23, 11, 13)
		knee_r = detector.findAngle(image, 24, 26, 28)
		knee_l = detector.findAngle(image, 23, 25, 27)
		hip_r = detector.findAngle(image, 12, 24, 26)
		
	cv2.imshow("hienthi", image)

	if cv2.waitKey(5) & 0xff == ord("q"):
		break
	cv2.imwrite("tuthechienbinh.jpg",image)
cap.release()
cv2.destroyAllWindows()
