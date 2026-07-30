<div align="center">

# 🛡️ CertifyAI

### AI-Powered Certificate Verification System

**Detect fake certificates in seconds, not hours.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

---

**Upload certificates → AI extracts text & QR data → Cross-verifies → Flags fraud → Exports results**

*Built for colleges, HR teams, and admissions departments who need to verify certificates at scale.*

</div>

---

## ⚡ Get Started in 30 Seconds

> **Prerequisites:** [Python 3.11+](https://www.python.org/downloads/) installed and added to PATH.

```
1.  Double-click  setup.bat           ← One-time setup (creates environment, installs everything)
2.  Double-click  Start_CertifyAI.bat ← Launches the app & opens your browser
```

That's it. No manual installs, no terminal commands, no configuration files.

> **📦 Setup handles everything automatically** — Python virtual environment, pip dependencies, Tesseract OCR engine, and Poppler PDF tools are all downloaded and configured for you.

---

## 🔍 How It Works

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   📄 Upload  │────▶│  🔤 OCR      │────▶│  📊 Cross-   │────▶│  ✅ Result   │
│  Certificate │     │  Extraction  │     │  Verification│     │  & Export    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                      Tesseract AI         OCR vs QR Data       Excel Report
                      reads all text       fuzzy matching       with verdicts
                      from the image       detects mismatches   color-coded
                            │                     │
                            ▼                     ▼
                     ┌──────────────┐     ┌──────────────┐
                     │  📱 QR Code  │     │  🧠 Fuzzy    │
                     │  Decoding    │     │  Matching    │
                     └──────────────┘     └──────────────┘
                      OpenCV + ZBar        Levenshtein
                      extracts JSON        distance scoring
                      credential data      for name/date
```

### The Verification Pipeline

| Step | Engine | What It Does |
|------|--------|-------------|
| **OCR Extraction** | Tesseract 5 (LSTM) | Reads name, course, date, issuer from the certificate image |
| **QR Decoding** | OpenCV + ZBar | Decodes the embedded QR code to extract the original credential JSON |
| **Cross-Verification** | FuzzyWuzzy + Levenshtein | Compares OCR text against QR data using fuzzy matching (handles typos, formatting) |
| **Date Validation** | Custom parser | Normalizes and compares dates across 6+ formats with tolerance |
| **Verdict** | Rule engine | `✅ Verified` · `⚠️ Likely Valid` · `❌ Forgery Suspected` · `🔍 Manual Review` |

---

## 🎯 Key Features

<table>
<tr>
<td width="50%">

### 🚀 Bulk Processing
Upload **up to 100 certificates at once**. Parallel processing with thread pools handles them simultaneously — not one by one.

### 🧠 Multi-Layer AI
Not just OCR. The system cross-references **extracted text against embedded QR code data** using fuzzy matching algorithms to catch even subtle forgeries.

### 📊 Excel Export
One-click download of a **professional, color-coded Excel report** — green for verified, red for forgery, yellow for manual review.

</td>
<td width="50%">

### 📱 QR Code Intelligence
Decodes embedded credential QR codes (JSON format) and extracts the **original issuer data** for comparison against the printed text.

### 🔤 Smart OCR
Tesseract 5 LSTM with **image preprocessing** — auto-resize, grayscale conversion, contrast enhancement, and sharpening for maximum accuracy.

### 🖥️ Zero-Config Desktop App
Double-click to launch. **No Python knowledge needed.** Auto-downloads all dependencies including Tesseract OCR and Poppler.

</td>
</tr>
</table>

---

## 🏗️ Project Structure

```
CertifyAI/
├── 🟢 setup.bat              ← Run first: creates environment & installs everything
├── 🟢 Start_CertifyAI.bat    ← Run to launch the app
├── 📄 README.md
├── 📄 LICENSE
│
└── src/
    ├── backend/
    │   ├── app.py             ← FastAPI server, bulk processing, Excel export
    │   ├── ocr.py             ← Tesseract OCR with image preprocessing
    │   ├── qr_decoder.py      ← OpenCV + ZBar QR code extraction
    │   ├── comparator.py      ← Fuzzy matching & verification logic
    │   ├── desktop_simple.py  ← Desktop launcher (auto-opens browser)
    │   └── requirements.txt   ← Python dependencies
    │
    └── frontend/
        ├── index.html         ← Single-page app UI
        ├── script.js          ← Upload, progress, results logic
        └── style.css          ← Modern responsive design
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Server** | FastAPI + Uvicorn | High-performance async API server |
| **OCR** | Tesseract 5 (LSTM engine) | Text extraction from certificate images |
| **Computer Vision** | OpenCV 5 + ZBar | QR code detection and decoding |
| **Matching** | FuzzyWuzzy + python-Levenshtein | Fuzzy string comparison for name/course matching |
| **PDF Support** | pdf2image + Poppler | Convert PDF certificates to images for processing |
| **Image Processing** | Pillow | Preprocessing (resize, contrast, sharpen) before OCR |
| **Export** | openpyxl | Professional Excel report generation |
| **Frontend** | Vanilla HTML/CSS/JS | Lightweight, fast, no build step needed |
| **Desktop** | PyWebView | Native desktop window wrapper |
| **Deployment** | Docker | One-command containerized deployment |

---

## 🚀 Setup Options

### ⚡ Windows Desktop (Recommended)

```
setup.bat              ← Installs Python venv, dependencies, Tesseract, Poppler
Start_CertifyAI.bat    ← Starts server + opens browser at http://127.0.0.1:5199
```

> **Portable:** Copy the project folder to any Windows PC, run `setup.bat`, and it works. The setup automatically detects and recreates broken virtual environments from other machines.

---

### 🐧 Manual Setup (macOS / Linux)

```bash
cd src/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Tesseract OCR
# Ubuntu/Debian: sudo apt install tesseract-ocr
# macOS: brew install tesseract

python desktop_simple.py
```

---

### 🐳 Docker

```bash
cd src
docker build -t certifyai .
docker run -p 7860:7860 certifyai
```

---

## 📡 API Reference

The server runs at `http://127.0.0.1:5199` and exposes these endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the frontend UI |
| `POST` | `/verify` | Verify a single certificate (returns JSON) |
| `POST` | `/verify-bulk` | Verify multiple certificates, returns Excel file |
| `POST` | `/verify-bulk-json` | Verify multiple certificates, returns JSON |

### Single Verification

```bash
curl -X POST http://127.0.0.1:5199/verify \
  -F "certificate=@certificate.pdf"
```

**Response:**
```json
{
  "name":    { "ocr": "John Doe", "qr": "John Doe", "match": true },
  "course":  { "ocr": "Machine Learning", "qr": "Machine Learning", "match": true },
  "date":    { "ocr": "January 15, 2024", "qr": "2024-01-15", "match": true },
  "verdict": "✅ Verified"
}
```

---

## 🔧 Environment Variables

Create `src/backend/.env` for optional configuration:

```env
# Only needed for cloud deployments
MONGODB_URL=mongodb+srv://...
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
JWT_SECRET_KEY=your_secret_key
```

> **Note:** The desktop app works without any `.env` file. Environment variables are only needed for cloud deployment features.

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Single certificate | ~2-5 seconds |
| Bulk (100 certificates) | ~60-90 seconds (parallel) |
| Concurrent workers | 4 threads |
| Supported formats | JPG, PNG, PDF |
| Max image dimension | Auto-resized to 2000px |

---

## 🤝 Contributing

```bash
# 1. Fork & clone
git clone https://github.com/YOUR_USERNAME/Certify_ai.git

# 2. Create a feature branch
git checkout -b feature/your-feature

# 3. Make changes & test
setup.bat
Start_CertifyAI.bat

# 4. Submit a pull request
git push origin feature/your-feature
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/VishalRaut2106/Certify_ai/issues)
- **Email:** vishalraut.contact@gmail.com

---

<div align="center">

**Built with 🧠 AI and ❤️ for educational institutions worldwide**

*CertifyAI — Because trust should be verified, not assumed.*

</div>
