import pyrebase
import os

# path_record = "record/"
# firebase = Firebase(config)
# storage = Firebase.storage()
# path_on_cloud = ""
# storage.child(path_on_cloud)

config = {
    "apiKey": "AIzaSyCuwZLvFYIXqrO9IhiD_wUYSS6xKz287G4",
    "authDomain": "proctor-96511.firebaseapp.com",
    "projectId": "proctor-96511",
    "storageBucket": "proctor-96511.appspot.com",
    "messagingSenderId": "782036150781",
    "appId": "1:782036150781:web:78d84200dcd02327995194",
    "measurementId": "G-BHS76LQV6Z"
}

now_firebase = pyrebase.initialize_app(config)
storage = now_firebase.storage()
my_rec = "sample.wav"
storage.child(my_rec).download(filename=my_rec, path=os.path.basename(my_rec))
auth = now_firebase.auth()
email = "wqe2@gmail.com"
password = "abbasasma99"
user = auth.sign_in_with_email_and_password(email, password)
url = storage.child(my_rec).get_url(user['idToken'])
print(url)
