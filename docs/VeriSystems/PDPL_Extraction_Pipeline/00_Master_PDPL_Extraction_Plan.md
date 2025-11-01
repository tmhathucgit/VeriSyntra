# PDPL Extraction Pipeline - Master Implementation Plan

**Project**: VeriSyntra PDPL 91/2025/QH15 Knowledge Base Extraction  
**Purpose**: Extract official Vietnamese PDPL law text to enhance AI model training  
**Timeline**: 3-4 weeks (one-time infrastructure investment)  
**Team**: 1 Python Developer + 1 Vietnamese Legal Expert  
**Output**: Reusable PDPL knowledge base for Phases 0-3

---

## Executive Summary

This master plan outlines the complete pipeline to extract, parse, structure, and convert the Vietnamese PDPL 91/2025/QH15 PDF into training-ready JSON datasets for all VeriAIDPO model training phases.

**Key Deliverables:**
1. Raw Vietnamese text extraction (preserving diacritics)
2. Structured hierarchical parsing (chapters, articles, clauses, points)
3. Category mapping to 8 PDPL principles
4. Phase-specific JSON training datasets
5. Quality validation framework
6. Reusable infrastructure for future legal document processing

**Strategic Value:**
- **Competitive Moat**: Only Vietnamese platform trained on official PDPL text
- **Legal Authority**: Cite exact article numbers in AI recommendations
- **Accuracy Boost**: Expected +1-3% improvement across all models
- **Enterprise Credibility**: "Trained on the actual law, not just examples"

---

## Pipeline Architecture Overview

```
[INPUT: PDPL 91/2025/QH15 PDF]
         |
         v
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: PDF TEXT EXTRACTION                                │
│ Tool: PyMuPDF (fitz)                                         │
│ Output: pdpl_raw_text.txt (Vietnamese UTF-8)                │
│ Quality: Diacritics preserved, layout maintained            │
└─────────────────────────────────────────────────────────────┘
         |
         v
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: STRUCTURE PARSING                                  │
│ Tool: Custom Python parser with regex                       │
│ Output: pdpl_structured.json                                │
│ Structure: Chapters > Articles > Clauses > Points           │
└─────────────────────────────────────────────────────────────┘
         |
         v
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: CATEGORY MAPPING (8 PDPL Principles)              │
│ Tool: Manual mapping + AI-assisted validation               │
│ Output: pdpl_category_mapped.json                           │
│ Categories: 0-7 (Lawfulness, Purpose, Minimization, etc.)  │
└─────────────────────────────────────────────────────────────┘
         |
         v
┌─────────────────────────────────────────────────────────────┐
│ STAGE 4: PHASE-SPECIFIC DATASET GENERATION                 │
│ Outputs (parallel):                                         │
│ - Phase 0: pdpl_phase0_principles.jsonl                    │
│ - Phase 1: pdpl_phase1_principles_enhanced.jsonl           │
│ - Phase 2A: pdpl_phase2a_breach_triage.jsonl               │
│ - Phase 2B: pdpl_phase2b_policy_requirements.jsonl         │
│ - Phase 3A: pdpl_phase3a_legal_qa.jsonl                    │
│ - Phase 3B: pdpl_phase3b_risk_scoring.jsonl                │
│ - Phase 3C: pdpl_phase3c_mps_reporting.jsonl               │
└─────────────────────────────────────────────────────────────┘
         |
         v
┌─────────────────────────────────────────────────────────────┐
│ STAGE 5: HYBRID TRAINING DATA CREATION                     │
│ Merge: Official PDPL + Synthetic Data                       │
│ Strategy: Weighted sampling (2:1 official:synthetic)        │
│ Validation: Data leakage detection, quality checks          │
└─────────────────────────────────────────────────────────────┘
         |
         v
┌─────────────────────────────────────────────────────────────┐
│ STAGE 6: QUALITY VALIDATION & LEGAL REVIEW                 │
│ - Vietnamese language quality check                          │
│ - Legal expert review (10% sample)                          │
│ - Cross-reference with existing synthetic data              │
│ - Contradiction detection and resolution                    │
└─────────────────────────────────────────────────────────────┘
         |
         v
[OUTPUT: Training-Ready Hybrid Datasets for All Phases]
```

