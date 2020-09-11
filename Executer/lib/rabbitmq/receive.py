import pika
import configure as cfg

__connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.RABBITMQ_HOST, cfg.RABBITMQ_PORT,blocked_connection_timeout=1000))
__channel = __connection.channel()
__channel.basic_qos(prefetch_count=1) 

def consume(selectedQueue):
    return __channel.consume(selectedQueue['name'], inactivity_timeout=10)

def ack(method):
    __channel.basic_ack(method.delivery_tag)

def close():
    __channel.close()