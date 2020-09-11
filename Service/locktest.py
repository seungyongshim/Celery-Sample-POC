import redis
import time
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

r = redis.StrictRedis(host='localhost', port=6379)

logging.info("start process...")

with r.lock('my_resource_name',1000):
    logging.info("acquire lock...")
    time.sleep(10)

logging.info("release lock")