---

## Stage 1: PDF Text Extraction

### **Objective**
Extract all Vietnamese text from PDPL 91/2025/QH15 PDF while preserving:
- Vietnamese diacritical marks (ă, â, đ, ê, ô, ơ, ư, á, à, ả, ã, ạ, etc.)
- Document structure (page numbers, headings, paragraphs)
- Special characters (legal symbols, numbering)

### **Technical Approach**

**Tool Selection: PyMuPDF (fitz)**
- Best Unicode support for Vietnamese
- Fast extraction (200-300 pages in <10 seconds)
- Layout preservation
- Metadata extraction

**Implementation Script**: `extract_pdpl_text.py`

```python
import fitz  # PyMuPDF
import json
from pathlib import Path
from datetime import datetime

class PDPLTextExtractor:
    """Extract Vietnamese text from PDPL 91/2025/QH15 PDF"""
    
    def __init__(self, pdf_path: str, output_dir: str):
        self.pdf_path = Path(pdf_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_full_text(self) -> dict:
        """Extract all text with metadata"""
        pdf_document = fitz.open(self.pdf_path)
        
        extraction_result = {
            "metadata": {
                "source_file": self.pdf_path.name,
                "extraction_date": datetime.now().isoformat(),
                "total_pages": len(pdf_document),
                "pdf_metadata": pdf_document.metadata
            },
            "pages": []
        }
        
        print(f"[OK] Extracting from {len(pdf_document)} pages...")
        
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text = page.get_text("text", sort=True)  # Sort for reading order
            
            page_data = {
                "page_number": page_num + 1,
                "text": text,
                "char_count": len(text),
                "has_vietnamese": self._detect_vietnamese(text)
            }
            
            extraction_result["pages"].append(page_data)
            
            if (page_num + 1) % 50 == 0:
                print(f"  > Processed {page_num + 1}/{len(pdf_document)} pages")
        
        pdf_document.close()
        
        print(f"[OK] Extraction complete: {len(extraction_result['pages'])} pages")
        return extraction_result
    
    def _detect_vietnamese(self, text: str) -> bool:
        """Check if text contains Vietnamese characters"""
        vietnamese_chars = set('ăâđêôơưáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệ'
                               'íìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữự'
                               'ýỳỷỹỵ')
        return any(char.lower() in vietnamese_chars for char in text)
    
    def save_raw_text(self, extraction_result: dict):
        """Save as plain text file"""
        output_path = self.output_dir / "pdpl_raw_text.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# PDPL 91/2025/QH15 - Raw Text Extraction\n")
            f.write(f"# Extracted: {extraction_result['metadata']['extraction_date']}\n")
            f.write(f"# Total Pages: {extraction_result['metadata']['total_pages']}\n\n")
            
            for page in extraction_result['pages']:
                f.write(f"\n{'='*80}\n")
                f.write(f"PAGE {page['page_number']}\n")
                f.write(f"{'='*80}\n\n")
                f.write(page['text'])
        
        print(f"[OK] Raw text saved to: {output_path}")
    
    def save_structured_json(self, extraction_result: dict):
        """Save as structured JSON"""
        output_path = self.output_dir / "pdpl_raw_extraction.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(extraction_result, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] Structured JSON saved to: {output_path}")
    
    def generate_statistics(self, extraction_result: dict):
        """Generate extraction statistics"""
        total_chars = sum(page['char_count'] for page in extraction_result['pages'])
        vietnamese_pages = sum(1 for page in extraction_result['pages'] 
                              if page['has_vietnamese'])
        
        stats = {
            "total_pages": len(extraction_result['pages']),
            "total_characters": total_chars,
            "vietnamese_pages": vietnamese_pages,
            "avg_chars_per_page": total_chars / len(extraction_result['pages']),
            "vietnamese_coverage": vietnamese_pages / len(extraction_result['pages']) * 100
        }
        
        print("\n[STATISTICS]")
        print(f"  Total Pages: {stats['total_pages']}")
        print(f"  Total Characters: {stats['total_characters']:,}")
        print(f"  Vietnamese Pages: {stats['vietnamese_pages']} ({stats['vietnamese_coverage']:.1f}%)")
        print(f"  Avg Chars/Page: {stats['avg_chars_per_page']:.0f}")
        
        return stats

# Usage
if __name__ == "__main__":
    extractor = PDPLTextExtractor(
        pdf_path="data/PDPL_91_2025_QH15.pdf",
        output_dir="data/pdpl_extraction"
    )
    
    # Extract
    result = extractor.extract_full_text()
    
    # Save outputs
    extractor.save_raw_text(result)
    extractor.save_structured_json(result)
    
    # Statistics
    stats = extractor.generate_statistics(result)
```

