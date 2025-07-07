# 🔤 OCR Labeling Tool

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A full-stack application for semi-automated OCR labeling that extracts text from images using PaddleOCR and provides a clean interface for users to verify and correct the extracted text.

## ✨ Features

- **🤖 Automated OCR**: Uses PaddleOCR to automatically extract text from images
- **💻 Interactive UI**: Clean, modern interface built with React and TailwindCSS
- **📊 Progress Tracking**: Real-time progress bar showing labeling completion
- **✏️ Text Correction**: Easy-to-use interface for correcting OCR results
- **⏭️ Auto-advance**: Automatically moves to the next image after saving
- **🔔 Toast Notifications**: User-friendly notifications for all actions
- **⏭️ Skip Functionality**: Ability to skip images without labeling
- **🔄 Retry OCR**: Re-run OCR if the initial result is poor

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Output Format](#-output-format)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

## 🎬 Demo

> **Note**: Place your demo images/GIFs here when available

```bash
# Quick start in 3 commands
pip install -r requirements.txt
python main.py &
cd frontend && npm install && npm start
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ocr-labeling-tool.git
   cd ocr-labeling-tool
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify PaddleOCR installation:**
   ```bash
   python -c "from paddleocr import PaddleOCR; print('PaddleOCR installed successfully')"
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

## 🎯 Usage

### 1. Prepare Your Images

Create an `images/` directory and place all the images you want to label. The application supports:
- JPG/JPEG
- PNG
- BMP
- TIFF

```bash
mkdir images
# Copy your images to the images/ directory
```

### 2. Start the Backend Server

From the project root directory:
```bash
python main.py
```

The backend server will start on `http://localhost:8000`

**First Run**: PaddleOCR will download model files (~16MB total) on the first startup. This is normal and only happens once.

### 3. Start the Frontend Development Server

In a new terminal, navigate to the frontend directory and start the React development server:
```bash
cd frontend
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

### 4. Start Labeling

1. The application will automatically load the first unlabeled image
2. OCR will run automatically and display the extracted text
3. Review and correct the text in the editable text area
4. Click "Save & Next" to save the label and move to the next image
5. Use "Skip" to move to the next image without saving
6. Use "Retry OCR" if the initial OCR result is poor

### 5. Monitor Progress

- Progress bar shows completion percentage
- Counter displays "processed / total images"
- Toast notifications confirm successful saves

## 📚 API Documentation

The backend provides the following REST API endpoints:

### GET /api/images/next
Returns the next unprocessed image and progress information.

**Response:**
```json
{
  "image_name": "train_001.jpg",
  "image_url": "/images/train_001.jpg",
  "total_images": 1000,
  "processed_images": 42
}
```

### POST /api/ocr/file
Performs OCR on a specific image file.

**Parameters:**
- `image_name` (string) - Name of the image file

**Response:**
```json
{
  "extracted_text": "Hello world",
  "detailed_results": [...],
  "success": true,
  "image_name": "train_001.jpg"
}
```

### POST /api/save
Saves the corrected text label for an image.

**Form Data:**
- `image_name` (string) - Name of the image file
- `corrected_text` (string) - Corrected text content

**Response:**
```json
{
  "success": true,
  "message": "Label saved for train_001.jpg",
  "image_name": "train_001.jpg",
  "saved_text": "Hello world"
}
```

### GET /api/images
Returns overall progress information and image lists.

### GET /api/labels
Returns all saved labels.

## 📄 Output Format

Labels are saved in `labels.txt` with the following format:
```
train_001.jpg Hello world this is sample text
train_002.jpg Another example of extracted text
train_003.jpg More text content from the image
```

**Format Details**:
- **File**: `labels.txt` (plain text file)
- **Structure**: Each line contains one image-text pair
- **Separator**: Single space between image name and text
- **Encoding**: UTF-8
- **Text Processing**: Multiple spaces and newlines are normalized to single spaces

## 📁 Project Structure

```
├── main.py              # FastAPI backend server
├── requirements.txt     # Python dependencies
├── test_backend.py      # Backend testing script
├── labels.txt           # Output file with image-text pairs
├── images/              # Directory containing images to label
├── frontend/
│   ├── public/
│   │   └── index.html       # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/          # Reusable UI components
│   │   │   └── OCRLabeler.jsx  # Main labeling component
│   │   ├── hooks/
│   │   │   └── use-toast.js # Toast notification hook
│   │   ├── lib/
│   │   │   └── utils.js     # Utility functions
│   │   ├── App.js           # Main React component
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Node.js dependencies
│   ├── tailwind.config.js   # TailwindCSS configuration
│   └── postcss.config.js    # PostCSS configuration
├── .gitignore              # Git ignore file
├── LICENSE                 # MIT License
└── README.md               # This file
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `python test_backend.py`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Coding Standards

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write tests for new features

## 🔧 Troubleshooting

### Backend Issues

**PaddleOCR Model Download on First Run**:
On first startup, you'll see download progress for OCR models:
```
download https://paddleocr.bj.bcebos.com/PP-OCRv3/english/...
100%|██████████████████████████████████████| 4.00M/4.00M [00:03<00:00, 1.05MiB/s]
```
This is normal and only happens once.

**Server Not Starting**:
- Check if port 8000 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Frontend Issues

**Dependencies Installation**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Port Conflicts**:
If port 3000 is in use, React will automatically suggest an alternative port.

### OCR Issues

**Poor OCR Results**:
- Ensure images are clear and high-resolution
- Try the "Retry OCR" button
- Check that the image contains readable text

**OCR Taking Too Long**:
- First image may take longer as models initialize
- Subsequent images should process in ~0.3-0.4 seconds

## 🧪 Testing

To verify the backend is working correctly:
```bash
python test_backend.py
```

Expected output:
```
🔍 Testing OCR Labeling Backend...
==================================================
✅ Server Status: 200
✅ Images endpoint working
   Total images: 10001
   Processed: 0
   Remaining: 10001
✅ Next image endpoint working
   Next image: train_100_0.jpg
```

## 🏗️ Technical Stack

### Backend
- **FastAPI**: Modern, fast Python web framework
- **PaddleOCR**: Powerful OCR library supporting multiple languages
- **Uvicorn**: ASGI server for running FastAPI
- **Pillow**: Image processing library

### Frontend
- **React**: Modern JavaScript UI library
- **TailwindCSS**: Utility-first CSS framework
- **Radix UI**: Accessible component primitives
- **Lucide React**: Icon library
- **Axios**: HTTP client for API calls

## 📈 Performance

- **OCR Speed**: ~0.3-0.4 seconds per image
- **Text Detection**: 1-4 text boxes per image typically detected
- **Memory Usage**: ~2GB RAM for backend with PaddleOCR models loaded
- **Supported Languages**: English (can be configured for other languages)

## 🎯 Quick Start Summary

1. **Install backend**: `pip install -r requirements.txt`
2. **Install frontend**: `cd frontend && npm install`
3. **Start backend**: `python main.py` (wait for PaddleOCR to initialize)
4. **Start frontend**: `cd frontend && npm start`
5. **Open browser**: Visit `http://localhost:3000`
6. **Start labeling**: Review OCR results and save corrections!

## 📧 Support

For issues or questions:
1. Check the [troubleshooting section](#-troubleshooting)
2. Search existing [issues](https://github.com/yourusername/ocr-labeling-tool/issues)
3. Create a new [issue](https://github.com/yourusername/ocr-labeling-tool/issues/new) if needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Status**: ✅ **Ready to use** - Both servers are operational and OCR labeling can begin immediately!

Made with ❤️ by the OCR Labeling Tool community 