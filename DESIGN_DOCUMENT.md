# Semi-Auto OCR Tool - Design Document

## 1. Project Overview

### 1.1 Project Description
The Semi-Auto OCR Tool is a full-stack web application designed to streamline the process of labeling OCR (Optical Character Recognition) text data. The system automatically extracts text from images using PaddleOCR and provides an intuitive interface for users to review, edit, and confirm the extracted text labels.

### 1.2 Key Objectives
- **Automated Text Extraction**: Leverage PaddleOCR for high-accuracy text recognition
- **User-Friendly Interface**: Provide an intuitive web-based labeling interface
- **Efficient Workflow**: Enable rapid processing of large image datasets
- **Progress Tracking**: Real-time monitoring of labeling progress
- **Data Persistence**: Reliable storage and retrieval of labeled data

### 1.3 Target Users
- Data scientists and ML engineers
- Content moderators
- Document digitization teams
- Research organizations

## 2. System Architecture

### 2.1 High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   File System   │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Images &     │
│                 │    │                 │    │    Labels)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   PaddleOCR     │
                    │   Engine        │
                    └─────────────────┘
```

### 2.2 Component Architecture
- **Frontend Layer**: React-based SPA with TailwindCSS and shadcn/ui
- **Backend Layer**: FastAPI with async support
- **OCR Engine**: PaddleOCR for text extraction
- **File Management**: Local file system for image and label storage
- **Natural Sorting**: Custom algorithm for proper file ordering

## 3. Technology Stack

### 3.1 Backend Technologies
- **Framework**: FastAPI 0.104.1
- **Language**: Python 3.10+
- **OCR Engine**: PaddleOCR 2.7.3
- **Computer Vision**: OpenCV 4.8.1.78
- **Numerical Computing**: NumPy 1.24.3
- **HTTP Client**: httpx (for async operations)
- **CORS**: FastAPI CORS middleware

### 3.2 Frontend Technologies
- **Framework**: React 18
- **Language**: TypeScript/JavaScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui (Radix UI based)
- **Build Tool**: Create React App
- **HTTP Client**: Fetch API

### 3.3 Development Tools
- **Version Control**: Git
- **Package Managers**: pip (Python), npm (Node.js)
- **Environment**: Virtual environments (venv)

## 4. System Components

### 4.1 Backend Components

#### 4.1.1 FastAPI Application (`main.py`)
```python
# Core responsibilities:
- Image serving endpoints
- OCR processing endpoints
- Label management (CRUD operations)
- File system operations
- Natural sorting implementation
```

#### 4.1.2 OCR Service
- **PaddleOCR Integration**: Text detection and recognition
- **Image Processing**: Format handling (JPG, PNG, etc.)
- **Confidence Scoring**: OCR accuracy metrics
- **Error Handling**: Graceful degradation for failed OCR

#### 4.1.3 File Management Service
- **Image Directory Management**: Scanning and indexing
- **Label File Operations**: Read/write operations for labels.txt
- **Natural Sorting**: Custom algorithm for numerical ordering
- **Path Resolution**: Secure file access with validation

### 4.2 Frontend Components

#### 4.2.1 Main Application (`App.tsx`)
- Application routing and layout
- Global state management
- Error boundary implementation

#### 4.2.2 Image Labeling Interface
- **Image Display**: Responsive image rendering
- **Label Input**: Text field with real-time editing
- **Navigation Controls**: Previous/Next/Jump functionality
- **Progress Display**: Current position and total count

#### 4.2.3 UI Components
- **Button**: Consistent action buttons
- **Input**: Form input with validation
- **Card**: Content containers
- **Progress**: Visual progress indicators

## 5. API Design

### 5.1 Endpoints Overview

#### 5.1.1 Image Management
```
GET /images/{filename}
- Purpose: Serve image files
- Parameters: filename (path parameter)
- Response: Image file (JPEG/PNG)
- Headers: Appropriate MIME types
```

#### 5.1.2 OCR Operations
```
POST /ocr/{filename}
- Purpose: Extract text from image
- Parameters: filename (path parameter)
- Response: JSON with extracted text and confidence
- Processing: PaddleOCR text detection and recognition
```

#### 5.1.3 File Listing
```
GET /files
- Purpose: Get list of all image files
- Response: JSON array of filenames (naturally sorted)
- Processing: Directory scanning with custom sort algorithm
```

#### 5.1.4 Label Management
```
GET /labels/{filename}
- Purpose: Get existing label for image
- Response: JSON with label text or null

POST /labels/{filename}
- Purpose: Save/update label for image
- Body: JSON with label text
- Response: Success confirmation

GET /labels
- Purpose: Get all labels
- Response: JSON object with filename-label pairs
```

### 5.2 Natural Sorting Algorithm
```python
def natural_sort_key(filename):
    # Extract numeric parts for proper ordering
    # Example: train_1_0.jpg comes before train_100_0.jpg
    parts = re.split(r'(\d+)', filename)
    return [int(part) if part.isdigit() else part for part in parts]
```

## 6. Data Models

### 6.1 Label Storage Format
```
# labels.txt format (space-separated)
filename1.jpg extracted_text_content_here
filename2.jpg another_text_content_example
filename3.jpg multi word text content
```

### 6.2 API Response Models
```typescript
// OCR Response
interface OCRResponse {
  text: string;
  confidence?: number;
  success: boolean;
  error?: string;
}

