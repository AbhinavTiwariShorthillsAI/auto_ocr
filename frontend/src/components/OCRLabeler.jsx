import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { Textarea } from './ui/textarea';
import { useToast } from '../hooks/use-toast';
import { Loader2, Eye, Save, SkipForward, RefreshCw, AlertCircle } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

const OCRLabeler = () => {
  const [currentImage, setCurrentImage] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [editedText, setEditedText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [progress, setProgress] = useState({ processed: 0, total: 0 });
  const [error, setError] = useState('');
  const [isLoadingImage, setIsLoadingImage] = useState(false);
  const { toast } = useToast();

  // Load next image on component mount
  useEffect(() => {
    loadNextImage();
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/images`);
      setProgress({
        processed: response.data.processed_images,
        total: response.data.total_images
      });
    } catch (error) {
      console.error('Error loading progress:', error);
    }
  };

  const loadNextImage = async () => {
    setIsLoadingImage(true);
    setError('');
    
    try {
      const response = await axios.get(`${API_BASE_URL}/api/images/next`);
      
      if (response.data.message) {
        // All images processed
        setCurrentImage(null);
        setExtractedText('');
        setEditedText('');
        setError('All images have been processed! 🎉');
        return;
      }
      
      setCurrentImage(response.data);
      setProgress({
        processed: response.data.processed_images,
        total: response.data.total_images
      });
      
      // Automatically perform OCR on the new image
      await performOCR(response.data.image_name);
      
    } catch (error) {
      console.error('Error loading next image:', error);
      setError('Failed to load next image. Please try again.');
      toast({
        title: "Error",
        description: "Failed to load next image",
        variant: "destructive",
      });
    } finally {
      setIsLoadingImage(false);
    }
  };

  const performOCR = async (imageName) => {
    if (!imageName) return;
    
    setIsProcessing(true);
    setError('');
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/ocr/file`, null, {
        params: { image_name: imageName }
      });
      
      if (response.data.success) {
        setExtractedText(response.data.extracted_text);
        setEditedText(response.data.extracted_text);
        
        if (!response.data.extracted_text) {
          setError('No text detected in this image.');
        }
      } else {
        setError('OCR processing failed. Please try again.');
      }
      
    } catch (error) {
      console.error('Error performing OCR:', error);
      setError('Failed to extract text. Please try again.');
      toast({
        title: "OCR Error",
        description: "Failed to extract text from image",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const saveLabel = async () => {
    if (!currentImage || !editedText.trim()) {
      toast({
        title: "Error",
        description: "Please enter some text before saving",
        variant: "destructive",
      });
      return;
    }
    
    setIsSaving(true);
    
    try {
      const formData = new FormData();
      formData.append('image_name', currentImage.image_name);
      formData.append('corrected_text', editedText.trim());
      
      const response = await axios.post(`${API_BASE_URL}/api/save`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      if (response.data.success) {
        toast({
          title: "Success",
          description: `Label saved for ${currentImage.image_name}`,
        });
        
        // Move to next image
        await loadNextImage();
      } else {
        setError('Failed to save label. Please try again.');
      }
      
    } catch (error) {
      console.error('Error saving label:', error);
      setError('Failed to save label. Please try again.');
      toast({
        title: "Save Error",
        description: "Failed to save label",
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
    }
  };

  const skipImage = async () => {
    toast({
      title: "Skipped",
      description: `Skipped ${currentImage?.image_name}`,
    });
    await loadNextImage();
  };

  const retryOCR = async () => {
    if (currentImage) {
      await performOCR(currentImage.image_name);
    }
  };

  const progressPercentage = progress.total > 0 ? (progress.processed / progress.total) * 100 : 0;

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">OCR Labeling Tool</h1>
        <p className="text-gray-600">Extract and correct text from images</p>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm text-gray-600">
          <span>Progress</span>
          <span>{progress.processed} / {progress.total} images</span>
        </div>
        <Progress value={progressPercentage} className="h-2" />
        <div className="text-center text-sm text-gray-500">
          {progressPercentage.toFixed(1)}% complete
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex items-center space-x-2">
          <AlertCircle className="h-5 w-5 text-yellow-600" />
          <span className="text-yellow-800">{error}</span>
        </div>
      )}

      {/* Main Content */}
      {currentImage ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Image Display */}
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow-sm border p-4">
              <h2 className="text-lg font-semibold mb-3 flex items-center">
                <Eye className="h-5 w-5 mr-2" />
                Current Image
              </h2>
              <div className="relative">
                {isLoadingImage ? (
                  <div className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
                    <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
                  </div>
                ) : (
                  <img
                    src={`${API_BASE_URL}${currentImage.image_url}`}
                    alt={currentImage.image_name}
                    className="w-full h-auto rounded-lg border"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      setError('Failed to load image');
                    }}
                  />
                )}
              </div>
              <p className="text-sm text-gray-600 mt-2 text-center">
                {currentImage.image_name}
              </p>
            </div>
          </div>

          {/* Text Editing */}
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow-sm border p-4">
              <h2 className="text-lg font-semibold mb-3">Extracted Text</h2>
              
              {/* OCR Processing Indicator */}
              {isProcessing && (
                <div className="flex items-center space-x-2 mb-3 p-3 bg-blue-50 rounded-lg">
                  <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
                  <span className="text-blue-800 text-sm">Processing image...</span>
                </div>
              )}
              
              {/* Original extracted text display */}
              {extractedText && (
                <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-500 mb-1">Original OCR Result:</p>
                  <p className="text-sm text-gray-700">{extractedText}</p>
                </div>
              )}
              
              {/* Editable text area */}
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">
                  Corrected Text:
                </label>
                <Textarea
                  value={editedText}
                  onChange={(e) => setEditedText(e.target.value)}
                  placeholder="Edit the extracted text or enter text manually..."
                  className="min-h-[120px] resize-none"
                  disabled={isProcessing}
                />
              </div>
              
              {/* OCR Retry Button */}
              <div className="mt-3">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={retryOCR}
                  disabled={isProcessing || isLoadingImage}
                  className="w-full"
                >
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Retry OCR
                </Button>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="text-center py-12">
          <div className="max-w-md mx-auto">
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <h2 className="text-xl font-semibold text-green-800 mb-2">
                All Done! 🎉
              </h2>
              <p className="text-green-700">
                You've successfully processed all images in the folder.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      {currentImage && (
        <div className="flex justify-center space-x-4">
          <Button
            variant="outline"
            onClick={skipImage}
            disabled={isProcessing || isSaving || isLoadingImage}
            className="flex items-center space-x-2"
          >
            <SkipForward className="h-4 w-4" />
            <span>Skip</span>
          </Button>
          
          <Button
            onClick={saveLabel}
            disabled={isProcessing || isSaving || isLoadingImage || !editedText.trim()}
            className="flex items-center space-x-2"
          >
            {isSaving ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Save className="h-4 w-4" />
            )}
            <span>{isSaving ? 'Saving...' : 'Save & Next'}</span>
          </Button>
        </div>
      )}
    </div>
  );
};

export default OCRLabeler; 