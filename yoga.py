import  cv2, os
import time
import practices11 as pr
import numpy as np
from datetime import datetime


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
bTime = 0

folderPath = 'yoga'                 
myList = os.listdir(folderPath)     #List of image
overlayList= []                     # list after read image
for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)


detector = pr.poseDetector()
seconds_old =0
dem =  0
z =1      #chosen pose number one
def count_time (time):
    global seconds_old, dem,z
    now = datetime.now()
    seconds_new = now.strftime("%S")
    if seconds_new != seconds_old:
        seconds_old = seconds_new
        dem = dem + 1
        if dem == time+1:
            dem =0
            z +=1
            if z==5:
                z=1
    return dem, z


while True:
    success, image = cap.read()
    image = cv2.resize(image, (1280, 720))
    image = cv2.flip(image, 2)
    image = detector.findPose(image,False)
    lmList =detector.findPosition(image,False)
    #wrist = []
    if len(lmList) !=0:
        arm_r = detector.findAngle(image, 12, 14, 16)
        arm_l = detector.findAngle(image, 11, 13, 15)
        upbody_r =detector.findAngle(image,24,12,14)
        upbody_l = detector.findAngle(image, 23, 11, 13)
        knee_r = detector.findAngle(image, 24, 26, 28)
        knee_l = detector.findAngle(image, 23, 25, 27)
        hip_r = detector.findAngle(image, 12, 24, 26)

        
        # Warrior pose
        if z==1:
            h, w, c = overlayList[2].shape
            image[0:h, 0:w] = overlayList[2]

            per_arm_r = np.interp(arm_r, (175, 185), (0, 100))
            per_arm_l = np.interp(arm_l, (177, 180), (0, 100))
            per_upbody_r = np.interp(upbody_r, (90, 105), (0, 100))
            per_upbody_l = np.interp(upbody_l, (270, 280), (100, 0))
            per_knee_r = np.interp(knee_r, (105, 125), (100, 0))
            per_knee_l = np.interp(knee_l, (170, 182), (0, 100))

            if (per_arm_r > 20 and per_arm_l > 20 and per_upbody_r > 20 and per_upbody_l > 20 and
                    per_knee_r > 20 and per_knee_l > 20):
                # h, w, c = overlayList[2].shape
                image[500:700, 1080:1280] = overlayList[3]
                #dem time
                time_hen, z = count_time(5)
                cv2.rectangle(image, (0, 450), (350, 720), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, f"TIME: {int(time_hen) }" +"s", (10, 600),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

            else:
                    dem = 0
        # Tree pose
        elif (z == 2):
            h, w, c = overlayList[1].shape
            image[0:h, 0:w] = overlayList[1]

            per_arm_r = np.interp(arm_r, (25, 80), (100, 0))
            per_arm_l = np.interp(arm_l, (200, 325), (0, 100))
            per_upbody_r = np.interp(upbody_r, (45, 70), (100, 0))  # vai phai
            per_upbody_l = np.interp(upbody_l, (309, 290), (0, 100))
            per_knee_r = np.interp(knee_r, (30, 68), (100, 0))
            per_knee_l = np.interp(knee_l, (170, 190), (0, 100))
            per_hip_r = np.interp(hip_r, (250, 260), (0, 100))
            if (per_arm_r > 20 and per_arm_l > 20 and per_upbody_r > 20 and per_upbody_l > 20 and
                    per_knee_r > 20 and per_knee_l > 20 and per_hip_r > 10):
                image[500:700, 1080:1280] = overlayList[3]
                # dem time
                time_hen, z = count_time(5)
                cv2.rectangle(image, (0, 450), (350, 720), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, f"TIME: {int(time_hen)}" + "s", (10, 600),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

            else:
                dem = 0
         # Triangle Pose
        elif (z == 3):
            h, w, c = overlayList[0].shape
            image[0:h, 0:w] = overlayList[0]

            per_arm_r = np.interp(arm_r, (184, 194), (0, 100))
            per_arm_l = np.interp(arm_l, (154, 178), (100, 0))
            per_upbody_r = np.interp(upbody_r, (80, 94), (0, 100))  # vai phai
            per_upbody_l = np.interp(upbody_l, (274, 300), (100, 0))
            per_knee_r = np.interp(knee_r, (160, 178), (0, 100))
            per_knee_l = np.interp(knee_l, (180, 190), (0, 100))
            per_hip_r = np.interp(hip_r, (136, 186), (100, 0))
            if (per_arm_r > 20 and per_arm_l > 20 and per_upbody_r > 20 and per_upbody_l > 20 and
                    per_knee_r > 20 and per_knee_l > 20 and per_hip_r > 10):
                image[500:700, 1080:1280] = overlayList[3]
                # dem time
                time_hen, z = count_time(5)
                cv2.rectangle(image, (0, 450), (350, 720), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, f"TIME: {int(time_hen)}" + "s", (10, 600),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)

            else:
                dem = 0

        elif (z == 4):
            cv2.rectangle(image, (0, 450), (650, 650), (170, 232, 238), cv2.FILLED)
            cv2.putText(image, f"HOAN THANH" , (10, 600),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 15)


    cv2.imshow("screen", image)

    if cv2.waitKey(5) & 0xff == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
