# Image Compression Engine (YUV & Quantization)

A lightweight Python implementation of a lossy image compression pipeline. This project demonstrates core Digital Signal Processing (DSP) and computer vision concepts by converting images from the standard BGR/RGB color space into **YUV**, applying **chroma subsampling**, and utilizing **bit-depth quantization** to reduce file size while maintaining structural visual quality.

---

## 🚀 Features

* **Color Space Conversion:** Custom matrices to transition between RGB and YUV spaces to separate brightness (Luminance) from color (Chrominance).
* **Chroma Subsampling:** Implements a custom 4:2:2 spatial reduction algorithm, discarding redundant color data where the human eye is less sensitive.
* **Bit-Depth Quantization:** Offers configurable bit-reduction per channel (e.g., 6-bit for Y, 5-bit for Chrominance) to limit the color palette and compress data.
* **Quality Metrics Summary:** Built-in calculation of **PSNR (Peak Signal-to-Noise Ratio)** and MSE to accurately measure quality degradation against the original image.
* **Size Analysis:** Real-time calculation of memory footprints (in KB) to evaluate compression ratios.

---

## 🛠️ The Compression Pipeline

The process follows a classical image processing workflow:

$$\text{Original (BGR)} \longrightarrow \text{YUV Space} \longrightarrow \text{Chroma Subsampling (4:2:2)} \longrightarrow \text{Quantization} \longrightarrow \text{Reconstructed BGR}$$

1.  **Luminance Splitting ($Y$):** Kept at a higher resolution/bitrate since human vision is highly sensitive to brightness details.
2.  **Chrominance Compression ($U, V$):** Subsampled horizontally by skipping alternate columns, then padded back dynamically to match core array dimensions.
3.  **Uniform Quantization:** Scales down continuous 8-bit channel values into discrete levels based on a custom bit-rate threshold.

---

## 📊 Evaluation Standards

The engine evaluates performance using Peak Signal-to-Noise Ratio (PSNR):
* **> 40 dB:** Excellent quality (near-lossless to the human eye).
* **30 - 40 dB:** Good quality with minimal compression artifacts.
* **20 - 30 dB:** Acceptable quality; ideal for aggressive storage optimization.

---

## 💻 Tech Stack & Requirements

* **Python 3.x**
* **OpenCV (cv2):** For image decoding and basic matrix conversions.
* **NumPy:** For high-performance vector operations and array clipping.
* **Pillow (PIL):** Used for buffer stream emulation to measure raw compressed sizes.

### Installation

```bash
pip install opencv-python numpy pillow
