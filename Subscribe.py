# coding: utf-8

from pubnub import Pubnub
from pymongo import MongoClient
import re
sub_key="sub-c-5373256c-34a4-11e6-ad57-02ee2ddab7fe"
url = 'mongodb://saturn.ee.ntu.edu.tw:11707'

def _callback(message, channel):
    try:
        data = {'name':message['name'], 'price':message['price'], 'time':message['ts']}
        msg_buffer.append(data) # data structure: (name,price,time)
#         print(message) # debug use
        storeData(data)
    except TypeError:
        pass
def _error(message):
    print(message)

def storeData(data):
    client = MongoClient(url)
    database = client['XChangeRate']
    name = re.sub(r'USD/','',data['name'])
    collection = database[name]
    collection.find_one_and_update({'time':data['time']},{'$set':{'price':data['price'], 'time':data['time']}}, upsert = True)

if __name__ == '__main__':
    msg_buffer = []
    pubnub = Pubnub(publish_key="demo", subscribe_key=sub_key)
    pubnub.subscribe(channels="xChangeRate", callback=_callback, error=_error)
    while True:
        if len(msg_buffer) > 0:
            for msg in msg_buffer:
                storeData(msg)
                msg_buffer.pop(0)
