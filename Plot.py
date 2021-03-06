# coding: utf-8
import pymongo
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import datetime, os
url = 'mongodb://saturn.ee.ntu.edu.tw:11707'

def plotGraph(dataX,dataY,title):
    fig = plt.figure()
    dataX = matplotlib.dates.date2num(dataX)
    plt.plot_date(dataX, dataY, linestyle = 'solid', figure = fig, marker="")
    plt.ticklabel_format(style='plain', axis='y')    
    plt.ylabel('USD/'+ title)
    fig.autofmt_xdate()
    
    # Export graph as PNG to 'Data' directory
    path = os.path.dirname(os.path.realpath('__file__'))
    path = os.path.join(path,'Data/', title+'.png')
    fig.savefig(path)
    plt.close()

if __name__ == '__main__':
    client = pymongo.MongoClient(url)
    database = client['XChangeRate']
    currencyNameList = database.collection_names() # get collection list
    
    for currency in currencyNameList:
        collection = database[currency]
        Time = []
        Price = []
        for entry in collection.find().sort('time', pymongo.ASCENDING):
            p = entry['price']        
            t = datetime.datetime.utcfromtimestamp(int(entry['time']))
            Time.append(t)
            Price.append(p)
        graph = plotGraph(Time, Price, currency)

