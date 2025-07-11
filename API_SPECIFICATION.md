# Semi-Auto OCR Tool - API Specification

## Overview
This document provides detailed specifications for all API endpoints in the Semi-Auto OCR Tool backend service.

**Base URL**: `http://localhost:8000`  
**API Version**: 1.0  
**Content-Type**: `application/json`

## Authentication
Currently, the API does not require authentication. For production deployments, consider implementing API key or OAuth2 authentication.

## Endpoints

### 1. Health Check

#### GET `/`
Returns basic API information and health status.

**Request**
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response**
```json
{
  "message": "Semi-Auto OCR Tool API",
  "version": "1.0",
  "status": "healthy"
}
```

**Status Codes**
- `200 OK`: Service is healthy

---

### 2. Image Serving

#### GET `/images/{filename}`
Serves image files from the images directory.

**Parameters**
- `filename` (path, required): Name of the image file

**Request**
```http
GET /images/train_1_0.jpg HTTP/1.1
Host: localhost:8000
```

**Response**
- **Content-Type**: `image/jpeg` or `image/png`
- **Body**: Binary image data

**Status Codes**
- `200 OK`: Image found and served
- `404 Not Found`: Image file does not exist
- `400 Bad Request`: Invalid filename

**Error Response Example**
```json
{
  "detail": "Image not found: train_1_0.jpg"
}
```

---

### 3. File Listing

#### GET `/files`
Returns a list of all image files in the images directory, sorted naturally.

**Request**
```http
GET /files HTTP/1.1
Host: localhost:8000
```

**Response**
```json
{
  "files": [
    "train_1_0.jpg",
    "train_1_1.jpg",
    "train_2_0.jpg",
    "train_10_0.jpg",
    "train_100_0.jpg"
  ],
  "total": 5
}
```

**Status Codes**
- `200 OK`: File list retrieved successfully
- `500 Internal Server Error`: Unable to read images directory

---

### 4. OCR Processing

#### POST `/ocr/{filename}`
Processes an image file using PaddleOCR to extract text.

**Parameters**
- `filename` (path, required): Name of the image file to process

**Request**
```http
POST /ocr/train_1_0.jpg HTTP/1.1
Host: localhost:8000
```

**Response**
```json
{
  "text": "Sample extracted text from the image",
  "confidence": 0.95,
  "processing_time": 1.23,
  "success": true
}
```

**Error Response**
```json
{
  "error": "Failed to process image",
  "details": "Image format not supported",
  "success": false
}
```

**Status Codes**
- `200 OK`: OCR processing completed (check `success` field)
- `404 Not Found`: Image file does not exist
- `400 Bad Request`: Invalid filename or unsupported format
- `500 Internal Server Error`: OCR processing failed

---

### 5. Label Management

#### GET `/labels/{filename}`
Retrieves the existing label for a specific image.

**Parameters**
- `filename` (path, required): Name of the image file

**Request**
```http
GET /labels/train_1_0.jpg HTTP/1.1
Host: localhost:8000
```

**Response**
```json
{
  "filename": "train_1_0.jpg",
  "label": "Sample label text"
}
```

**Response (No Label)**
```json
{
  "filename": "train_1_0.jpg",
  "label": null
}
```

**Status Codes**
- `200 OK`: Label retrieved (may be null if no label exists)
- `400 Bad Request`: Invalid filename

---

#### POST `/labels/{filename}`
Saves or updates a label for a specific image.

**Parameters**
- `filename` (path, required): Name of the image file

**Request Body**
```json
{
  "label": "Updated label text"
}
```

**Request**
```http
POST /labels/train_1_0.jpg HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "label": "Updated label text"
}
```

**Response**
```json
{
  "message": "Label saved successfully",
  "filename": "train_1_0.jpg",
  "label": "Updated label text"
}
```

**Status Codes**
- `200 OK`: Label saved successfully
- `400 Bad Request`: Invalid filename or request body
- `500 Internal Server Error`: Failed to save label

