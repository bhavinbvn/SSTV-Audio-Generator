from flask import Flask, render_template, request, send_file
from pysstv.color import MartinM1
from PIL import Image
from scipy.io.wavfile import write
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], "uploaded.jpg")
            file.save(filepath)

            # Convert to SSTV
            image = Image.open(filepath).convert('RGB').resize((320, 256))
            sstv = MartinM1(image, 44100, bits=8)
            samples = np.fromiter(sstv.gen_samples(), dtype=np.float32)
            samples = np.clip(samples, -1.0, 1.0)
            samples = (samples * 32767).astype(np.int16)
            out_wav_path = os.path.join(app.config['UPLOAD_FOLDER'], "output_sstv.wav")
            write(out_wav_path, 44100, samples)

            return render_template('index.html', generated=True)

    return render_template('index.html', generated=False)

@app.route('/download')
def download():
    return send_file("static/output_sstv.wav", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
