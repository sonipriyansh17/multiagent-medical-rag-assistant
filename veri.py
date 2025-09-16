import torch

if torch.cuda.is_available():
    print("✅ GPU is available!")
    print(f"Device Name: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Version (used by PyTorch): {torch.version.cuda}")
else:
    print("❌ GPU is not available. Check your installation.")

