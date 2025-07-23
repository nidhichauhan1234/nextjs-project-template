"use client";

import { useState } from "react";
import { PDFData } from "@/types/pdf";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

interface PDFViewerProps {
  pdfData: PDFData;
}

export function PDFViewer({ pdfData }: PDFViewerProps) {
  const [selectedText, setSelectedText] = useState("");
  const [highlightedSections, setHighlightedSections] = useState<string[]>([]);

  const handleTextSelection = () => {
    const selection = window.getSelection()?.toString() || "";
    setSelectedText(selection);
  };

  const highlightHeading = (headingId: string) => {
    setHighlightedSections(prev => 
      prev.includes(headingId) 
        ? prev.filter(id => id !== headingId)
        : [...prev, headingId]
    );
  };

  const renderTextWithHighlights = (text: string) => {
    let processedText = text;
    
    // Highlight important headings
    pdfData.headings.forEach(heading => {
      const regex = new RegExp(`(${heading.text})`, 'gi');
      processedText = processedText.replace(regex, `<mark id="heading-${heading.id}" class="bg-red-500/20 text-red-300 px-1 rounded">$1</mark>`);
    });

    return { __html: processedText };
  };

  return (
    <div className="h-full bg-black">
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-white mb-2">{pdfData.filename}</h1>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="border-red-500 text-red-500">
                {pdfData.pages} pages
              </Badge>
              <Badge variant="outline" className="border-red-500 text-red-500">
                {Math.round(pdfData.size / 1024)} KB
              </Badge>
              <span className="text-sm text-gray-400">
                Uploaded: {new Date(pdfData.uploadDate).toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>

        <Card className="bg-gray-900 border-gray-800">
          <ScrollArea className="h-[calc(100vh-200px)]">
            <div 
              className="p-6 text-gray-300 leading-relaxed whitespace-pre-wrap"
              onMouseUp={handleTextSelection}
              dangerouslySetInnerHTML={renderTextWithHighlights(pdfData.text)}
            />
          </ScrollArea>
        </Card>

        {selectedText && (
          <div className="fixed bottom-20 right-4 bg-gray-800 border border-gray-700 rounded-lg p-3 max-w-xs">
            <p className="text-sm text-gray-300 mb-2">Selected text:</p>
            <p className="text-xs text-gray-400 truncate">{selectedText}</p>
          </div>
        )}
      </div>
    </div>
  );
}
