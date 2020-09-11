import nvidia_smi 
import logging
logger = logging.getLogger(__name__)

nvidia_smi.nvmlInit()

def GetUUID(GPU):
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(GPU)
    ret = nvidia_smi.nvmlDeviceGetUUID(handle)
    logger.info(ret)
    return ret
