import pyrebase
import os
def upload_files():
    config={
       "apiKey": "AIzaSyCuwZLvFYIXqrO9IhiD_wUYSS6xKz287G4",
        "authDomain": "proctor-96511.firebaseapp.com",
        "databaseURL": "https://proctor-96511-default-rtdb.firebaseio.com",
        "projectId": "proctor-96511",
        "storageBucket": "proctor-96511.appspot.com",
        "messagingSenderId": "782036150781",
        "appId": "1:782036150781:web:78d84200dcd02327995194",
        "measurementId": "G-BHS76LQV6Z"

    }
    firebase=pyrebase.initialize_app(config)
    storage=firebase.storage()
    for (i, img) in enumerate(os.listdir("malpractice")):
        path_on_cloud = "Image/Proctor" + str(i)+".png"
        storage.child(path_on_cloud).put("malpractice\\"+img)
    print("UPLOADED")