### **Deliverables**
- [x] `pdpl_raw_text.txt` - Plain text for human review
- [x] `pdpl_raw_extraction.json` - Structured JSON with metadata
- [x] `extraction_statistics.json` - Quality metrics

### **Quality Checks**
- [ ] Vietnamese diacritics preserved (sample 50 random paragraphs)
- [ ] Page numbers sequential (no missing pages)
- [ ] Special characters intact (legal numbering: 1., a), i., etc.)
- [ ] Total character count reasonable (expect 500K-1M characters)

### **Timeline**: 2 days

---

## Stage 2: Structure Parsing

### **Objective**
Parse flat Vietnamese text into hierarchical legal document structure:
- **Chapters** (Chương): 10-15 chapters
- **Articles** (Điều): 50-100 articles
- **Clauses** (Khoản): 200-400 clauses
- **Points** (Điểm): 500-1000 points

### **Vietnamese Legal Document Patterns**

```
Chương I: TÊN CHƯƠNG
  Điều 1. Tên điều
    1. Khoản 1 text...
    2. Khoản 2 text...
       a) Điểm a text...
       b) Điểm b text...
  Điều 2. Tên điều
    ...
```

### **Implementation Script**: `parse_pdpl_structure.py`

```python
import re
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

@dataclass
class Point:
    """Điểm (Point) - smallest unit"""
    point_id: str  # "a", "b", "c", etc.
    text: str
    parent_clause: Optional[str] = None

@dataclass
class Clause:
    """Khoản (Clause)"""
    clause_number: int
    text: str
    points: List[Point]
    parent_article: Optional[int] = None

@dataclass
class Article:
    """Điều (Article)"""
    article_number: int
    title: str
    clauses: List[Clause]
    parent_chapter: Optional[int] = None
    full_text: str = ""

@dataclass
class Chapter:
    """Chương (Chapter)"""
    chapter_number: int
    title: str
    articles: List[Article]

class PDPLStructureParser:
    """Parse Vietnamese PDPL document structure"""
    
    # Regex patterns for Vietnamese legal document structure
    CHAPTER_PATTERN = r'Chương\s+([IVXLCDM]+)[:\.]?\s*(.+?)(?=\n|$)'
    ARTICLE_PATTERN = r'Điều\s+(\d+)[:\.]?\s*(.+?)(?=\n|$)'
    CLAUSE_PATTERN = r'^\s*(\d+)\.\s+(.+?)(?=\n|$)'
    POINT_PATTERN = r'^\s*([a-z])\)\s+(.+?)(?=\n|$)'
    
    def __init__(self, raw_text_path: str):
        with open(raw_text_path, 'r', encoding='utf-8') as f:
            self.raw_text = f.read()
        
        self.chapters: List[Chapter] = []
    
    def parse_full_structure(self) -> List[Chapter]:
        """Parse entire document structure"""
        print("[OK] Starting structure parsing...")
        
        # Split by chapters
        chapter_splits = re.split(self.CHAPTER_PATTERN, self.raw_text, flags=re.MULTILINE)
        
        current_chapter = None
        
        for i in range(1, len(chapter_splits), 3):
            chapter_num_roman = chapter_splits[i]
            chapter_title = chapter_splits[i+1].strip()
            chapter_content = chapter_splits[i+2] if i+2 < len(chapter_splits) else ""
            
            chapter_num = self._roman_to_int(chapter_num_roman)
            
            print(f"  > Parsing Chapter {chapter_num}: {chapter_title[:50]}...")
            
            # Parse articles within chapter
            articles = self._parse_articles(chapter_content, chapter_num)
            
            chapter = Chapter(
                chapter_number=chapter_num,
                title=chapter_title,
                articles=articles
            )
            
            self.chapters.append(chapter)
        
        print(f"[OK] Parsed {len(self.chapters)} chapters")
        return self.chapters
    
    def _parse_articles(self, chapter_text: str, chapter_num: int) -> List[Article]:
        """Parse articles within a chapter"""
        articles = []
        article_splits = re.split(self.ARTICLE_PATTERN, chapter_text, flags=re.MULTILINE)
        
        for i in range(1, len(article_splits), 3):
            article_num = int(article_splits[i])
            article_title = article_splits[i+1].strip()
            article_content = article_splits[i+2] if i+2 < len(article_splits) else ""
            
            # Parse clauses within article
            clauses = self._parse_clauses(article_content, article_num)
            
            article = Article(
                article_number=article_num,
                title=article_title,
                clauses=clauses,
                parent_chapter=chapter_num,
                full_text=article_content.strip()
            )
            
            articles.append(article)
        
        return articles
    
    def _parse_clauses(self, article_text: str, article_num: int) -> List[Clause]:
        """Parse clauses within an article"""
        clauses = []
        lines = article_text.split('\n')
        
        current_clause = None
        current_clause_text = []
        current_points = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if new clause
            clause_match = re.match(self.CLAUSE_PATTERN, line)
            if clause_match:
                # Save previous clause
                if current_clause is not None:
                    clauses.append(Clause(
                        clause_number=current_clause,
                        text=' '.join(current_clause_text),
                        points=current_points,
                        parent_article=article_num
                    ))
                
                # Start new clause
                current_clause = int(clause_match.group(1))
                current_clause_text = [clause_match.group(2)]
                current_points = []
                continue
            
            # Check if point
            point_match = re.match(self.POINT_PATTERN, line)
            if point_match:
                point = Point(
                    point_id=point_match.group(1),
                    text=point_match.group(2),
                    parent_clause=f"{article_num}.{current_clause}"
                )
                current_points.append(point)
                continue
            
            # Continuation of current clause
            if current_clause is not None:
                current_clause_text.append(line)
        
        # Save last clause
        if current_clause is not None:
            clauses.append(Clause(
                clause_number=current_clause,
                text=' '.join(current_clause_text),
                points=current_points,
                parent_article=article_num
            ))
        
        return clauses
    
    def _roman_to_int(self, roman: str) -> int:
        """Convert Roman numerals to integer"""
        roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        prev_value = 0
        
        for char in reversed(roman.upper()):
            value = roman_values.get(char, 0)
            if value < prev_value:
                result -= value
            else:
                result += value
            prev_value = value
        
        return result
    
    def save_structured_json(self, output_path: str):
        """Save parsed structure as JSON"""
        output_data = {
            "total_chapters": len(self.chapters),
            "chapters": []
        }
        
        for chapter in self.chapters:
            chapter_dict = {
                "chapter_number": chapter.chapter_number,
                "title": chapter.title,
                "total_articles": len(chapter.articles),
                "articles": []
            }
            
            for article in chapter.articles:
                article_dict = {
                    "article_number": article.article_number,
                    "title": article.title,
                    "parent_chapter": article.parent_chapter,
                    "total_clauses": len(article.clauses),
                    "clauses": []
                }
                
                for clause in article.clauses:
                    clause_dict = {
                        "clause_number": clause.clause_number,
                        "text": clause.text,
                        "points": [asdict(p) for p in clause.points]
                    }
                    article_dict["clauses"].append(clause_dict)
                
                chapter_dict["articles"].append(article_dict)
            
            output_data["chapters"].append(chapter_dict)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] Structured JSON saved to: {output_path}")
    
    def generate_statistics(self):
        """Generate parsing statistics"""
        total_articles = sum(len(ch.articles) for ch in self.chapters)
        total_clauses = sum(len(a.clauses) for ch in self.chapters for a in ch.articles)
        total_points = sum(len(c.points) for ch in self.chapters 
                          for a in ch.articles for c in a.clauses)
        
        print("\n[PARSING STATISTICS]")
        print(f"  Total Chapters: {len(self.chapters)}")
        print(f"  Total Articles: {total_articles}")
        print(f"  Total Clauses: {total_clauses}")
        print(f"  Total Points: {total_points}")
        
        return {
            "chapters": len(self.chapters),
            "articles": total_articles,
            "clauses": total_clauses,
            "points": total_points
        }

# Usage
if __name__ == "__main__":
    parser = PDPLStructureParser("data/pdpl_extraction/pdpl_raw_text.txt")
    
    # Parse structure
    chapters = parser.parse_full_structure()
    
    # Save structured JSON
    parser.save_structured_json("data/pdpl_extraction/pdpl_structured.json")
    
    # Statistics
    stats = parser.generate_statistics()
```

