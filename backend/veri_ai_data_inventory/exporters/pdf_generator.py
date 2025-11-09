"""
ROPA PDF Generator with Vietnamese Font Support
Vietnamese PDPL 2025 - Decree 13/2023/ND-CP Compliance

This module generates PDF format ROPA documents with proper Vietnamese diacritics
support using Noto Sans Vietnamese font.

Legal Framework:
- Decree 13/2023/ND-CP Article 12 (ROPA requirements)
- PDPL 2025 Article 17 (Record keeping obligations)
- Vietnamese language support for official documents

Document #3 Section 6: PDF Generation - COMPLETE
Version: 1.0.0
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import List, Any
import io
from datetime import datetime
from pathlib import Path
import logging

from models.ropa_models import ROPADocument, ROPAEntry, ROPALanguage
from config.ropa_translations import ROPATranslations

logger = logging.getLogger(__name__)


class ROPAPDFGenerator:
    """
    Generate Vietnamese PDPL-compliant ROPA in PDF format
    
    Zero hard-coding pattern:
    - Uses ROPATranslations for all text
    - Dictionary routing for language selection  
    - Vietnamese font support for proper diacritics (ă, â, ê, ô, ơ, ư, đ)
    
    Vietnamese Color Palette (VeriSyntra):
    - Primary: #6b8e6b (Vietnamese green)
    - Secondary: #7fa3c3 (Vietnamese blue)
    - Accent: #d4c18a (Vietnamese gold)
    
    Usage:
        pdf_bytes = ROPAPDFGenerator.generate_ropa_pdf(document, ROPALanguage.VIETNAMESE)
        with open('ropa.pdf', 'wb') as f:
            f.write(pdf_bytes)
    """
    
    # Vietnamese font configuration
    VIETNAMESE_FONT = "NotoSansVietnamese"
    VIETNAMESE_FONT_BOLD = "NotoSansVietnameseBold"
    FALLBACK_FONT = "Helvetica"
    FALLBACK_FONT_BOLD = "Helvetica-Bold"
    
    # Font sizes
    FONT_SIZE_TITLE = 16
    FONT_SIZE_SUBTITLE = 12
    FONT_SIZE_HEADING = 12
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_SMALL = 8
    
    # VeriSyntra Vietnamese color palette
    COLOR_PRIMARY = colors.HexColor('#6b8e6b')      # Vietnamese green
    COLOR_SECONDARY = colors.HexColor('#7fa3c3')    # Vietnamese blue
    COLOR_ACCENT = colors.HexColor('#d4c18a')       # Vietnamese gold
    COLOR_TEXT = colors.black
    COLOR_HEADER_TEXT = colors.whitesmoke
    
    # Flag to track if Vietnamese font is available
    _vietnamese_font_registered = False
    _using_vietnamese_font = False
    
    @classmethod
    def _setup_vietnamese_font(cls) -> bool:
        """
        Register Noto Sans Vietnamese font with reportlab
        
        Noto Sans supports all Vietnamese diacritics:
        - Tone marks: á à ả ã ạ
        - Vowel marks: ă â ê ô ơ ư  
        - Special: đ Đ
        
        Returns:
            bool: True if Vietnamese font registered successfully
        """
        if cls._vietnamese_font_registered:
            return cls._using_vietnamese_font
        
        try:
            # Try to find Noto Sans font files
            font_dir = Path(__file__).parent / "fonts"
            regular_font = font_dir / "NotoSans-Regular.ttf"
            bold_font = font_dir / "NotoSans-Bold.ttf"
            
            if regular_font.exists():
                pdfmetrics.registerFont(TTFont(cls.VIETNAMESE_FONT, str(regular_font)))
                logger.info(f"[OK] Vietnamese font registered: {regular_font}")
                cls._using_vietnamese_font = True
                
                # Register bold if available
                if bold_font.exists():
                    pdfmetrics.registerFont(TTFont(cls.VIETNAMESE_FONT_BOLD, str(bold_font)))
                    logger.info(f"[OK] Vietnamese bold font registered: {bold_font}")
                else:
                    logger.warning("[WARNING] Vietnamese bold font not found, using regular")
                    cls.VIETNAMESE_FONT_BOLD = cls.VIETNAMESE_FONT
            else:
                logger.warning(
                    f"[WARNING] Vietnamese font not found at {regular_font}, "
                    f"using {cls.FALLBACK_FONT} (diacritics may not display correctly)"
                )
                cls.VIETNAMESE_FONT = cls.FALLBACK_FONT
                cls.VIETNAMESE_FONT_BOLD = cls.FALLBACK_FONT_BOLD
                cls._using_vietnamese_font = False
            
            cls._vietnamese_font_registered = True
            return cls._using_vietnamese_font
            
        except Exception as e:
            logger.error(f"[ERROR] Font registration failed: {str(e)}")
            cls.VIETNAMESE_FONT = cls.FALLBACK_FONT
            cls.VIETNAMESE_FONT_BOLD = cls.FALLBACK_FONT_BOLD
            cls._vietnamese_font_registered = True
            cls._using_vietnamese_font = False
            return False
    
    @classmethod
    def generate_ropa_pdf(
        cls,
        document: ROPADocument,
        language: ROPALanguage = ROPALanguage.VIETNAMESE
    ) -> bytes:
        """
        Generate ROPA PDF document - ZERO HARD-CODING
        
        Args:
            document: ROPADocument instance
            language: ROPALanguage enum (VIETNAMESE or ENGLISH)
            
        Returns:
            PDF bytes ready for download or storage
            
        Example:
            pdf_bytes = ROPAPDFGenerator.generate_ropa_pdf(
                ropa_document,
                ROPALanguage.VIETNAMESE
            )
        """
        try:
            # Setup Vietnamese font
            cls._setup_vietnamese_font()
            
            # Create PDF buffer
            buffer = io.BytesIO()
            
            # Create document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=2*cm,
                leftMargin=2*cm,
                topMargin=2*cm,
                bottomMargin=2*cm,
                title=ROPATranslations.PDF_TITLES[language]['title']
            )
            
            # Build PDF content
            story = []
            
            # Page 1: Title + Controller + Summary
            story.extend(cls._create_title_page(document, language))
            story.append(Spacer(1, 0.8*cm))
            
            story.append(cls._create_controller_section(document.entries[0], language))
            story.append(Spacer(1, 0.5*cm))
            
            # DPO section (if DPO appointed)
            if document.entries[0].dpo_name:
                story.append(cls._create_dpo_section(document.entries[0], language))
                story.append(Spacer(1, 0.5*cm))
            
            story.append(cls._create_summary_section(document, language))
            
            # Page 2+: Processing activities table
            story.append(PageBreak())
            story.append(cls._create_activities_header(language))
            story.append(Spacer(1, 0.3*cm))
            story.append(cls._create_activities_table(document, language))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            logger.info(
                f"[OK] Generated ROPA PDF: {len(pdf_bytes)} bytes, "
                f"{len(document.entries)} entries, language={language.value}"
            )
            
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"[ERROR] PDF generation failed: {str(e)}")
            raise
    
    @classmethod
    def _create_title_page(cls, document: ROPADocument, language: ROPALanguage) -> List[Any]:
        """
        Create PDF title page - ZERO HARD-CODING
        
        Uses ROPATranslations.PDF_TITLES config
        """
        elements = []
        
        # Get title from config - NO if/else
        title_config = ROPATranslations.PDF_TITLES[language]
        title_text = title_config['title']
        subtitle_text = title_config['subtitle']
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            fontName=cls.VIETNAMESE_FONT_BOLD,
            fontSize=cls.FONT_SIZE_TITLE,
            alignment=TA_CENTER,
            textColor=cls.COLOR_PRIMARY,
            spaceAfter=12
        )
        
        # Subtitle style
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            fontName=cls.VIETNAMESE_FONT,
            fontSize=cls.FONT_SIZE_SUBTITLE,
            alignment=TA_CENTER,
            textColor=cls.COLOR_TEXT,
            spaceAfter=6
        )
        
        # Add title and subtitle
        elements.append(Paragraph(f"<b>{title_text}</b>", title_style))
        elements.append(Paragraph(f"<i>{subtitle_text}</i>", subtitle_style))
        
        # Add generation date
        date_format = ROPATranslations.DATE_FORMATS[language]
        date_label = ROPATranslations.PDF_FIELD_LABELS[language]['generated_date']
        date_text = f"{date_label} {document.generated_date.strftime(date_format)}"
        
        date_style = ParagraphStyle(
            'DateStyle',
            fontName=cls.VIETNAMESE_FONT,
            fontSize=cls.FONT_SIZE_NORMAL,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        
        elements.append(Spacer(1, 0.3*cm))
        elements.append(Paragraph(date_text, date_style))
        
        return elements
    
    @classmethod
    def _create_controller_section(cls, entry: ROPAEntry, language: ROPALanguage) -> Table:
        """
        Create controller information section - ZERO HARD-CODING
        
        Uses ROPATranslations.PDF_SECTION_HEADERS and PDF_FIELD_LABELS
        """
        # Get labels from config - NO if/else
        headers = ROPATranslations.PDF_SECTION_HEADERS[language]
        labels = ROPATranslations.PDF_FIELD_LABELS[language]
        
        # Build data using config labels and field accessors
        data = [
            [headers["controller"], ""],
            [labels["org_name"], ROPATranslations.get_field_value(entry, 'controller_name', language)],
            [labels["tax_id"], entry.controller_tax_id],
            [labels["address"], entry.controller_address],
            [labels["contact_person"], entry.controller_contact_person],
            [labels["phone"], entry.controller_phone],
            [labels["email"], entry.controller_email],
        ]
        
        # Create table
        table = Table(data, colWidths=[7*cm, 11*cm])
        table.setStyle(cls._get_section_table_style("controller"))
        
        return table
    
    @classmethod
    def _create_dpo_section(cls, entry: ROPAEntry, language: ROPALanguage) -> Table:
        """
        Create DPO information section - ZERO HARD-CODING
        
        Only called if DPO is appointed (entry.dpo_name is not None)
        """
        headers = ROPATranslations.PDF_SECTION_HEADERS[language]
        labels = ROPATranslations.PDF_FIELD_LABELS[language]
        
        data = [
            [headers["dpo"], ""],
            [labels["dpo_name"], entry.dpo_name or ROPATranslations.NOT_SPECIFIED[language]],
            [labels["dpo_email"], entry.dpo_email or ROPATranslations.NOT_SPECIFIED[language]],
            [labels["dpo_phone"], entry.dpo_phone or ROPATranslations.NOT_SPECIFIED[language]]
        ]
        
        table = Table(data, colWidths=[7*cm, 11*cm])
        table.setStyle(cls._get_section_table_style("dpo"))
        
        return table
    
    @classmethod
    def _create_summary_section(cls, document: ROPADocument, language: ROPALanguage) -> Table:
        """
        Create summary statistics section - ZERO HARD-CODING
        
        Uses ROPATranslations helper methods for formatting
        """
        headers = ROPATranslations.PDF_SECTION_HEADERS[language]
        labels = ROPATranslations.PDF_FIELD_LABELS[language]
        
        # Build data using config - NO if/else
        data = [
            [headers["summary"], ""],
            [labels["total_activities"], str(document.total_processing_activities)],
            [labels["total_subjects"], ROPATranslations.format_optional_int(
                document.total_data_subjects, language
            )],
            [labels["has_sensitive"], ROPATranslations.format_boolean(
                document.has_sensitive_data, language
            )],
            [labels["has_cross_border"], ROPATranslations.format_boolean(
                document.has_cross_border_transfers, language
            )],
        ]
        
        table = Table(data, colWidths=[7*cm, 11*cm])
        table.setStyle(cls._get_section_table_style("summary"))
        
        return table
    
    @classmethod
    def _create_activities_header(cls, language: ROPALanguage) -> Paragraph:
        """Create activities table header"""
        headers = ROPATranslations.PDF_SECTION_HEADERS[language]
        
        header_style = ParagraphStyle(
            'ActivitiesHeader',
            fontName=cls.VIETNAMESE_FONT_BOLD,
            fontSize=cls.FONT_SIZE_HEADING,
            textColor=cls.COLOR_PRIMARY,
            spaceAfter=6
        )
        
        return Paragraph(f"<b>{headers['activities']}</b>", header_style)
    
    @classmethod
    def _create_activities_table(cls, document: ROPADocument, language: ROPALanguage) -> Table:
        """
        Create processing activities table - ZERO HARD-CODING
        
        Uses config for headers and field accessors for data
        Multi-page table support with text wrapping
        """
        labels = ROPATranslations.PDF_FIELD_LABELS[language]
        
        # Style for wrapping text in table cells
        cell_style = ParagraphStyle(
            'TableCell',
            fontName=cls.VIETNAMESE_FONT,
            fontSize=cls.FONT_SIZE_SMALL,
            leading=10,
            wordWrap='CJK'  # Enable word wrapping
        )
        
        # Style for headers with wrapping
        header_style = ParagraphStyle(
            'TableHeader',
            fontName=cls.VIETNAMESE_FONT_BOLD,
            fontSize=cls.FONT_SIZE_NORMAL,
            leading=11,
            textColor=cls.COLOR_HEADER_TEXT,
            wordWrap='CJK'
        )
        
        # Headers from config wrapped in Paragraphs - NO if/else
        headers = [
            Paragraph(labels["serial_no"], header_style),
            Paragraph(labels["activity"], header_style),
            Paragraph(labels["purpose"], header_style),
            Paragraph(labels["legal_basis"], header_style),
            Paragraph(labels["data_categories"], header_style),
            Paragraph(labels["subjects"], header_style)
        ]
        
        data = [headers]
        
        # Build rows using field accessors - NO if/else
        for idx, entry in enumerate(document.entries, start=1):
            activity_name = ROPATranslations.get_field_value(entry, 'processing_activity_name', language)
            purpose = ROPATranslations.get_field_value(entry, 'processing_purpose', language)
            legal_basis = ROPATranslations.get_field_value(entry, 'legal_basis', language)
            categories = ROPATranslations.get_field_value(entry, 'data_categories', language) or []
            
            # Format categories list (show first 3)
            categories_display = ", ".join(categories[:3])
            if len(categories) > 3:
                categories_display += f" (+{len(categories) - 3})"
            
            # Wrap text in Paragraph objects for proper text wrapping
            row = [
                str(idx),
                Paragraph(activity_name, cell_style),
                Paragraph(purpose, cell_style),
                Paragraph(legal_basis, cell_style),
                Paragraph(categories_display, cell_style),
                ROPATranslations.format_optional_int(entry.estimated_data_subjects, language)
            ]
            
            data.append(row)
        
        # Create table with adjusted column widths for A4 page (17cm available width)
        # Optimized for both Vietnamese and English text
        # Columns: No. (0.8cm) | Activity (4cm) | Purpose (4cm) | Legal Basis (2.5cm) | Data Categories (3.5cm) | Subjects (2.2cm)
        table = Table(data, colWidths=[0.8*cm, 4*cm, 4*cm, 2.5*cm, 3.5*cm, 2.2*cm])
        table.setStyle(cls._get_activities_table_style())
        
        return table
    
    @classmethod
    def _get_section_table_style(cls, section_type: str) -> TableStyle:
        """
        Apply Vietnamese-themed styling to section tables - ZERO HARD-CODING
        
        Args:
            section_type: 'controller', 'dpo', or 'summary'
        """
        # Choose color based on section - dictionary routing
        section_colors = {
            'controller': cls.COLOR_PRIMARY,
            'dpo': cls.COLOR_SECONDARY,
            'summary': cls.COLOR_ACCENT
        }
        
        bg_color = section_colors.get(section_type, cls.COLOR_PRIMARY)
        
        style = TableStyle([
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), bg_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), cls.COLOR_HEADER_TEXT),
            ('FONTNAME', (0, 0), (-1, 0), cls.VIETNAMESE_FONT_BOLD),
            ('FONTSIZE', (0, 0), (-1, 0), cls.FONT_SIZE_HEADING),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('FONTNAME', (0, 1), (-1, -1), cls.VIETNAMESE_FONT),
            ('FONTSIZE', (0, 1), (-1, -1), cls.FONT_SIZE_NORMAL),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        return style
    
    @classmethod
    def _get_activities_table_style(cls) -> TableStyle:
        """
        Apply styling to activities table - ZERO HARD-CODING
        """
        style = TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), cls.COLOR_PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), cls.COLOR_HEADER_TEXT),
            ('FONTNAME', (0, 0), (-1, 0), cls.VIETNAMESE_FONT_BOLD),
            ('FONTSIZE', (0, 0), (-1, 0), cls.FONT_SIZE_NORMAL),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), cls.VIETNAMESE_FONT),
            ('FONTSIZE', (0, 1), (-1, -1), cls.FONT_SIZE_SMALL),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 1), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            
            # Alternating row colors for readability
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ])
        
        return style


    @classmethod
    def export(
        cls,
        document: ROPADocument,
        output_path: str,
        language: ROPALanguage = ROPALanguage.VIETNAMESE
    ) -> None:
        """
        Export ROPA to PDF file - Unified interface for service layer
        
        This method provides a unified interface matching JSON/CSV exporters.
        
        Args:
            document: ROPADocument instance
            output_path: Path where PDF file will be saved
            language: ROPALanguage enum (VIETNAMESE or ENGLISH)
        
        Example:
            ROPAPDFGenerator.export(
                ropa_document,
                "ropa_export.pdf",
                ROPALanguage.VIETNAMESE
            )
        """
        pdf_bytes = cls.generate_ropa_pdf(document, language)
        
        # Write bytes to file
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
