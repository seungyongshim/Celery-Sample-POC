import logging
import time
import sys
import lib.hwinfo.gpu as gpu
from lib.utils import *

logger = logging.getLogger(__name__)
__lastLoadedModel = ''

def loadModel(modelName, limit_memory_percentage = 85):
    def checkUsageGpuMemory():
        gpuUsage = gpu.gpuUsage()
        if limit_memory_percentage < gpuUsage.memory: 
            logger.fatal("not enough memory %f" % gpuUsage.memory)
            sys.exit()

    global __lastLoadedModel 
    
    if __lastLoadedModel == modelName:
        logger.info('[x] Model Cached')
    else:
        with RedisLock('test'):
            logger.info('Model Loading %r' % modelName)
            __lastLoadedModel = modelName
            checkUsageGpuMemory()
            time.sleep(5)

def run(job):
    logger.info('Received %r' % job)
    time.sleep(1)
    return True
    

    
    