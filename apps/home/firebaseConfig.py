import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# Application Default credentials are automatically created.
from firebase_admin import storage

cred = credentials.Certificate("apps/home/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
#
db = firestore.client()

transaction = db.transaction()
# bucket = storage.bucket()




