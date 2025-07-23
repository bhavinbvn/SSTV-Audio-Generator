
from pysstv.color import MartinM1
from PIL import Image
from scipy.io.wavfile import write
import numpy as np

image = Image.open("test2.jpg").convert('RGB').resize((320, 256))
sstv = MartinM1(image, 44100, bits=8)
samples = np.fromiter(sstv.gen_samples(), dtype=np.float32)
samples = np.clip(samples, -1.0, 1.0)
samples = (samples * 32767).astype(np.int16)
write("output_sstv4.wav", 44100, samples)
print("✅ SSTV audio generated.")
