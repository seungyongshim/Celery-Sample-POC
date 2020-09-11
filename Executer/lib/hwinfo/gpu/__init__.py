import nvidia_smi 
import configure as config

nvidia_smi.nvmlInit()
handle = nvidia_smi.nvmlDeviceGetHandleByIndex(config.SELECT_GPU)
UUID = nvidia_smi.nvmlDeviceGetUUID(handle)

def gpuUsage():
    return nvidia_smi.nvmlDeviceGetUtilizationRates(handle)