import nvidia_smi 

nvidia_smi.nvmlInit()
handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)

tests = [
    nvidia_smi.nvmlDeviceGetName,
    nvidia_smi.nvmlDeviceGetPciInfo,
    nvidia_smi.nvmlDeviceGetMemoryInfo,
    nvidia_smi.nvmlDeviceGetUUID,
    nvidia_smi.nvmlDeviceGetUtilizationRates
]

for fx in tests:
    print(fx(handle)) 

ret = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
print(ret.gpu)
print(ret.memory)