// Label Response
interface LabelResponse {
  filename: string;
  label: string | null;
}

// File List Response
interface FileListResponse {
  files: string[];
  total: number;
}
```

## 7. User Interface Design

### 7.1 Layout Structure
```
┌─────────────────────────────────────────┐
│              Header                     │
│        OCR Labeling Tool                │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────┐   │
│  │             │  │  Label Input    │   │
│  │    Image    │  │  ┌───────────┐  │   │
│  │   Display   │  │  │ Text Area │  │   │
│  │             │  │  └───────────┘  │   │
│  └─────────────┘  │  [Save] [OCR]   │   │
│                   └─────────────────┘   │
├─────────────────────────────────────────┤
│  [◄ Prev] [1/1000] [Progress] [Next ►]  │
├─────────────────────────────────────────┤
│    Jump to: [___] [Go] [Reset All]      │
└─────────────────────────────────────────┘
```
<img width="1919" height="1015" alt="image" src="https://github.com/user-attachments/assets/6680ee3c-5715-4d34-8f68-25c364dac649" />


### 7.2 Responsive Design
- **Desktop**: Side-by-side image and label panel
- **Tablet**: Stacked layout with optimized spacing
- **Mobile**: Single column with touch-friendly controls

### 7.3 User Experience Features
- **Auto-advance**: Move to next image after saving
- **Keyboard Shortcuts**: Navigation and actions
- **Real-time Progress**: Visual progress indicators
- **Unsaved Changes Warning**: Prevent data loss

## 8. Security Considerations

### 8.1 File Access Security
- **Path Validation**: Prevent directory traversal attacks
- **File Type Restrictions**: Only allow image files
- **Sanitized Filenames**: Remove dangerous characters

### 8.2 CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 8.3 Input Validation
- **Filename Validation**: Alphanumeric with safe characters
- **Label Content**: Text sanitization and length limits
- **File Size Limits**: Prevent oversized uploads

## 9. Performance Considerations

### 9.1 OCR Optimization
- **Model Loading**: Load PaddleOCR once at startup
- **GPU Acceleration**: Utilize available GPU resources
- **Batch Processing**: Process multiple images when possible

### 9.2 File System Performance
- **Image Caching**: Browser-level caching for images
- **Lazy Loading**: Load images on demand
- **Efficient File I/O**: Optimized read/write operations

### 9.3 Frontend Performance
- **Component Optimization**: React.memo for expensive components
- **Image Optimization**: Responsive images and compression
- **Bundle Optimization**: Code splitting and tree shaking

## 10. Error Handling

### 10.1 Backend Error Handling
```python
# OCR Processing Errors
- Image format not supported
- OCR engine failures
- File system permissions

# API Error Responses
{
  "error": "descriptive_error_message",
  "code": "ERROR_CODE",
  "details": {}
}
```

### 10.2 Frontend Error Handling
- **Network Errors**: Retry mechanisms and user feedback
- **Loading States**: Proper loading indicators
- **Fallback UI**: Graceful degradation for failures

## 11. Testing Strategy

### 11.1 Backend Testing
- **Unit Tests**: OCR functions, file operations
- **Integration Tests**: API endpoints, database operations
- **Performance Tests**: Load testing for OCR processing

### 11.2 Frontend Testing
- **Component Tests**: UI component functionality
- **Integration Tests**: User workflows and API integration
- **E2E Tests**: Complete user journeys

## 12. Deployment Architecture

### 12.1 Development Environment
```bash
# Backend
cd /project/root
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm start
```

### 12.2 Production Deployment
- **Backend**: Docker container with Uvicorn
- **Frontend**: Static build served by CDN
- **Reverse Proxy**: Nginx for routing and SSL
- **Process Management**: systemd or Docker Compose

## 13. Monitoring and Logging

### 13.1 Application Metrics
- **OCR Processing Time**: Performance monitoring
- **Error Rates**: Failed OCR attempts and API errors
- **User Activity**: Labeling progress and usage patterns

### 13.2 Logging Strategy
```python
# Backend Logging
- INFO: Successful operations
- WARNING: OCR confidence issues
- ERROR: Processing failures
- DEBUG: Detailed processing information
```

## 14. Future Enhancements

### 14.1 Short-term Improvements
- **Batch OCR Processing**: Process multiple images simultaneously
- **Label Export**: Export labels in various formats (JSON, CSV, XML)
- **Image Preprocessing**: Enhance image quality before OCR
- **Undo/Redo**: Action history for label editing

### 14.2 Long-term Roadmap
- **Machine Learning Integration**: Custom OCR model training
- **Collaborative Labeling**: Multi-user support with conflict resolution
- **Advanced Analytics**: OCR accuracy analytics and insights
- **Cloud Storage**: Integration with cloud storage providers
- **API Authentication**: User management and access controls

## 15. Conclusion

The Semi-Auto OCR Tool represents a comprehensive solution for efficient text labeling workflows. The architecture balances simplicity with extensibility, ensuring reliable performance while maintaining the flexibility for future enhancements. The modular design allows for easy maintenance and scaling as requirements evolve.

### Key Success Factors
- **Robust OCR Integration**: High-accuracy text extraction
- **Intuitive User Interface**: Minimal learning curve
- **Efficient Data Management**: Reliable storage and retrieval
- **Performance Optimization**: Fast processing and responsive UI
- **Extensible Architecture**: Ready for future enhancements 