### **Deliverables**
- [x] `pdpl_structured.json` - Hierarchical structure
- [x] `parsing_statistics.json` - Structure metrics

### **Quality Checks**
- [ ] All chapters extracted (expect 10-15)
- [ ] All articles numbered sequentially
- [ ] Key articles present (Article 13 for legal basis)
- [ ] Vietnamese text intact in all levels

### **Timeline**: 3-4 days (includes regex testing and validation)

---

## Stage 3: Category Mapping

### **Objective**
Map each article/clause to the 8 PDPL principle categories used in VeriAIDPO training:

```
Category 0: Lawfulness (Tính hợp pháp)
Category 1: Purpose Limitation (Giới hạn mục đích)
Category 2: Data Minimization (Giảm thiểu dữ liệu)
Category 3: Accuracy (Chính xác)
Category 4: Storage Limitation (Giới hạn lưu trữ)
Category 5: Security (An toàn bảo mật)
Category 6: Transparency (Minh bạch)
Category 7: Consent (Đồng ý)
```

### **Mapping Strategy**

**Phase 1: Manual Expert Mapping**
- Vietnamese legal expert reads each article
- Maps to primary category (0-7)
- Identifies secondary categories (if applicable)
- Notes key phrases for training

**Phase 2: AI-Assisted Validation**
- Run existing VeriAIDPO model on articles
- Compare AI predictions with expert mapping
- Flag discrepancies for review
- Build confidence in both mapping and model

