import requests
from PIL import Image
import os
import faceAPIConfig as cnfg
import json
from collections import namedtuple

image_path = os.path.join('/home/brad/Documents/randomFiles/opencv.png')
image_data = open(image_path, "rb")

subscription_key, face_api_url = cnfg.config();

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
#print(faces)
file = open("face.json", "w")
file.write(json.dumps(faces))
file.close()
print(faces[0]['faceAttributes']['headPose']['yaw'])
#print(faces[0])















################OLD CODE###################

##Now that we have the face data as a JSON, turn it into an object
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(faces): return json.loads(faces, object_hook=_json_object_hook)

listOfFaces = []
object1 = json2obj(json.dumps(faces))
#print(object1['headPose']['yaw'])
# listOfFaces.append(object1)

# print(listOfFaces[0].headPose)

# for idx, item in enumerate(listOfFaces):
#     print(listOfFaces[idx])
