export interface PDFHeading {
  id: string;
  text: string;
  level: number;
  page: number;
  position: number;
}

export interface PDFData {
  id: string;
  filename: string;
  text: string;
  headings: PDFHeading[];
  summary: string;
  pages: number;
  size: number;
  uploadDate: string;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  references?: PDFHeading[];
}

export interface QAResponse {
  answer: string;
  confidence: number;
  references: PDFHeading[];
}
