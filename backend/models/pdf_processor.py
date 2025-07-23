import fitz  # PyMuPDF
import re
from typing import List, Dict, Any
import uuid
from datetime import datetime

class PDFProcessor:
    def __init__(self):
        pass
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    def extract_headings(self, text: str) -> List[Dict[str, Any]]:
        """Extract headings from PDF text"""
        headings = []
        
        # Common heading patterns
        heading_patterns = [
            r'^(#{1,6})\s*(.+)$',  # Markdown-style headings
            r'^(\d+\.)\s*(.+)$',  # Numbered headings
            r'^([A-Z][a-zA-Z\s]+)$',  # Capitalized headings
            r'^(Chapter|Section|Part)\s+\d+\s*(.+)$',  # Chapter/Section headings
        ]
        
        lines = text.split('\n')
        position = 0
        
        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for heading patterns
            for pattern in heading_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    level = 1  # Default level
                    text = line
                    
                    # Determine level based on pattern
                    if match.group(1) and match.group(1).startswith('#'):
                        level = len(match.group(1))
                    
                    headings.append({
                        "id": str(uuid.uuid4()),
                        "text": line,
                        "level": level,
                        "page": 1,  # Simplified for now
                        "position": position
                    })
                    position += 1
                    break
        
        return headings
    
    def process_pdf(self, file_content, filename: str) -> Dict[str, Any]:
        """Process PDF and return structured data"""
        # Save file temporarily
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(file_content.read())
            tmp_path = tmp_file.name
        
        try:
            # Extract text
            text = self.extract_text(tmp_path)
            
            # Extract headings
            headings = self.extract_headings(text)
            
            # Generate summary (placeholder)
            summary = self._generate_summary(text, headings)
            
            # Get file info
            import os
            file_size = os.path.getsize(tmp_path)
            
            return {
                "id": str(uuid.uuid4()),
                "filename": filename,
                "text": text,
                "headings": headings,
                "summary": summary,
                "pages": 1,  # Simplified for now
                "size": file_size,
                "upload_date": datetime.now().isoformat()
            }
        finally:
            os.unlink(tmp_path)
    
    def _generate_summary(self, text: str, headings: List[Dict[str, Any]]) -> str:
        """Generate a simple summary"""
        # Simple summary generation - in real app, use AI model
        sentences = text.split('.')
        summary = ' '.join(sentences[:5]) + "..."
        return summary
