# -*- coding: utf-8 -*- 
import logging
import configure as cfg
import requests
import json
import time

logger = logging.getLogger(__name__)

def GetRabbitMQListQueues(containTopicName, response):
    return map(lambda x: { 'name':x['name'], 'consumers':x['consumers'], 'messages':x['messages'], 'cost': x['messages'] / (x['consumers'] + 1) }, 
           filter(lambda x: 0 != x['messages'], 
           filter(lambda x: containTopicName in x['name'], 
           response.json())))

def GetQueueOrWaiting():
    while True:
        response = requests.get(cfg.RABBITMQ_API_URL + 'queues', auth=(cfg.RABBITMQ_ID, cfg.RABBITMQ_PW))
        queues = sorted(GetRabbitMQListQueues(cfg.RABBITMQ_TOPIC, response),  key=lambda x: x['cost']) 

        if queues:
            # 조건) consumer+1로 messages 수를 나눈 값이 가장 큰 queue를 선택한다.
            logger.info('selected queue %r' % queues[-1])
            return queues[-1]

        logger.info('nothing job... wait 5 sec')
        time.sleep(5)