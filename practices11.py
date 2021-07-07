import cv2
import time
import mediapipe as mp
import  math


class poseDetector():
    def __init__(self, mode= False, upBody=False, smooth=True,
                    detectioncon = 0.5, trackicon = 0.5):
        self.mode=mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectioncon = detectioncon
        self.trackicon = trackicon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.upBody ,self.smooth ,
                                        self.detectioncon ,self.trackicon )

    def findPose(self, img, draw =True):
        imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results= self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return  img


    def findPosition(self, img, draw =True):
        self.lmList= []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx, cy])
                if draw:
                    if len(self.lmList)!=0:
                        cv2.circle(img, (cx,cy), 3, (255,0,0),cv2.FILLED)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        #xac dinh cac toa do
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        #tinhs toan goc

        # u = [x1 - x2, y1 - y2]
        # v = [x3 - x2, y3 - y2]
        # cosin = ((u[0] * v[0]) + (u[1] * v[1])) / (
        #                 math.sqrt(u[0] * u[0] + u[1] * u[1]) * math.sqrt(v[0] * v[0] + v[1] * v[1]))
        # angle = math.degrees(math.acos(cosin))


        angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        #print(angle)
        if angle < 0:
            angle +=360


        #ve canh tay
        if draw:
            cv2.circle(img, (x1, y1), 10 ,(255,0,0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), 2)
            cv2.line(img,(x1,y1),(x2,y2),(255,255,255),5)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), 2)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 5)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 0, 0), 2)
            cv2.putText(img,str(int(angle))+"do",(x2-100,y2), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),3)
        return angle
    def findStomach(self, img, p1, p2, p3, draw=True):
        #xac dinh cac toa do
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
        #tinhs toan goc

        u = [x1 - x2, y1 - y2]
        v = [x3 - x2, y3 - y2]
        cosin = ((u[0] * v[0]) + (u[1] * v[1])) / (
                        math.sqrt(u[0] * u[0] + u[1] * u[1]) * math.sqrt(v[0] * v[0] + v[1] * v[1]))
        angle = math.degrees(math.acos(cosin))


        #angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        #print(angle)
        # if angle < 0:
        #     angle +=360

        #ve goc
        if draw:
            cv2.circle(img, (x1, y1), 10 ,(255,0,0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), 2)
            cv2.line(img,(x1,y1),(x2,y2),(255,255,255),5)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), 2)
            cv2.line(img, (x2, y2), (x3, y3), (255, 255, 255), 5)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 0, 0), 2)
            cv2.putText(img,str(int(angle))+"do",(x2,y2-50), cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,255),3)
        return angle
    def lenght(self, img, p1, p2):
        #xac dinh cac toa do
        x1, y1 = self.lmList[p1][1:] #khuyu tay
        x2, y2 = self.lmList[p2][1:] #co tay
        u = [x1 - x2, y1 - y2]
        dodai = int(math.sqrt(u[0] * u[0] + u[1] * u[1]))
        return dodai


    #tinh goc lech trong dembbell_shoulder
    def cosin2goc (self, img, p1, p2, p3, draw=True):
        #xac dinh cac toa do
        x1, y1 = p1                 # toa do co tay chuan
        x2, y2 = self.lmList[p2][1:]#toa do khuy tay
        x3, y3 = self.lmList[p3][1:] #toa do co tay
        #tinhs toan goc

        u = [x1 - x2, y1 - y2]
        v = [x3 - x2, y3 - y2]
        cosin = ((u[0] * v[0]) + (u[1] * v[1])) / (
                        math.sqrt(u[0] * u[0] + u[1] * u[1]) * math.sqrt(v[0] * v[0] + v[1] * v[1]))
        angle = math.degrees(math.acos(cosin))
        if draw:
            if angle>15:
                cv2.circle(img, (x1, y1), 10 ,(0, 255, 0), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), 2)
                cv2.line(img,(x1,y1),(x2,y2),(0, 255, 0),5)
                cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
                cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 5)
                cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            

        return  angle



def main():
    cap = cv2.VideoCapture("PoseVideos/1.mp4")
    detector = poseDetector()
    Ptime = 0
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img, draw=False)
        keypoint = 14
        print(lmList[keypoint])
        cv2.circle(img, (lmList[keypoint][1], lmList[keypoint][2]), 10, (255, 0, 255), cv2.FILLED)

        Ctime = time.time()
        fps = 1 / (Ctime - Ptime)
        Ptime = Ctime
        cv2.putText(img, str(int(fps)), (50, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Hien thi", img)
        cv2.waitKey(10)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()