### **Implementation Script**: `map_pdpl_categories.py`

```python
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class CategoryMapping:
    """Category assignment for PDPL content"""
    article_number: int
    article_title: str
    clause_number: Optional[int] = None
    primary_category: int = -1  # 0-7
    secondary_categories: List[int] = None
    confidence: str = "MANUAL"  # MANUAL, AI_ASSISTED, VALIDATED
    key_phrases: List[str] = None
    notes: str = ""
    
    def __post_init__(self):
        if self.secondary_categories is None:
            self.secondary_categories = []
        if self.key_phrases is None:
            self.key_phrases = []

class PDPLCategoryMapper:
    """Map PDPL articles to 8 principle categories"""
    
    CATEGORY_NAMES = {
        0: {"vi": "Tính hợp pháp", "en": "Lawfulness"},
        1: {"vi": "Giới hạn mục đích", "en": "Purpose Limitation"},
        2: {"vi": "Giảm thiểu dữ liệu", "en": "Data Minimization"},
        3: {"vi": "Chính xác", "en": "Accuracy"},
        4: {"vi": "Giới hạn lưu trữ", "en": "Storage Limitation"},
        5: {"vi": "An toàn bảo mật", "en": "Security"},
        6: {"vi": "Minh bạch", "en": "Transparency"},
        7: {"vi": "Đồng ý", "en": "Consent"}
    }
    
    # Pre-defined mappings for known articles (from PDPL analysis)
    KNOWN_MAPPINGS = {
        13: {  # Article 13: Legal basis
            "primary": 0,
            "secondary": [],
            "key_phrases": ["cơ sở pháp lý", "legal basis", "Điều 13"]
        },
        7: {  # Article 7: Processing principles
            "clauses": {
                1: {"primary": 6, "key": "minh bạch"},  # Transparency
                2: {"primary": 1, "key": "mục đích"},  # Purpose Limitation
                3: {"primary": 2, "key": "tối thiểu"},  # Data Minimization
                4: {"primary": 3, "key": "chính xác"},  # Accuracy
                5: {"primary": 4, "key": "lưu trữ"},  # Storage Limitation
                6: {"primary": 5, "key": "bảo mật"}  # Security
            }
        }
    }
    
    def __init__(self, structured_json_path: str):
        with open(structured_json_path, 'r', encoding='utf-8') as f:
            self.pdpl_structure = json.load(f)
        
        self.mappings: List[CategoryMapping] = []
    
    def create_mapping_template(self, output_path: str):
        """Create template for manual mapping"""
        template = {
            "instructions": {
                "en": "Map each article to primary category (0-7). Add secondary categories if applicable.",
                "vi": "Phân loại mỗi điều vào danh mục chính (0-7). Thêm danh mục phụ nếu có."
            },
            "categories": self.CATEGORY_NAMES,
            "articles": []
        }
        
        for chapter in self.pdpl_structure["chapters"]:
            for article in chapter["articles"]:
                article_template = {
                    "article_number": article["article_number"],
                    "article_title": article["title"],
                    "chapter": chapter["chapter_number"],
                    "primary_category": -1,  # TO BE FILLED
                    "secondary_categories": [],
                    "key_phrases": [],
                    "notes": "",
                    "full_text_preview": article["clauses"][0]["text"][:200] if article["clauses"] else ""
                }
                template["articles"].append(article_template)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] Mapping template created: {output_path}")
        print(f"  > {len(template['articles'])} articles to map")
    
    def load_manual_mappings(self, mapping_file: str):
        """Load completed manual mappings"""
        with open(mapping_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for article_data in data["articles"]:
            if article_data["primary_category"] == -1:
                print(f"[WARNING] Article {article_data['article_number']} not mapped yet")
                continue
            
            mapping = CategoryMapping(
                article_number=article_data["article_number"],
                article_title=article_data["article_title"],
                primary_category=article_data["primary_category"],
                secondary_categories=article_data.get("secondary_categories", []),
                key_phrases=article_data.get("key_phrases", []),
                notes=article_data.get("notes", ""),
                confidence="MANUAL"
            )
            
            self.mappings.append(mapping)
        
        print(f"[OK] Loaded {len(self.mappings)} manual mappings")
    
    def validate_with_ai(self, ai_classify_func):
        """Validate manual mappings with AI model"""
        print("[OK] Validating mappings with AI model...")
        
        agreements = 0
        disagreements = []
        
        for mapping in self.mappings:
            # Get article text
            article_text = self._get_article_text(mapping.article_number)
            
            # AI classification
            ai_result = ai_classify_func(article_text)
            ai_category = ai_result["category_id"]
            
            if ai_category == mapping.primary_category:
                agreements += 1
                mapping.confidence = "VALIDATED"
            else:
                disagreements.append({
                    "article": mapping.article_number,
                    "manual": mapping.primary_category,
                    "ai": ai_category,
                    "ai_confidence": ai_result["confidence"]
                })
        
        agreement_rate = agreements / len(self.mappings) * 100
        
        print(f"\n[VALIDATION RESULTS]")
        print(f"  Agreement: {agreements}/{len(self.mappings)} ({agreement_rate:.1f}%)")
        print(f"  Disagreements: {len(disagreements)}")
        
        if disagreements:
            print("\n[DISAGREEMENTS TO REVIEW]")
            for d in disagreements[:10]:  # Show first 10
                print(f"  Article {d['article']}: Manual={d['manual']}, AI={d['ai']} ({d['ai_confidence']:.0%})")
        
        return agreement_rate, disagreements
    
    def _get_article_text(self, article_number: int) -> str:
        """Get full text of an article"""
        for chapter in self.pdpl_structure["chapters"]:
            for article in chapter["articles"]:
                if article["article_number"] == article_number:
                    # Combine all clause texts
                    texts = [clause["text"] for clause in article["clauses"]]
                    return article["title"] + " " + " ".join(texts)
        return ""
    
    def save_category_mappings(self, output_path: str):
        """Save final category mappings"""
        output_data = {
            "total_mappings": len(self.mappings),
            "category_distribution": self._calculate_distribution(),
            "mappings": [asdict(m) for m in self.mappings]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] Category mappings saved: {output_path}")
    
    def _calculate_distribution(self) -> Dict[int, int]:
        """Calculate category distribution"""
        distribution = {i: 0 for i in range(8)}
        for mapping in self.mappings:
            distribution[mapping.primary_category] += 1
        return distribution

# Usage
if __name__ == "__main__":
    mapper = PDPLCategoryMapper("data/pdpl_extraction/pdpl_structured.json")
    
    # Step 1: Create mapping template for legal expert
    mapper.create_mapping_template("data/pdpl_extraction/pdpl_mapping_template.json")
    
    print("\n[NEXT STEP]")
    print("  1. Legal expert fills in pdpl_mapping_template.json")
    print("  2. Run validation with AI model")
    print("  3. Review disagreements")
    print("  4. Finalize mappings")
```

