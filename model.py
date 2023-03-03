
# from diffusers import StableDiffusionImg2ImgPipeline
from diffusers import StableDiffusionPipeline
import torch
import requests
from PIL import Image
import os
from GPUtil import showUtilization as gpu_usage
from numba import cuda
import random as rand

import os
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"
device = "cuda"

import inspect
import warnings
from typing import List, Optional, Union


def clearGPU():
    print("Initial GPU Usage")
    gpu_usage()                             

    torch.cuda.empty_cache()

    cuda.select_device(0)
    cuda.close()
    cuda.select_device(0)

    print("GPU Usage after emptying the cache")
    gpu_usage()
    
    torch.cuda.empty_cache()
    print(torch.cuda.memory_summary(device=None, abbreviated=False))

# This can be anything that the node operator desirs
model_path = "runwayml/stable-diffusion-v1-5"
def dummy(images, **kwargs): return images, False

pipe = None

def infer(prompt, request_id, strength=.75, num_inference_steps=70, guidance_scale=11, num_images_per_prompt=1):
    global pipe
    if (pipe is None):
        # clearGPU()
        pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16, safety_checker=dummy).to(device)
        
        
    
    generator = torch.Generator(device=device).manual_seed(1024)
    image = pipe(prompt=prompt, strength=0.5, guidance_scale=10, num_inference_steps=70, generator=generator).images[0]

    image.save("test.png")
    
    # Save it in decentralised storage here
    fname = "amazing_inference.jpg"
    
    if os.path.isfile("test.png"):
            os.remove("test.png")
    else:
        pass
    
    return fname

