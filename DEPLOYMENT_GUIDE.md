# Semi-Auto OCR Tool - Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+ recommended), macOS, or Windows 10/11
- **Python**: 3.10 or higher
- **Node.js**: 16.0 or higher
- **RAM**: Minimum 4GB, 8GB+ recommended for OCR processing
- **Storage**: 10GB+ free space for images and dependencies
- **GPU**: Optional but recommended for faster OCR processing

### Software Dependencies
- Git
- Python pip
- Node.js npm
- Virtual environment tools (venv)

## Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-repo/auto_ocr.git
cd auto_ocr
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify PaddleOCR installation
python -c "import paddleocr; print('PaddleOCR installed successfully')"
```

#### Prepare Data Directory
```bash
# Create images directory if it doesn't exist
mkdir -p images

# Copy your training images to the images directory
# Images should be named in format: train_X_Y.jpg

# Create empty labels file
touch labels.txt
```

#### Start Backend Server
```bash
# Development server
python main.py

# The API will be available at http://localhost:8000
```

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Start Development Server
```bash
npm start

# The frontend will be available at http://localhost:3000
```

### 4. Verify Installation
1. Open browser to `http://localhost:3000`
2. Verify that images load correctly
3. Test OCR functionality on a sample image
4. Test label saving and retrieval

## Production Deployment

### 1. Server Preparation

#### System Updates
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx
```

#### Create Application User
```bash
sudo useradd -m -s /bin/bash ocrapp
sudo usermod -aG sudo ocrapp
sudo su - ocrapp
```

### 2. Application Deployment

#### Deploy Backend
```bash
# Clone repository
git clone https://github.com/your-repo/auto_ocr.git /opt/ocrapp
cd /opt/ocrapp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production ASGI server
pip install uvicorn[standard] gunicorn

# Create systemd service
sudo tee /etc/systemd/system/ocrapp-backend.service > /dev/null <<EOF
[Unit]
Description=OCR App Backend
After=network.target

[Service]
Type=exec
User=ocrapp
Group=ocrapp
WorkingDirectory=/opt/ocrapp
Environment=PATH=/opt/ocrapp/venv/bin
ExecStart=/opt/ocrapp/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable ocrapp-backend
sudo systemctl start ocrapp-backend
```

#### Deploy Frontend
```bash
cd /opt/ocrapp/frontend

# Install dependencies
npm ci --only=production

# Build for production
npm run build

# Copy build files to web server directory
sudo cp -r build/* /var/www/html/
```

### 3. Reverse Proxy Configuration

#### Nginx Configuration
```bash
sudo tee /etc/nginx/sites-available/ocrapp > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    # Frontend static files
    location / {
        root /var/www/html;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Image files
    location /images/ {
        proxy_pass http://localhost:8000/images/;
        proxy_set_header Host \$host;
    }

    # Increase upload size for large images
    client_max_body_size 50M;
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/ocrapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. SSL Configuration (Optional but Recommended)

#### Using Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

## Docker Deployment

### 1. Backend Dockerfile
```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create images directory
RUN mkdir -p images

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Frontend Dockerfile
```dockerfile
# frontend/Dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

### 3. Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./images:/app/images
      - ./labels.txt:/app/labels.txt
    environment:
      - PYTHONPATH=/app
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped
```

### 4. Run with Docker Compose
```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Environment Configuration

### 1. Environment Variables

#### Backend Configuration
```bash
# .env file for backend
PORT=8000
HOST=0.0.0.0
IMAGES_DIR=./images
LABELS_FILE=./labels.txt
OCR_USE_GPU=false
OCR_USE_ANGLE_CLS=true
OCR_USE_SPACE_CHAR=true
LOG_LEVEL=INFO
```

#### Frontend Configuration
```bash
# .env file for frontend
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_TITLE=Semi-Auto OCR Tool
REACT_APP_VERSION=1.0.0
```

### 2. Production Environment
```bash
# Production backend environment
PORT=8000
HOST=0.0.0.0
IMAGES_DIR=/data/images
LABELS_FILE=/data/labels.txt
OCR_USE_GPU=true
LOG_LEVEL=WARNING
CORS_ORIGINS=https://your-domain.com
```

## Monitoring and Maintenance

### 1. Log Management

#### Backend Logs
```bash
# View application logs
sudo journalctl -u ocrapp-backend -f

# Rotate logs
sudo logrotate -f /etc/logrotate.conf
```

#### Nginx Logs
```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

### 2. Health Monitoring

#### Create Health Check Script
```bash
#!/bin/bash
# health_check.sh

# Check backend health
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
if [ $BACKEND_STATUS -ne 200 ]; then
    echo "Backend health check failed: $BACKEND_STATUS"
    exit 1
fi

# Check frontend availability
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
if [ $FRONTEND_STATUS -ne 200 ]; then
    echo "Frontend health check failed: $FRONTEND_STATUS"
    exit 1
fi

echo "All services healthy"
```

#### Cron Job for Health Checks
```bash
# Add to crontab
*/5 * * * * /opt/ocrapp/health_check.sh >> /var/log/ocrapp_health.log 2>&1
```

### 3. Backup Strategy

#### Database Backup (Labels)
```bash
#!/bin/bash
# backup_labels.sh

