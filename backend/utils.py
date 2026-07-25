import numpy as np
from PIL import Image
from skimage.color import rgb2lab, lab2rgb
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F

def preprocess_image(image: Image.Image) -> tuple[torch.Tensor, tuple[int, int]]:
    """
    Converts RGB PIL Image to a padded LAB L-channel tensor.
    The image is padded to be divisible by 16.
    """
    # 1. Get original size and convert to RGB numpy array
    original_size = (image.height, image.width)
    img_np = np.array(image.convert("RGB"))
    
    # 2. Convert to LAB and then to a tensor
    img_lab = rgb2lab(img_np).astype("float32")
    img_lab = transforms.ToTensor()(img_lab)
    
    # 3. Extract L channel and normalize [0, 100] -> [0, 1]
    L = img_lab[[0], ...] / 100.0 
    
    # 4. Calculate padding to make dimensions divisible by 16
    _, h, w = L.shape
    pad_h = (16 - h % 16) % 16
    pad_w = (16 - w % 16) % 16
    
    # Pad the tensor (left, right, top, bottom)
    L_padded = F.pad(L, (0, pad_w, 0, pad_h), mode='replicate')
    
    # 5. Add batch dimension and return with original size
    return L_padded.unsqueeze(0), original_size

def postprocess_image(L_padded_tensor: torch.Tensor, ab_tensor: torch.Tensor, original_size: tuple[int, int]) -> Image.Image:
    """Converts L and ab tensors back to an RGB PIL Image, cropping to original size."""
    # 1. Denormalize L and ab channels
    L_padded = L_padded_tensor.cpu().numpy().squeeze() * 100.0
    ab = ab_tensor.cpu().numpy().squeeze() * 128.0
    
    # 2. Ensure correct dimensions for concatenation
    if L_padded.ndim == 2:
        L_padded = np.expand_dims(L_padded, axis=-1)
    if ab.ndim == 3 and ab.shape[0] == 2:
        ab = ab.transpose(1, 2, 0)
        
    # 3. Combine channels and convert back to RGB
    Lab_padded = np.concatenate([L_padded, ab], axis=-1)
    rgb_padded_float = lab2rgb(Lab_padded)
    
    # 4. Crop the image back to its original size
    h_orig, w_orig = original_size
    rgb_float = rgb_padded_float[:h_orig, :w_orig, :]
    
    # 5. Convert to uint8 [0, 255] and return as PIL Image
    rgb_uint8 = (rgb_float * 255.0).astype(np.uint8)
    return Image.fromarray(rgb_uint8)
