from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from time import sleep
import base64

from scrap import get_results


def loto_get_data_pubsub(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
        results = get_results(name)
        sleep(3)

        # Use a service account
        cred = credentials.Certificate('./serviceAccount.json')
        firebase_admin.initialize_app(cred)

        db = firestore.client()

        df_base = db.collection('loto_results').document(
            name).collection('results')

        for res in results:
            doc_ref = df_base.document(res['title'])
            doc_ref.set(res)
        print('Done')

    else:
        print('no data')
