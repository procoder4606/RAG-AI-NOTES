"""
PDF Generator Module
Converts text notes to formatted PDF documents
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
from datetime import datetime

def generate_pdf_from_notes(notes_text, title="Video Notes"):
    """
    Generate a formatted PDF from notes text
    
    Args:
        notes_text (str): The notes content to convert to PDF
        title (str): Title for the PDF document
        
    Returns:
        bytes: PDF file as bytes
    """
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#1f77b4',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#333333',
        spaceAfter=12,
        spaceBefore=12
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=10
    )
    
    # Build content
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Process notes text
    lines = notes_text.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # Handle markdown-style headings
        if line.startswith('# '):
            # Main heading
            text = line[2:].strip()
            story.append(Paragraph(text, title_style))
        elif line.startswith('## '):
            # Subheading
            text = line[3:].strip()
            story.append(Paragraph(text, heading_style))
        elif line.startswith('### '):
            # Minor heading
            text = line[4:].strip()
            story.append(Paragraph(text, styles['Heading3']))
        else:
            # Regular text - escape special characters
            text = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(text, body_style))
    
    # Build PDF
    doc.build(story)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes

def save_pdf_to_file(notes_text, output_path, title="Video Notes"):
    """
    Save notes as PDF to a file
    
    Args:
        notes_text (str): The notes content
        output_path (str): Where to save the PDF
        title (str): Title for the PDF
    """
    pdf_bytes = generate_pdf_from_notes(notes_text, title)
    
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)
    
    print(f"PDF saved to: {output_path}")
