import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os


def initialiseSDK():
    sdk_path = os.path.join(os.getcwd(), "Source", "SDKFile")
    SDK_FOUND = False
    for file in os.listdir(sdk_path):
        if file.endswith(".json"):
            SDK_FOUND = True
            sdk_path = os.path.join(sdk_path, file)
    
    return SDK_FOUND, sdk_path


SDK_FOUND, sdk_path = initialiseSDK()
if SDK_FOUND:
    cred = credentials.Certificate(sdk_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://automatic-videography-default-rtdb.firebaseio.com/'
    })


def sendToDatabase(dataDict):
    ref = db.reference('main/')
    review_ref = ref.child('reviews')
    review_ref.push().set(dataDict)
