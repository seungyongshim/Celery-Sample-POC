import pika
import time


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare('mls.inference_jobs_direct', arguments={'alternate-exchange': 'mls.inference_jobs' })
channel.queue_declare(queue='mls.inference_jobs.tf2')
channel.basic_qos(prefetch_count=1) 
last_loading_model=''

for method, properties, body in channel.consume('mls.inference_jobs.tf2'):
    
    channel.queue_declare(queue=method.routing_key, 
                          auto_delete=True,
                          arguments={'x-message-ttl': 60000,
                                     'x-dead-letter-exchange': 'mls.inference_jobs',
                                     'x-max-length': 5 })
    channel.queue_bind(method.routing_key, 'mls.inference_jobs_direct')

    if method.routing_key == last_loading_model: 
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " [x] Received Cached %r" % body)
        time.sleep(3)
    else: 
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " [x] Received %r" % body)
        time.sleep(30)
        last_loading_model = method.routing_key

    channel.basic_ack(method.delivery_tag)
    
    c = connection.channel()
    c.basic_qos(prefetch_count=1) 
    
    for m, p, b in c.consume(method.routing_key,  inactivity_timeout=10):
        if b == None: break
    
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " [x] Received Cached %r" % b)
        time.sleep(3)

        c.basic_ack(m.delivery_tag)
        
    c.close()


channel.close()
connection.close()