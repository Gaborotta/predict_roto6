from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from time import sleep
import IPython

from functools import reduce

from screp import get_numbers_roto, get_index

targets = get_index()
sleep(2)

targets[17:]

res_list = []
for tg in targets[17:]:
    res_list.append(get_numbers_roto(tg))
    sleep(2)

numbers = reduce(lambda a, b: a+b, res_list)

# Use a service account
cred = credentials.Certificate('./serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

for num in numbers:
    doc_ref = db.collection(u'number_results').document(num['title'])
    doc_ref.set(num)
