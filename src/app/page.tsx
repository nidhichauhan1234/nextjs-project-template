"use client";

import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { PDFViewer } from "@/components/PDFViewer";
import { ChatInterface } from "@/components/ChatInterface";
import { PDFUploader } from "@/components/PDFUploader";
import { PDFData } from "@/types/pdf";

export default function Home() {
  const [pdfData, setPdfData] = useState<PDFData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handlePDFUpload = async (file: File) => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload PDF");
      }

      const data = await response.json();
      setPdfData(data);
    } catch (error) {
      console.error("Error uploading PDF:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-black">
      <Sidebar 
        pdfData={pdfData} 
        onHeadingClick={(heading) => {
          const element = document.getElementById(`heading-${heading.id}`);
          element?.scrollIntoView({ behavior: "smooth" });
        }}
      />
      
      <main className="flex-1 flex flex-col overflow-hidden">
        {!pdfData ? (
          <div className="flex-1 flex items-center justify-center">
            <PDFUploader onUpload={handlePDFUpload} isLoading={isLoading} />
          </div>
        ) : (
          <>
            <div className="flex-1 overflow-y-auto">
              <PDFViewer pdfData={pdfData} />
            </div>
            <div className="border-t border-gray-800">
              <ChatInterface pdfData={pdfData} />
            </div>
          </>
        )}
      </main>
    </div>
  );
}