---

#### GET `/labels`
Retrieves all labels from the labels.txt file.

**Request**
```http
GET /labels HTTP/1.1
Host: localhost:8000
```

**Response**
```json
{
  "train_1_0.jpg": "First image label",
  "train_1_1.jpg": "Second image label",
  "train_2_0.jpg": null
}
```

**Status Codes**
- `200 OK`: Labels retrieved successfully
- `500 Internal Server Error`: Failed to read labels file

---

## Data Models

### OCR Response Model
```typescript
interface OCRResponse {
  text: string;                    // Extracted text content
  confidence?: number;             // OCR confidence score (0-1)
  processing_time?: number;        // Processing time in seconds
  success: boolean;                // Whether OCR was successful
  error?: string;                  // Error message if success is false
  details?: string;                // Additional error details
}
```

### Label Request Model
```typescript
interface LabelRequest {
  label: string;                   // Label text content
}
```

### Label Response Model
```typescript
interface LabelResponse {
  filename: string;                // Image filename
  label: string | null;            // Label text or null if no label
  message?: string;                // Success/error message
}
```

### File List Response Model
```typescript
interface FileListResponse {
  files: string[];                 // Array of image filenames
  total: number;                   // Total number of files
}
```

## Error Handling

### Standard Error Response
```typescript
interface ErrorResponse {
  detail: string;                  // Error description
  error_code?: string;             // Machine-readable error code
  timestamp?: string;              // ISO timestamp of error
}
```

### Common Error Codes
- `FILE_NOT_FOUND`: Requested file does not exist
- `INVALID_FILENAME`: Filename contains invalid characters
- `OCR_PROCESSING_FAILED`: PaddleOCR processing failed
- `LABEL_SAVE_FAILED`: Unable to save label to file
- `INVALID_REQUEST_BODY`: Request body validation failed

## Rate Limiting
Currently, no rate limiting is implemented. For production use, consider implementing:
- Per-IP rate limiting
- OCR processing queue management
- Request timeout handling

## CORS Configuration
The API is configured to accept requests from:
- `http://localhost:3000` (development frontend)

Additional origins can be configured in the FastAPI CORS middleware.

## Examples

### Complete Labeling Workflow

1. **Get list of images**
```bash
curl -X GET "http://localhost:8000/files"
```

2. **Process first image with OCR**
```bash
curl -X POST "http://localhost:8000/ocr/train_1_0.jpg"
```

3. **Save the label**
```bash
curl -X POST "http://localhost:8000/labels/train_1_0.jpg" \
  -H "Content-Type: application/json" \
  -d '{"label": "Extracted text here"}'
```

4. **Retrieve saved label**
```bash
curl -X GET "http://localhost:8000/labels/train_1_0.jpg"
```

### Batch Operations

**Get all labels at once**
```bash
curl -X GET "http://localhost:8000/labels"
```

## Security Considerations

### Input Validation
- Filenames are validated against a whitelist pattern
- Label content is sanitized to prevent injection attacks
- File paths are resolved securely to prevent directory traversal

### File Access
- Only files within the designated images directory are accessible
- File existence is checked before processing
- Invalid file paths return appropriate error responses

## Performance Notes

### OCR Processing
- PaddleOCR model is loaded once at application startup
- Processing time varies based on image complexity (typically 1-5 seconds)
- Consider implementing caching for frequently processed images

### File Operations
- File listing is performed synchronously (consider caching for large directories)
- Label operations use file locking to prevent concurrent modification issues
- Natural sorting is performed in-memory (efficient for typical dataset sizes)

## Monitoring and Logging

The API logs the following events:
- OCR processing requests and results
- Label save/update operations
- File access attempts
- Error conditions

Log levels:
- `INFO`: Successful operations
- `WARNING`: Potential issues (low OCR confidence)
- `ERROR`: Processing failures
- `DEBUG`: Detailed processing information 