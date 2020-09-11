import redis
import time
import logging

logger = logging.getLogger(__name__)
r = redis.StrictRedis(host='localhost', port=6379)

def RedisLock(uuid):
    return r.lock(uuid,1000)