### **Deliverables**
- [x] `pdpl_mapping_template.json` - Template for expert
- [x] `pdpl_category_mapped.json` - Final mappings
- [x] `mapping_validation_report.json` - AI validation results

### **Quality Checks**
- [ ] All 8 categories represented
- [ ] Article 13 correctly mapped to Category 0 (Lawfulness)
- [ ] AI validation agreement >80%
- [ ] Legal expert review complete

### **Timeline**: 5-7 days (includes expert mapping time)

---

## Implementation Timeline

### **Week 1: Infrastructure Setup**
- Day 1-2: Stage 1 (PDF extraction)
- Day 3-4: Stage 2 (Structure parsing)
- Day 5: Testing and validation

### **Week 2: Category Mapping**
- Day 1-2: Create mapping templates
- Day 3-5: Legal expert mapping
- Day 6-7: AI validation and review

### **Week 3: Dataset Generation**
- Day 1-2: Phase 0 dataset generation
- Day 3-4: Phase 1 dataset generation
- Day 5: Phase 2-3 dataset generation

### **Week 4: Quality Validation & Integration**
- Day 1-2: Quality checks and legal review
- Day 3-4: Integration with synthetic data
- Day 5: Final validation and documentation

---

## Success Metrics

### **Extraction Quality**
- [x] 100% page coverage
- [x] 100% Vietnamese character preservation
- [x] <1% parsing errors

### **Mapping Quality**
- [x] All articles mapped to categories
- [x] >80% AI-human agreement
- [x] 100% legal expert review

### **Training Data Quality**
- [x] 1,500-2,000 official PDPL samples
- [x] Zero contradictions with synthetic data
- [x] Balanced category distribution

---

## Next Steps

After completing this master plan, implement phase-specific plans:

1. **Phase 0 Plan**: `01_Phase0_Principles_PDPL_Integration.md`
2. **Phase 1 Plan**: `02_Phase1_Principles_Enhanced_PDPL.md`
3. **Phase 2A Plan**: `03_Phase2A_BreachTriage_PDPL.md`
4. **Phase 2B Plan**: `04_Phase2B_PolicyGen_PDPL.md`
5. **Phase 3A Plan**: `05_Phase3A_LegalQA_PDPL.md`
6. **Phase 3B Plan**: `06_Phase3B_RiskScoring_PDPL.md`
7. **Phase 3C Plan**: `07_Phase3C_MPS_Reporting_PDPL.md`

---

**Document Status**: Master Plan v1.0  
**Last Updated**: October 21, 2025  
**Owner**: VeriSyntra AI Team
