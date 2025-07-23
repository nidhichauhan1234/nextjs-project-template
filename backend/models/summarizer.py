from transformers import pipeline
from typing import List, Dict, Any
import torch

class DocumentSummarizer:
    def __init__(self):
        self.summarizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the summarization model"""
        try:
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=0 if torch.cuda.is_available() else -1
            )
        except Exception as e:
            print(f"Error loading summarization model: {e}")
            self.summarizer = None
    
    def summarize(self, text: str, headings: List[Dict[str, Any]] = None) -> str:
        """Generate summary of the document"""
        if not self.summarizer:
            return self._fallback_summary(text, headings)
        
        # Limit text length for model
        max_length = min(1024, len(text))
        text_to_summarize = text[:max_length]
        
        try:
            summary = self.summarizer(
                text_to_summarize,
                max_length=150,
                min_length=50,
                do_sample=False
            )[0]['summary_text']
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._fallback_summary(text, headings)
    
    def _fallback_summary(self, text: str, headings: List[Dict[str, Any]] = None) -> str:
        """Fallback summary generation when model fails"""
        # Extract key sentences
        sentences = text.split('.')
        key_sentences = []
        
        # Look for sentences with important keywords
        important_keywords = ['important', 'key', 'main', 'significant', 'crucial', 'essential']
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in important_keywords):
                key_sentences.append(sentence.strip())
        
        # If no key sentences found, take first few
        if not key_sentences:
            key_sentences = sentences[:3]
        
        summary = '. '.join(key_sentences) + '.'
        
        # Ensure summary is not too long
        if len(summary) > 300:
            summary = summary[:300] + '...'
        
        return summary
    
    def summarize_by_sections(self, text: str, headings: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate summary for each section based on headings"""
        sections = {}
        
        if not headings:
            return {"full_document": self.summarize(text)}
        
        # Split text by headings
        text_parts = text
        for heading in headings:
            heading_text = heading['text']
            if heading_text in text_parts:
                parts = text_parts.split(heading_text, 1)
                if len(parts) > 1:
                    section_text = parts[1]
                    # Find next heading to limit section
                    next_heading = None
                    for h in headings:
                        if h['position'] > heading['position']:
                            next_heading = h['text']
                            break
                    
                    if next_heading and next_heading in section_text:
                        section_text = section_text.split(next_heading)[0]
                    
                    sections[heading_text] = self.summarize(section_text)
        
        return sections
