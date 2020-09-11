import json
import logging
import logging.config

import configure as cfg
import lib.hwinfo.gpu as hwinfo
import inference
import lib.rabbitmq as rmq


logging.config.dictConfig(json.load(open('./logger.json')))

logger = logging.getLogger(__name__)
logger.info("start inference.executer...")

modelName = rmq.GetQueueOrWaiting()['name']

for m, p, job in rmq.consume(modelName):
    if job :
        inference.loadModel(modelName)
        if inference.run(job):
            rmq.ack(m)
    else:
        break
    
rmq.close()    
