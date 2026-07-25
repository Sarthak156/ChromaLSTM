import os
import torch
from model import xLSTMColorizer

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "checkpoints", "best_model.pth")

_model_instance = None

def get_model():
    global _model_instance
    if _model_instance is None:
        _model_instance = xLSTMColorizer().to(DEVICE)
        
        # Load weights if checkpoint exists, otherwise run random weights for demo
        if os.path.exists(MODEL_PATH):
            print(f"Loading weights from {MODEL_PATH}")
            checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)
            # Handle checkpoints saved as a dict or as the state_dict directly
            if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                _model_instance.load_state_dict(checkpoint['model_state_dict'])
            else:
                _model_instance.load_state_dict(checkpoint)

        else:
            print("WARNING: No checkpoint found. Using initialized weights for dry-run/testing.")
            
        _model_instance.eval()
    return _model_instance

def predict_color(L_tensor: torch.Tensor) -> torch.Tensor:
    model = get_model()
    L_tensor = L_tensor.to(DEVICE)
    with torch.no_grad():
        ab_tensor = model(L_tensor)
    return ab_tensor
