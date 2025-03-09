import torch

if torch.cuda.is_available():
    print("CUDA is available. GPU is ready for use.")
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available. Using CPU instead.")
