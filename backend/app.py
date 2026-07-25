from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import io
import time
from PIL import Image

from utils import preprocess_image, postprocess_image
from inference import predict_color

app = FastAPI(title="xLSTM Colorizer API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev. In prod, lock this down.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ONLINE", "model": "xLSTM", "device": "ACTIVE"}

@app.get("/model-info")
def model_info():
    return {
        "architecture": "PurePyTorch_mLSTM",
        "embed_dim": 256,
        "parameters": "Approx 4.5M",
        "status": "READY"
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Only PNG and JPG files are supported.")
    
    try:
        # 1. Read Image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        start_time = time.time()
        
        # 2. Preprocess
        L_tensor, original_size = preprocess_image(image)
        
        # 3. Inference
        ab_tensor = predict_color(L_tensor)
        
        # 4. Postprocess
        out_image = postprocess_image(L_tensor, ab_tensor, original_size)
        
        # 5. Save to bytes
        img_byte_arr = io.BytesIO()
        out_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        print(f"Inference complete in {time.time() - start_time:.3f}s")
        
        return Response(content=img_byte_arr, media_type="image/png")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
