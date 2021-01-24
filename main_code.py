from flask import Flask, render_template, Response, redirect, url_for,abort
import keyboard
from upload import upload_files
import numpy as np
from camera import VideoCamera
import joblib
from multiprocessing import Process, Value
import cv2
import os
import time
from bpo_main_code import bpo_model_start,bpo_run_model
from PIL import Image
from person_and_phone import initialize_model, run_person_model
from mouth_opening_detector import initialize_mouth_model, run_mouth_open
from face_detector import get_face_detector, find_faces
from face_landmarks import get_landmark_model, detect_marks
from face_spoofing import run_face_spoof
from head_pose_estimation import run_head_position
from eye_tracker import run_eye_tracker
from audio_part import record_audio
import os
import signal
import warnings
warnings.filterwarnings("ignore")
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


def model_start(img, ret):

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


def run_model(image, ret):

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
                detected.save("malpractice//Person"+str(attempts)+".png")

            elif person_count == 0:
                print("Warning No Person Detected...")

            elif mobile:
                attempts -= 1
                print("Mobile Detected. Attempts Left : ", attempts)
                detected=Image.fromarray((image.copy()))
                detected.save("malpractice//Mobile"+str(attempts)+".png")

            mouth_open = run_mouth_open(
                image, ret, face_model, landmark_model, font, outer_points,
                d_outer, inner_points, d_inner
            )

            if mouth_open:
                if status.value == 1:
                    print("Mouth Open, Started Recording...")
                    detected=Image.fromarray((image.copy()))
                    detected.save("malpractice//Mouth"+str(attempts)+".png")
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
                print("Spoofed Face")

            eye_position = run_eye_tracker(
                image, ret, face_model, find_faces, detect_marks,  landmark_model, left, right, kernel
            )

            if eye_position is not None:
                if len(eye_position) > 1:
                    print(eye_position)

            head_position = run_head_position(
                image, ret, font, find_faces, face_model, detect_marks, landmark_model
            )

            if len(head_position) > 1:
                print(head_position)

        else:
            print("Must Exit")
            os.kill(audio_process.pid, signal.SIGINT)

        if attempts == 0:
            print("Number of Attempts Exceeded. Closing Exam...")
            return None
    return image


@app.route('/', methods=["GET", "POST"])
def root():
    return render_template("index.html")
@app.route('/Register', methods=["GET", "POST"])
def Register():
    return render_template("Register.html")
@app.route('/choice', methods=["GET", "POST"])
def choice():
    return render_template("choose.html")

@app.route('/instruction', methods=["GET", "POST"])
def instruction():
    return render_template("instruction.html")
@app.route('/instructions', methods=["GET", "POST"])
def instructions():
    return render_template("instructions.html")
@app.route('/dash', methods=["GET", "POST"])
def dash():
    return render_template("dash.html")
@app.route('/test', methods=["GET", "POST"])
def test():
    return render_template("quiz.html")
@app.route('/testb', methods=["GET", "POST"])
def testb():
    return render_template("dashbpo.html")
@app.route('/testq', methods=["GET", "POST"])
def testq():
    return render_template("work.html")
@app.route('/upload', methods=["GET", "POST"])
def upload():
    upload()
    return "Hello World"

@app.route('/home', methods=['GET', "POST"])
def home():
    return render_template('exam_index.html')


@app.route('/home/exam_proctor', methods=["GET", "POST"])
def exam_proctor():
    return Response(initialize(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')
def initialize(camera):

    while True:
        ret,image = camera.get_frame()
        try:
            init, image = model_start(image, ret)
        except TypeError:
            break
        if init:
            global distance
            distance = True
            break
        else:
            pass
    start_time=time.time()
    while True:
        ret,image = camera.get_frame()
        current_time=time.time()
        if (attempts == 0) or ((current_time - start_time) > 25):
            if len(os.listdir("malpractice")) == 0:
                print("No Malpractice Images Found")
                camera.__del__()
                abort(404)
            else:
                print("Uploading Files to the Cloud")
                upload_files()
                camera.__del__()
                abort(404)

        else:
            try:
                output = run_model(image, ret)
            except cv2.error:
                pass
            if output is not None:
                pass
            else:
                camera.__del__()
                break


    print("Moving Forward...")
@app.route('/home/bpo_proctor', methods=["GET", "POST"])
def bpo_proctor():
    return Response(initi(VideoCamera()))
def initi(camera):

    while True:
        frame, ret, image = camera.get_frame()
        try:
            init, image = bpo_model_start(image, ret)
        except TypeError:
            break
        if init:
            global distance
            distance = True
            break
        else:
            pass

    while True:
        frame,ret, image = camera.get_frame()
        if attempts == 0:
            camera.__del__()
            redirect(url_for("Register"))
        else:
            try:
                output =bpo_run_model(image, ret)
            except cv2.error:
                pass
            if output is not None:
                pass
            else:
                camera.__del__()
                break


    print("Moving Forward...")



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

    left = [36, 37, 38, 39, 40, 41]
    right = [42, 43, 44, 45, 46, 47]
    kernel = np.ones((9, 9), np.uint8)

    yolo = initialize_model()
    face_model = get_face_detector()
    landmark_model = get_landmark_model()
    clf = joblib.load('models/face_spoofing.pkl')
    model_initialized = False

    app.run(debug=True)
