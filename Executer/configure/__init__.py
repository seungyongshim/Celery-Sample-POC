import os
import logging

SELECT_GPU = os.getenv('SELECT_GPU', 0) 
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost') 
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 5672) 
RABBITMQ_API_HOST = os.getenv('RABBITMQ_API_HOST', RABBITMQ_HOST) 
RABBITMQ_API_PORT = os.getenv('RABBITMQ_API_PORT', 15672) 
RABBITMQ_ID = os.getenv('RABBITMQ_ID','guest')
RABBITMQ_PW = os.getenv('RABBITMQ_PW','guest')
RABBITMQ_TOPIC = os.getenv('RABBITMQ_TOPIC', 'mls.inference_jobs.tf2')

RABBITMQ_API_URL = 'http://%s:%d/api/' % (RABBITMQ_API_HOST, RABBITMQ_API_PORT)