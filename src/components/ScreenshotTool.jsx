import React, { useState } from 'react';
import { Camera, Copy, Download } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import html2canvas from 'html2canvas';

const ScreenshotTool = () => {
  const [capturedImage, setCapturedImage] = useState(null);

  const captureScreen = async () => {
    try {
      const canvas = await html2canvas(document.body);
      const imageData = canvas.toDataURL('image/png');
      setCapturedImage(imageData);
      toast.success('Screenshot captured!');
    } catch (error) {
      toast.error('Failed to capture screenshot');
    }
  };

  const copyToClipboard = async () => {
    if (capturedImage) {
      try {
        const blob = await (await fetch(capturedImage)).blob();
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': blob })
        ]);
        toast.success('Screenshot copied to clipboard!');
      } catch (error) {
        toast.error('Failed to copy screenshot');
      }
    }
  };

  const saveImage = () => {
    if (capturedImage) {
      const link = document.createElement('a');
      link.href = capturedImage;
      link.download = 'screenshot.png';
      link.click();
    }
  };

  return (
    <div className="fixed bottom-4 right-4 flex flex-col items-end space-y-2">
      <Button onClick={captureScreen} variant="outline" size="icon">
        <Camera className="h-4 w-4" />
      </Button>
      {capturedImage && (
        <>
          <Button onClick={copyToClipboard} variant="outline" size="icon">
            <Copy className="h-4 w-4" />
          </Button>
          <Button onClick={saveImage} variant="outline" size="icon">
            <Download className="h-4 w-4" />
          </Button>
        </>
      )}
    </div>
  );
};

export default ScreenshotTool;