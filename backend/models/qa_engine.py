from transformers import pipeline
import torch
from typing import List, Dict, Any
import re

class QAEngine:
    def __init__(self):
        self.qa_pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load the question-answering model"""
        try:
            self.qa_pipeline = pipeline(
                "question-answering",
                model="deepset/roberta-base-squad2",
                tokenizer="deepset/roberta-base-squad2",
                device=0 if torch.cuda.is_available() else -1
            )
            print("QA model loaded successfully")
        except Exception as e:
            print(f"Error loading QA model: {e}")
            self.qa_pipeline = None
    
    def answer_question(self, question: str, context: str, headings: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Answer a question based on the document context"""
        if not self.qa_pipeline:
            return self._fallback_answer(question, context, headings)
        
        try:
            # Limit context length for model (BERT has token limits)
            max_context_length = 4000
            if len(context) > max_context_length:
                # Try to find relevant sections first
                relevant_context = self._find_relevant_context(question, context, max_context_length)
            else:
                relevant_context = context
            
            result = self.qa_pipeline(
                question=question,
                context=relevant_context,
                max_answer_len=200,
                handle_impossible_answer=True
            )
            
            answer = result.get("answer", "")
            confidence = result.get("score", 0.0)
            
            # Find relevant headings
            references = self._find_relevant_headings(answer, headings or [])
            
            return {
                "answer": answer,
                "confidence": float(confidence),
                "references": references
            }
            
        except Exception as e:
            print(f"Error processing question: {e}")
            return self._fallback_answer(question, context, headings)
    
    def _find_relevant_context(self, question: str, context: str, max_length: int) -> str:
        """Find the most relevant part of the context for the question"""
        # Split context into sentences
        sentences = re.split(r'[.!?]+', context)
        
        # Score sentences based on keyword overlap with question
        question_words = set(question.lower().split())
        scored_sentences = []
        
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) < 10:  # Skip very short sentences
                continue
            
            sentence_words = set(sentence.lower().split())
            overlap = len(question_words.intersection(sentence_words))
            scored_sentences.append((overlap, i, sentence))
        
        # Sort by relevance score
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        
        # Build context from most relevant sentences
        relevant_context = ""
        for score, idx, sentence in scored_sentences:
            if len(relevant_context) + len(sentence) > max_length:
                break
            relevant_context += sentence + ". "
        
        return relevant_context if relevant_context else context[:max_length]
    
    def _find_relevant_headings(self, answer: str, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find headings that are relevant to the answer"""
        if not answer or not headings:
            return []
        
        relevant_headings = []
        answer_words = set(answer.lower().split())
        
        for heading in headings:
            heading_words = set(heading.get("text", "").lower().split())
            if heading_words.intersection(answer_words):
                relevant_headings.append(heading)
        
        return relevant_headings[:3]  # Limit to top 3 relevant headings
    
    def _fallback_answer(self, question: str, context: str, headings: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Fallback answer when model is not available"""
        # Simple keyword-based search
        question_words = question.lower().split()
        context_lower = context.lower()
        
        # Find sentences containing question keywords
        sentences = re.split(r'[.!?]+', context)
        relevant_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(word in sentence_lower for word in question_words):
                relevant_sentences.append(sentence.strip())
        
        if relevant_sentences:
            answer = ". ".join(relevant_sentences[:2]) + "."
        else:
            answer = "I couldn't find a specific answer to your question in the document."
        
        return {
            "answer": answer,
            "confidence": 0.5,
            "references": []
        }
