subscription_key = "dda0a6860604416bb0d5594a8f067e60" #DSFace API
face_api_url = 'https://conuhacksfaceapi.cognitiveservices.azure.com/face/v1.0/detect'


def config():
    print("Call Config")
    return subscription_key, face_api_url