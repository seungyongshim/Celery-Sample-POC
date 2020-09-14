import pika
import configure as cfg

__connection = pika.BlockingConnection(pika.ConnectionParameters(cfg.RABBITMQ_HOST, cfg.RABBITMQ_PORT,blocked_connection_timeout=1000))
__channel = __connection.channel()
__channel.basic_qos(prefetch_count=1) 
__channel.exchange_declare('log', 'topic')
__channel.exchange_declare('bluecats', 'fanout')
__channel.exchange_declare('events', 'fanout')

__channel.exchange_bind('bluecats','log', '#')
__channel.exchange_bind('events','log', '#.INFO')
__channel.exchange_bind('events','log', '#.WARN')
__channel.exchange_bind('events','log', '#.ERROR')
__channel.exchange_bind('events','log', '#.FATAL')

__channel.queue_declare('bluecats.recently', arguments={'x-max-length': 100})
__channel.queue_declare('events.recently', arguments={'x-max-length': 100})
__channel.queue_bind('bluecats.recently','bluecats')
__channel.queue_bind('events.recently','events')


def consume(modelName):
    return __channel.consume(modelName, inactivity_timeout=10)

def ack(method):
    __channel.basic_ack(method.delivery_tag)

def close():
    __channel.close()