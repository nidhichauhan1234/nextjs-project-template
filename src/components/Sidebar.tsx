"use client";

import { useState } from "react";
import { PDFData, PDFHeading } from "@/types/pdf";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

interface SidebarProps {
  pdfData: PDFData | null;
  onHeadingClick: (heading: PDFHeading) => void;
}

export function Sidebar({ pdfData, onHeadingClick }: SidebarProps) {
  const [activeTab, setActiveTab] = useState<'headings' | 'summary' | 'chat'>('headings');

  if (!pdfData) {
    return (
      <div className="w-80 bg-gray-900 border-r border-gray-800 p-4">
        <div className="flex items-center space-x-2 mb-6">
          <div className="w-8 h-8 bg-red-500 rounded flex items-center justify-center">
            <span className="text-white text-sm font-bold">PDF</span>
          </div>
          <h2 className="text-lg font-semibold text-white">PDF Assistant</h2>
        </div>
        <div className="text-center text-gray-400 mt-8">
          <p>Upload a PDF to get started</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-80 bg-gray-900 border-r border-gray-800 flex flex-col">
      <div className="p-4 border-b border-gray-800">
        <div className="flex items-center space-x-2 mb-4">
          <div className="w-8 h-8 bg-red-500 rounded flex items-center justify-center">
            <span className="text-white text-sm font-bold">PDF</span>
          </div>
          <h2 className="text-lg font-semibold text-white truncate">{pdfData.filename}</h2>
        </div>
        
        <div className="flex space-x-1">
          <Button
            variant={activeTab === 'headings' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setActiveTab('headings')}
            className="flex-1"
          >
            <span className="text-xs mr-1">#</span>
            Headings
          </Button>
          <Button
            variant={activeTab === 'summary' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setActiveTab('summary')}
            className="flex-1"
          >
            <span className="text-xs mr-1">∑</span>
            Summary
          </Button>
          <Button
            variant={activeTab === 'chat' ? 'default' : 'ghost'}
            size="sm"
            onClick={() => setActiveTab('chat')}
            className="flex-1"
          >
            <span className="text-xs mr-1">💬</span>
            Chat
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1">
        <div className="p-4">
          {activeTab === 'headings' && (
            <div className="space-y-2">
              <h3 className="text-sm font-medium text-gray-300 mb-3">Document Headings</h3>
              {pdfData.headings.length > 0 ? (
                pdfData.headings.map((heading) => (
                  <Button
                    key={heading.id}
                    variant="ghost"
                    size="sm"
                    className="w-full justify-start text-left hover:bg-gray-800"
                    onClick={() => onHeadingClick(heading)}
                  >
                    <div className="flex items-center space-x-2">
                      <span className="text-red-500 text-xs">→</span>
                      <span 
                        className="text-sm text-gray-300 truncate"
                        style={{ paddingLeft: `${(heading.level - 1) * 12}px` }}
                      >
                        {heading.text}
                      </span>
                      <Badge variant="outline" className="ml-auto text-xs border-gray-600 text-gray-500">
                        p.{heading.page}
                      </Badge>
                    </div>
                  </Button>
                ))
              ) : (
                <p className="text-sm text-gray-500">No headings detected</p>
              )}
            </div>
          )}

          {activeTab === 'summary' && (
            <div className="space-y-3">
              <h3 className="text-sm font-medium text-gray-300 mb-3">Document Summary</h3>
              <div className="text-sm text-gray-400 leading-relaxed">
                {pdfData.summary || "No summary available"}
              </div>
              <div className="flex items-center space-x-2 text-xs text-gray-500">
                <Badge variant="outline" className="border-red-500 text-red-500">
                  {pdfData.pages} pages
                </Badge>
                <Badge variant="outline" className="border-red-500 text-red-500">
                  {Math.round(pdfData.size / 1024)} KB
                </Badge>
              </div>
            </div>
          )}

          {activeTab === 'chat' && (
            <div className="space-y-3">
              <h3 className="text-sm font-medium text-gray-300 mb-3">Ask Questions</h3>
              <div className="text-xs text-gray-400">
                Ask questions about your PDF document using the chat interface below.
              </div>
              <div className="bg-gray-800 rounded-lg p-3">
                <p className="text-xs text-gray-500 mb-2">Example questions:</p>
                <ul className="text-xs text-gray-400 space-y-1">
                  <li>• What is the main topic?</li>
                  <li>• Summarize the key points</li>
                  <li>• What are the conclusions?</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
