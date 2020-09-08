import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='mls.inference_jobs.tf2', )
channel.confirm_delivery()

channel.exchange_declare('mls.inference_jobs_direct', arguments={'alternate-exchange': 'mls.inference_jobs' })
channel.exchange_declare('mls.inference_jobs',exchange_type='topic')
channel.queue_bind('mls.inference_jobs.tf2', 'mls.inference_jobs', 'mls.inference_jobs.tf2.*')

try:
    while True:
        channel.basic_publish(exchange='mls.inference_jobs_direct',
                          routing_key='mls.inference_jobs.tf2.model1',
                          body='Model1 ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                          mandatory=True)
        print('Message was published')
        time.sleep(1)
        channel.basic_publish(exchange='mls.inference_jobs_direct',
                          routing_key='mls.inference_jobs.tf2.model2',
                          body='Model2 ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                          mandatory=True)
        print('Message was published')
        time.sleep(1)
    
except pika.exceptions.UnroutableError:
    print('Message was returned')