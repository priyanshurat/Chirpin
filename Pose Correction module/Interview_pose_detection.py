import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
from time import time
import math 

mp_pose=mp.solutions.pose

pose=mp_pose.Pose(static_image_mode=True,min_detection_confidence=0.3,model_complexity=1)

mp_drawing=mp.solutions.drawing_utils
def detectPose(image,pose,display=True):
    output_image=image.copy()
    imageRGB=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    
    results=pose.process(imageRGB)
    height,width,_=image.shape
    landmarks=[]
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image=output_image,landmark_list=results.pose_landmarks,
                                 connections=mp_pose.POSE_CONNECTIONS)
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x*width),int(landmark.y*height),(landmark.z*width)))
    if display:
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        mp_drawing.plot_landmarks(results.pose_world_landmarks,mp_pose.POSE_CONNECTIONS)
    else:
        return output_image,landmarks


def midpoint(point1, point2):
    x =(point1[0]+point2[0]) / 2
    y = (point1[1]+point2[1] )/ 2
    return [x,y]

def calculateAngle(landmark1,landmark2,landmark3):
    #get the required landmarks coordinates
    x1,y1=landmark1
    x2,y2=landmark2
    x3,y3=landmark3
    
    #calculate the angle between the three points
    angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
    
    #check if angle is less than 0
    if angle<0:
        angle+=360
    return angle

def classifyPose(landmarks):
    points = []
    print("LEFT SHOULDER: ",landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value])
    points.append([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0],landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][1]])
    print("RIGHT SHOULDER: ",landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
    points.append([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0],landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][1]])
    print("LEFT ELBOW: ",landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value])
    points.append([landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value][0],landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value][1]])
    print("RIGHT ELBOW: ",landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
    points.append([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value][0],landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value][1]])
    print("LEFT WRIST: ",landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    points.append([landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value][0],landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value][1]])
    print("RIGHT WRIST: ",landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    points.append([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value][0],landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value][1]])
    print("LEFT HIP: ",landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    points.append([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value][0],landmarks[mp_pose.PoseLandmark.LEFT_HIP.value][1]])
    print("RIGHT HIP: ",landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])
    points.append([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value][0],landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value][1]])
    print("LEFT KNEE: ",landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
    points.append([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][0],landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value][1]])
    print("RIGHT KNEE: ",landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
    points.append([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][0],landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value][1]])
    print("LEFT ANKLE: ",landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    points.append([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][0],landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value][1]])
    print("RIGHT ANKLE: ",landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    points.append([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][0],landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value][1]])
    print("NOSE: ",landmarks[mp_pose.PoseLandmark.NOSE.value])
    points.append([landmarks[mp_pose.PoseLandmark.NOSE.value][0],landmarks[mp_pose.PoseLandmark.NOSE.value][1]])


    left_elbow_angle=calculateAngle(points[0],
                                     points[2],
                                     points[4])
    
    right_elbow_angle=calculateAngle(points[1],
                                     points[3],
                                     points[5])
    
    left_shoulder_angle=calculateAngle(points[2],
                                     points[0],
                                     points[6])

    right_shoulder_angle=calculateAngle(points[3],
                                     points[1],
                                     points[7])

    left_hip_angle=calculateAngle(points[0],
                                     points[6],
                                     points[8])

    right_hip_angle=calculateAngle(points[1],
                                     points[7],
                                     points[9])

    left_knee_angle=calculateAngle(points[6],
                                     points[8],
                                     points[10])

    right_knee_angle=calculateAngle(points[7],
                                     points[9],
                                     points[11])

    print("left elbow angle",left_elbow_angle)
    print("right elbow angle: ",right_elbow_angle)
    print("left shoulder angle",left_shoulder_angle)
    print("right shoulder angle: ",right_shoulder_angle)
    print("left hip angle",left_hip_angle)
    print("right hip angle: ",right_hip_angle)
    print("left knee angle",left_knee_angle)
    print("right knee angle: ",right_knee_angle)

    mp = midpoint(points[0],points[1])
    print("Mid Point", mp)
    if (left_elbow_angle >= 180 and left_elbow_angle <= 230) and (right_elbow_angle >= 130 and right_elbow_angle <= 180) and (right_shoulder_angle >= 320 and right_shoulder_angle <= 355) and (left_shoulder_angle >= 5 and left_shoulder_angle <= 40) and (right_knee_angle >= 110 and right_knee_angle <= 150) and (left_knee_angle >= 210 and left_knee_angle <= 250) and (right_hip_angle >= 210 and right_hip_angle <= 250) and (left_hip_angle >= 110 and left_hip_angle <= 150) and (mp[0] - points[12][0] < 50) and abs(midpoint(points[6], points[8])[0] - mp[0] ) < 50:
    # if abs(mp[0] - points[12][0]) < 30 and abs(midpoint(points[6], points[8])[0] - mp[0] ) < 40: 
        print(mp[0] - points[12][0] )
        return (points,True)

    return (points,False)
    
pose_video = mp_pose.Pose(static_image_mode=False,min_detection_confidence=0.5,model_complexity=1)
video = cv2.VideoCapture(0)

while True:
    ret,frame = video.read()
    frame,landmarks=detectPose(frame,pose_video,display=False)
    if landmarks:
        essential_points,flag = classifyPose(landmarks)

        for pt in essential_points:
            cv2.circle(frame, pt, 5, (0,255,0), 2)
        if flag == True:
            cv2.circle(frame, [50,50], 30, (0,255,0), 20)
        else:
            cv2.circle(frame, [50,50], 30, (0,0,255), 20)
    cv2.imshow('Image',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
