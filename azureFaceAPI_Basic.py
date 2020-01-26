import requests
from PIL import Image
import os
import faceAPIConfig as cnfg
import json
from collections import namedtuple

calibrateFlag = False
boundries = [-999,-999,-999,-999] #right(yaw), left(yaw), top(pitch), bottom(pitch)

def calibrate():
    calibrateFlag = True
    left_image_path = os.path.join('calibration/calibrate-left.png')
    right_image_path = os.path.join('calibration/calibrate-right.png')
    top_image_path = os.path.join('calibration/calibrate-top.png')
    bottom_image_path = os.path.join('calibration/calibrate-bottom.png')
    
    paths = [right_image_path, left_image_path, top_image_path, bottom_image_path]
    
    for i in range(len(paths)):
        tmp = analyze(paths[i])
        if tmp:
            if i < 2:            
                boundries[i] = tmp[0]
            else:
                boundries[i] = tmp[1]
    
    
    # tmp = analyze(right_image_path)
    # boundries[0] = tmp[0]
    # tmp = analyze(left_image_path)
    # boundries[1] = 
    # boundries[1] = analyze(left_image_path)
    # boundries[2] = analyze(top_image_path)
    # boundries[3] = analyze(bottom_image_path)
    

# image_path = os.path.join('/home/brad/Documents/randomFiles/opencv.png')
# image_data = open(image_path, "rb")

def analyze(image_path):

    image_data = open(image_path, "rb")
    subscription_key, face_api_url = cnfg.config();
    returnArr = []

    headers = {'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key}

    params = {
        # 'returnFaceId': 'true',
        # 'returnFaceLandmarks': 'true',
        # 'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion'
        'returnFaceId': 'true',
        'returnFaceAttributes': 'headPose'
    }

    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    response.raise_for_status()
    faces = response.json()
    if not faces:
        return []
    
    returnArr.append(faces[0]['faceAttributes']['headPose']['yaw'])
    returnArr.append(faces[0]['faceAttributes']['headPose']['pitch'])

    return returnArr

def pomodoro_session_analysis():
    if not calibrateFlag:
        calibrate()
    
    #get amount of images in pomodoro
    DIR = 'pomodoro'
    length = 0
    dataSet = []
    withinScreenCount = 0
    #print len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    for name in os.listdir(DIR):
        if os.path.isfile(os.path.join(DIR, name)):
            length += 1
    
    for i in range(length):
        dataSet.append(analyze("pomodoro/capture" + str(i) + ".png"))
    
    for i in range(length):
        if(dataSet == []):
            continue
        elif(dataSet[i] == []):
            continue
        elif(dataSet[i][0] > boundries[0] and dataSet[i][0] < boundries[1] and dataSet[i][1] < boundries[2] and dataSet[i][1] > boundries[3]):
            withinScreenCount += 1
        
    if length == 0:
        return 0.0
    return (withinScreenCount/length)  
    
if __name__ == "__main__":
    print(str(pomodoro_session_analysis() * 100 ) + '%')