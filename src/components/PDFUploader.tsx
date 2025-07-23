"use client";

import { useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

interface PDFUploaderProps {
  onUpload: (file: File) => void;
  isLoading: boolean;
}

export function PDFUploader({ onUpload, isLoading }: PDFUploaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === "application/pdf") {
      onUpload(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type === "application/pdf") {
      onUpload(file);
    }
  };

  return (
    <Card className="w-full max-w-md mx-4 bg-gray-900 border-gray-800">
      <CardHeader>
        <CardTitle className="text-white">Upload PDF Document</CardTitle>
        <CardDescription className="text-gray-400">
          Drop your PDF file here or click to browse
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div
          className="border-2 border-dashed border-gray-700 rounded-lg p-8 text-center hover:border-red-500 transition-colors cursor-pointer"
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="hidden"
          />
          
          {isLoading ? (
            <div className="flex flex-col items-center space-y-4">
              <div className="w-12 h-12 border-4 border-red-500 border-t-transparent rounded-full animate-spin"></div>
              <p className="text-gray-300">Processing your PDF...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center space-y-4">
              <div className="w-16 h-16 bg-red-500 rounded-lg flex items-center justify-center">
                <span className="text-white text-2xl font-bold">PDF</span>
              </div>
              <div>
                <p className="text-gray-300 mb-2">Drag & drop your PDF here</p>
                <p className="text-sm text-gray-500">or click to select file</p>
              </div>
              <Button 
                variant="outline" 
                className="border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
              >
                Choose File
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
