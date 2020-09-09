import requests
import json
import time
import pika

HOST = 'localhost'
PORT = 5672
ID = 'guest'
PW = 'guest'
URL_API = 'http://%s:15672/api/' % HOST 
TOPIC = 'mls.inference_jobs.tf2.m'

def GetRabbitMQListQueues(containTopicName, response):
    return map(lambda x: { 'name':x['name'], 'consumers':x['consumers'], 'messages':x['messages'], 'cost': x['messages'] / (x['consumers'] + 1) }, 
           filter(lambda x: 0 != x['messages'], 
           filter(lambda x: containTopicName in x['name'], 
           response.json())))

def GetQueueOrWaiting():
    while True:
        response = requests.get(URL_API + 'queues', auth=(ID, PW))
        queues = sorted(GetRabbitMQListQueues(TOPIC, response),  key=lambda x: x['cost']) 

        if queues:
            # 조건) consumer+1로 messages 수를 나눈 값이 가장 큰 queue를 선택한다.
            return queues[-1]

        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' nothing job...')
        time.sleep(5)
        
selectedQueue = GetQueueOrWaiting()

connection = pika.BlockingConnection(pika.ConnectionParameters(HOST, PORT,blocked_connection_timeout=1000))
channel = connection.channel()
channel.basic_qos(prefetch_count=1) 
lastLoadedModel=''

def InferenceMocked(job):
    global lastLoadedModel 
    if lastLoadedModel == selectedQueue['name']:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " [x] Received Cached %r" % job)
        time.sleep(1)
    else:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " [x] Received %r" % job)
        lastLoadedModel = selectedQueue['name']
        time.sleep(5)
    return True

for m, p, b in channel.consume(selectedQueue['name'], inactivity_timeout=10):
    if b == None: break
    if InferenceMocked(b):
        channel.basic_ack(m.delivery_tag)

channel.close()    