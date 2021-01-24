from numpy import expand_dims, argmax
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import cv2


def run_bpo_camera_detector(image, ret, camera_model):
    if not ret:
        return
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = expand_dims(image, 0)
    image = preprocess_input(image)
    pred = argmax(camera_model.predict(image))
    if (pred == 732) or (pred == 759):
        return True
    return False
