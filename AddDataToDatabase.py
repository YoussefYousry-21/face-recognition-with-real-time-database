import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facedata-52f50-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "2005001":
    {
        "name": "Ghoniem",
        "major": "CIE",
        "starting_year": 2020,
        "total_attendence": 6,
        "standing": "6",
        "year": 5,
        "last_attendence_time": "2024-01-01 00:54:34"
    },
    "2005007":
    {
        "name": "Youssef",
        "major": "CIE",
        "starting_year": 2019,
        "total_attendence": 7,
        "standing": "7",
        "year": 5,
        "last_attendence_time": "2023-01-01 00:54:34"
    },

}

for key, value in data.items():
    ref.child(key).set(value)