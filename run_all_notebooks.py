import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import time
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

notebooks = [
    'notebooks/01_eda.ipynb',
    'notebooks/02_data_preparation.ipynb',
    'notebooks/03_model_experimentation.ipynb',
    'notebooks/end_to_end_dark_pattern_ml.ipynb'
]

ep = ExecutePreprocessor(timeout=1200, kernel_name='python3')

for nb_path in notebooks:
    print(f"\n========================================================", flush=True)
    print(f"▶ EXECUTING: {nb_path}", flush=True)
    print(f"========================================================", flush=True)
    start_time = time.time()
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    try:
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(os.path.abspath(nb_path))}})
        elapsed = time.time() - start_time
        print(f"✅ PASSED in {elapsed:.2f} seconds!", flush=True)
        
        # Save executed notebook with all outputs and figures intact
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"💾 Saved executed notebook with outputs to: {nb_path}", flush=True)
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"❌ FAILED after {elapsed:.2f} seconds:", flush=True)
        print(e, flush=True)
        sys.exit(1)

print("\n🎉 ALL 4 NOTEBOOKS SUCCESSFULLY EXECUTED AND SAVED WITH IN-LINE OUTPUTS!", flush=True)
