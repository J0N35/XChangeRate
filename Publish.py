
# coding: utf-8

# Method 2
# Different data source, limited query but realtime
from pubnub import Pubnub as PN
from time import sleep
import requests

def _callback(message):
    pass
def error(message):
    print("ERROR : " + str(message))
def publish_data(msg):
    stream.publish('xChangeRate', msg, callback=_callback, error=_callback)
def get_data():
    url = 'http://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?'
    param = {'format':'json'}
    req = requests.get(url, params = param).json()
    return req

if __name__ == '__main__':
    # Create Publish/Subscribe Channel
    stream = PN(publish_key="pub-c-5bc50adc-6bdd-4e4e-a7a8-1d7a78d4e528", subscribe_key="sub-c-5373256c-34a4-11e6-ad57-02ee2ddab7fe")
    while True:
        data = get_data() # about 175 entries
        if data:
            for entry in data['list']['resources']:
                publish_data(entry['resource']['fields']) # Publish data to PubNub Channel
                sleep(0.5) # Sleep to prevent over clawing, avoid banned by Yahoo!

