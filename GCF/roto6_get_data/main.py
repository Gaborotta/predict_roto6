from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from time import sleep

from screp import get_numbers_roto, get_index


def roto6_get_data(event, context):

    latest_target = get_index()[0]
    sleep(2)
    numbers = get_numbers_roto(latest_target)

    # Use a service account
    cred = credentials.Certificate('./serviceAccount.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    for num in numbers:
        doc_ref = db.collection(u'number_results').document(num['title'])
        doc_ref.set(num)

    return 'Finish {}'.format(len(numbers))