BACKUP_DIR="/backup/ocrapp"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup labels file
cp /opt/ocrapp/labels.txt $BACKUP_DIR/labels_$DATE.txt

# Keep only last 30 days of backups
find $BACKUP_DIR -name "labels_*.txt" -mtime +30 -delete
```

### 4. Performance Monitoring

#### System Resource Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor CPU and memory usage
htop

# Monitor disk I/O
iotop

# Monitor network usage
nethogs
```

## Troubleshooting

### Common Issues

#### 1. OCR Processing Fails
```bash
# Check PaddleOCR installation
python -c "import paddleocr; ocr = paddleocr.PaddleOCR(); print('OCR OK')"

# Check image file permissions
ls -la images/

# Check available memory
free -h

# Check GPU availability (if using)
nvidia-smi
```

#### 2. CORS Errors
```bash
# Check CORS configuration in main.py
grep -n "CORS" main.py

# Verify frontend URL in CORS origins
curl -I -X OPTIONS http://localhost:8000/ -H "Origin: http://localhost:3000"
```

#### 3. File Not Found Errors
```bash
# Check images directory
ls -la images/

# Check file permissions
chmod 755 images/
chmod 644 images/*.jpg

# Check labels file
touch labels.txt
chmod 644 labels.txt
```

#### 4. Service Won't Start
```bash
# Check service status
sudo systemctl status ocrapp-backend

# Check service logs
sudo journalctl -u ocrapp-backend -n 50

# Check port availability
sudo netstat -tlnp | grep :8000

# Restart service
sudo systemctl restart ocrapp-backend
```

#### 5. High Memory Usage
```bash
# Monitor memory usage
ps aux | grep python | head -10

# Check for memory leaks
sudo apt install valgrind
valgrind --tool=memcheck python main.py

# Restart service to clear memory
sudo systemctl restart ocrapp-backend
```

### Performance Optimization

#### 1. OCR Optimization
- Use GPU acceleration when available
- Process images in batches
- Implement result caching
- Optimize image preprocessing

#### 2. Frontend Optimization
- Enable gzip compression in Nginx
- Implement image lazy loading
- Use browser caching
- Minimize bundle size

#### 3. Backend Optimization
- Use async/await for I/O operations
- Implement connection pooling
- Enable HTTP/2 in Nginx
- Use CDN for static assets

## Security Checklist

- [ ] Update all system packages
- [ ] Configure firewall (UFW or iptables)
- [ ] Enable SSL/HTTPS
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Monitor access logs
- [ ] Backup sensitive data
- [ ] Use strong passwords
- [ ] Implement proper file permissions
- [ ] Regular security audits

## Maintenance Schedule

### Daily
- Monitor service health
- Check disk space
- Review error logs

### Weekly
- Update system packages
- Rotate log files
- Backup label data
- Performance review

### Monthly
- Security patch updates
- Full system backup
- Performance optimization
- Capacity planning review 