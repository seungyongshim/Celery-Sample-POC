import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.confirm_delivery()
channel.queue_declare('mls.inference_jobs.tf2.model-a')
channel.queue_declare('mls.inference_jobs.tf2.model-b')
channel.queue_declare('mls.inference_jobs.tf2.model-c')

i = 1

try:
    while True:
        channel.basic_publish(exchange='',
                          routing_key='mls.inference_jobs.tf2.model-c',
                          body='C%d ' % i  + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                          mandatory=True)
        print('Message was published')
        time.sleep(1)
        channel.basic_publish(exchange='',
                          routing_key='mls.inference_jobs.tf2.model-b',
                          body='B%d ' % i + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                          mandatory=True)
        print('Message was published')
        time.sleep(1)
        i = i + 1
    
except pika.exceptions.UnroutableError:
    print('Message was returned')