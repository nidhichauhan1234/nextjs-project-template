import fitz  # PyMuPDF
import re
from typing import List, Dict, Any
import uuid
from datetime import datetime
import tempfile
import os
import io

class PDFProcessor:
    def __init__(self):
        pass
    
    def extract_text_and_metadata(self, file_content: bytes) -> Dict[str, Any]:
        """Extract text and metadata from PDF file content"""
        try:
            # Open PDF from bytes
            doc = fitz.open(stream=file_content, filetype="pdf")
            
            text = ""
            page_texts = []
            total_pages = len(doc)
            
            # Extract text from each page
            for page_num in range(total_pages):
                page = doc[page_num]
                page_text = page.get_text()
                text += page_text + "\n"
                page_texts.append({
                    "page": page_num + 1,
                    "text": page_text
                })
            
            doc.close()
            
            return {
                "text": text,
                "pages": total_pages,
                "page_texts": page_texts
            }
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def extract_headings(self, text: str, page_texts: List[Dict] = None) -> List[Dict[str, Any]]:
        """Extract headings from PDF text with improved detection"""
        headings = []
        
        # Enhanced heading patterns
        heading_patterns = [
            (r'^(#{1,6})\s*(.+)$', lambda m: len(m.group(1))),  # Markdown headings
            (r'^(\d+\.(?:\d+\.)*)\s*(.+)$', lambda m: m.group(1).count('.') + 1),  # Numbered headings
            (r'^(Chapter|Section|Part|Article)\s+\d+[:\.\s]*(.*)$', lambda m: 1),  # Chapter/Section
            (r'^([A-Z][A-Z\s]{2,}[A-Z])$', lambda m: 2),  # ALL CAPS headings
            (r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):?\s*$', lambda m: 3),  # Title Case headings
            (r'^(\d+\.\s*[A-Z][a-z].*)$', lambda m: 2),  # Numbered sections
        ]
        
        lines = text.split('\n')
        position = 0
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) < 3:
                continue
            
            # Skip lines that are too long (likely paragraphs)
            if len(line) > 100:
                continue
            
            # Check for heading patterns
            for pattern, level_func in heading_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    try:
                        level = level_func(match)
                        
                        # Determine page number if page_texts available
                        page_num = 1
                        if page_texts:
                            char_count = 0
                            for page_data in page_texts:
                                char_count += len(page_data["text"])
                                if char_count >= sum(len(l) for l in lines[:line_num]):
                                    page_num = page_data["page"]
                                    break
                        
                        headings.append({
                            "id": str(uuid.uuid4()),
                            "text": line,
                            "level": min(level, 6),  # Cap at level 6
                            "page": page_num,
                            "position": position
                        })
                        position += 1
                        break
                    except:
                        continue
        
        return headings
    
    def process_pdf(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process PDF and return structured data"""
        try:
            # Extract text and metadata
            extraction_result = self.extract_text_and_metadata(file_content)
            text = extraction_result["text"]
            pages = extraction_result["pages"]
            page_texts = extraction_result["page_texts"]
            
            # Extract headings with page information
            headings = self.extract_headings(text, page_texts)
            
            # Generate summary using the summarizer
            from .summarizer import DocumentSummarizer
            summarizer = DocumentSummarizer()
            summary = summarizer.summarize(text, headings)
            
            # Get file size
            file_size = len(file_content)
            
            return {
                "id": str(uuid.uuid4()),
                "filename": filename,
                "text": text,
                "headings": headings,
                "summary": summary,
                "pages": pages,
                "size": file_size,
                "upload_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")
    
    def extract_section_text(self, text: str, heading: Dict[str, Any], headings: List[Dict[str, Any]]) -> str:
        """Extract text for a specific section based on heading"""
        try:
            heading_text = heading["text"]
            heading_pos = heading["position"]
            
            # Find the start of this section
            start_idx = text.find(heading_text)
            if start_idx == -1:
                return ""
            
            # Find the next heading to determine section end
            next_heading = None
            for h in headings:
                if h["position"] > heading_pos and h["level"] <= heading["level"]:
                    next_heading = h
                    break
            
            if next_heading:
                end_idx = text.find(next_heading["text"], start_idx + len(heading_text))
                if end_idx != -1:
                    return text[start_idx:end_idx].strip()
            
            # If no next heading found, take rest of text
            return text[start_idx:].strip()
            
        except Exception:
            return ""
