from flask import Flask, render_template, request
import os
import cv2
import numpy as np
# main file imageCompression
from imageCompression import compress_image, get_image_size_kb, calculate_psnr

app = Flask(__name__)


UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            # File inspection
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            # Original image
            path_orig = os.path.join(app.config['UPLOAD_FOLDER'], 'original.png')
            file.save(path_orig)
            
            # Read image
            img_np = cv2.imread(path_orig)
            orig_size = get_image_size_kb(img_np)

            # Compressed image
            compressed_np = compress_image(img_np)
            path_comp = os.path.join(app.config['UPLOAD_FOLDER'], 'compressed.png')
            cv2.imwrite(path_comp, compressed_np)
            
            # Detaile Size&Psnr
            comp_size = get_image_size_kb(compressed_np)
            saved_space = orig_size - comp_size
            ratio = (saved_space / orig_size) * 100 if orig_size > 0 else 0
            psnr_val = calculate_psnr(img_np, compressed_np)

            # Return To Html File
            return render_template('index.html', 
                                 orig_img='uploads/original.png',
                                 comp_img='uploads/compressed.png',
                                 orig_size=round(orig_size, 2),
                                 comp_size=round(comp_size, 2),
                                 saved=round(saved_space, 2),
                                 ratio=round(ratio, 1),
                                 psnr=round(psnr_val, 2))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)