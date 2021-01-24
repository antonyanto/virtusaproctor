from flask import Flask, render_template, redirect, url_for, Response
from camera import VideoCamera
import cv2
import os
import signal
import joblib
from multiprocessing import Value, Process
import keyboard
from audio_part import record_audio
from mouth_opening_detector import run_mouth_open, initialize_mouth_model
from face_spoofing import run_face_spoof
from face_detector import get_face_detector, find_faces
from face_landmarks import get_landmark_model
from person_and_phone import run_person_model, initialize_model
from bpo_camera_detector import run_bpo_camera_detector
from tensorflow.keras.models import load_model


app = Flask(__name__)
start = True

if start:
    file = open("test.txt", "w")
    file.close()
    file = open("final.txt", "w")
    file.close()
    file = open("common_words.txt", 'w')
    file.close()
    start = False


def bpo_model_start(img, ret):

    if not ret:
        return

    img, shape = initialize_mouth_model(img, ret, face_model, landmark_model)

    if keyboard.is_pressed('r'):
        for i in range(100):
            for k, (p1, p2) in enumerate(outer_points):
                d_outer[k] += shape[p2][1] - shape[p1][1]
            for k, (p1, p2) in enumerate(inner_points):
                d_inner[k] += shape[p2][1] - shape[p1][1]
        d_outer[:] = [x / 100 for x in d_outer]
        d_inner[:] = [x / 100 for x in d_inner]
        return True, img
    else:
        return False, img


def bpo_run_model(image, ret):
    if not distance:
        print("Please Restart the Service...")
        return
    else:
        global attempts, run, audio_process
        if attempts > 0:

            if not ret:
                return

            mobile, person_count = run_person_model(image, ret, yolo)
            if person_count > 1:
                attempts -= 1
                print("More than One Person is detected. Attempts Left : ", attempts)
                detected=Image.fromarray((image.copy()))
                detected.save("C://Users//Admin//BPOPerson"+str(attempts)+".png")

            elif person_count == 0:
                print("Warning No Person Detected...")


            if mobile:
                print("Mobile Phone Detected...")
                attempts -= 1
                detected=Image.fromarray((image.copy()))
                detected.save("C://Users//Admin//BPOMobile"+str(attempts)+".png")

            mouth_open = run_mouth_open(
                image, ret, face_model, landmark_model, font, outer_points,
                d_outer, inner_points, d_inner
            )

            if mouth_open:
                if status.value == 1:
                    print("Mouth Open, Started Recording...")
                    detected=Image.fromarray((image.copy()))
                    detected.save("C://Users//Admin//BPOMouth"+str(attempts)+".png")
                    if (audio_process.is_alive() is not True) and (run is False):
                        status.value = 0
                        audio_process.start()
                        run = True

                    elif (audio_process.is_alive() is not True) and (run is True):
                        audio_process.terminate()
                        audio_process = Process(target=record_audio, args=(status,))
                        status.value = 0
                        audio_process.start()

                else:
                    print("Mouth Open, But not Recording...")
            spoof = run_face_spoof(image, ret, find_faces, clf, face_model)

            if (len(spoof) > 0) and (all(spoof) is False):
                print("Human Face...")
            else:
                print("Spoofed Face or Lightining Condition must be improved...")


            is_camera = run_bpo_camera_detector(image, ret, camera_model)
            if is_camera:
                print("Camera Found...")
                detected=Image.fromarray((image.copy()))
                detected.save("C://Users//Admin//BPOCamera"+str(attempts)+".png")

        else:
            print("Must Exit")
            os.kill(audio_process.pid, signal.SIGTERM)

        if attempts == 0:
            print("Number of Attempts Exceeded. Closing Exam...")
            return None
    return image


@app.route("/", methods=["GET", "POST"])
def root():
    return redirect(url_for("home"))


@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("bpo_index.html")


@app.route("/home/bpo", methods=["GET", "POST"])
def bpo():
    return Response(initialize(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


def initialize(camera):

    while True:
        ret, image = camera.get_frame()
        try:
            init, image = bpo_model_start(image, ret)
        except TypeError:
            break
        if init:
            global distance
            distance = True
            break
        else:
            display = cv2.imencode(".jpg", image)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + display + b'\r\n\r\n')

    while True:
        ret, image = camera.get_frame()
        output = bpo_run_model(image, ret)
        if output is not None:
            display = cv2.imencode(".jpg", output)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + display + b'\r\n\r\n')
        else:
            camera.__del__()
            break


if __name__ == '__main__':
    attempts = 3
    distance = False
    run = False

    status = Value('i', 1)
    audio_process = Process(target=record_audio, args=(status,))

    outer_points = [[49, 59], [50, 58], [51, 57], [52, 56], [53, 55]]
    d_outer = [0] * 5
    inner_points = [[61, 67], [62, 66], [63, 65]]
    d_inner = [0] * 3
    font = cv2.FONT_HERSHEY_SIMPLEX

    class_names = [c.strip() for c in open("models/classes.TXT").readlines()]
    left = [36, 37, 38, 39, 40, 41]
    right = [42, 43, 44, 45, 46, 47]

    face_model = get_face_detector()
    landmark_model = get_landmark_model()
    clf = joblib.load('models/face_spoofing.pkl')
    model_initialized = False

    yolo = initialize_model()
    camera_model = load_model("models\\mobilenetv2_model.h5")

    app.run()
