import torch
print(torch.cuda.is_available())
print(torch.__version__)
print(torch.version.cuda)

if torch.cuda.is_available():
    print(f"可用的 GPU 數量: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
else:
    print("CUDA 不可用")
