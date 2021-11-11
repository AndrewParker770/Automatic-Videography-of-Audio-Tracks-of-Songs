import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("Source/automatic-videography-firebase-adminsdk-gxt1y-e27588c9f4.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://automatic-videography-default-rtdb.firebaseio.com/'
})

def sendToDatabase(dataDict):
    ref = db.reference('main/')
    review_ref = ref.child('reviews')
    review_ref.push().set(dataDict)
