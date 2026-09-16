import easyocr
import numpy as np
from PIL import Image
import io

reader = None

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    return reader

def extract_text_from_image(image_bytes: bytes) -> str:
    # Convert bytes to numpy array for EasyOCR
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image_np = np.array(image)
    
    # Read text
    r = get_reader()
    results = r.readtext(image_np, detail=0) # detail=0 returns just a list of strings
    
    # Combine extracted text
    full_text = " ".join(results)
    return full_text
