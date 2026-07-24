"""
Script to generate a sample multi-page PDF document for testing semantic search.
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def create_sample_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1e3c72'),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Heading3'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#6c757d'),
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2a5298'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#212529'),
        spaceAfter=10
    )

    story = []

    # Title
    story.append(Paragraph("Acme Corp - Employee Handbook & Corporate Policy", title_style))
    story.append(Paragraph("Standard Operating Procedures & Guidelines", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2a5298'), spaceAfter=15))

    # Section 1
    story.append(Paragraph("1. Work Culture & Office Hours", h2_style))
    story.append(Paragraph(
        "Standard working hours are from 9:00 AM to 5:00 PM EST, Monday through Friday. "
        "Employees are expected to maintain punctuality and professional decorum. "
        "Under our flexible work arrangement, full-time employees are eligible for remote work "
        "up to two days per week, subject to team lead approval.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # Section 2
    story.append(Paragraph("2. Customer Returns & Refund Policy", h2_style))
    story.append(Paragraph(
        "Customers may return any unused physical merchandise within 30 days of purchase for a 100% full refund "
        "to the original payment method, provided the original sales receipt is presented. "
        "Returns requested between 31 and 60 days after purchase are eligible for store credit only. "
        "Custom-engraved products, clearance items, and downloadable digital software are strictly non-refundable.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # Section 3
    story.append(Paragraph("3. Annual Leave & Time Off (PTO)", h2_style))
    story.append(Paragraph(
        "Full-time employees receive 20 days of paid annual leave per calendar year, accrued monthly. "
        "Additionally, employees are granted 10 paid sick leave days for medical appointments or personal illness. "
        "New parents are entitled to 12 weeks of fully paid parental leave following the birth, adoption, or foster placement of a child.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # Section 4
    story.append(Paragraph("4. IT Security & Cyber Hygiene Guidelines", h2_style))
    story.append(Paragraph(
        "Multi-Factor Authentication (MFA) must be enabled on all corporate email and VPN accounts. "
        "Employees are required to lock their computer screens (Win+L / Ctrl+Cmd+Q) whenever stepping away from their desk. "
        "Passwords must be at least 12 characters long and updated every 90 days. Sharing credentials with unauthorized personnel is prohibited.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # Section 5
    story.append(Paragraph("5. Business Travel & Expense Reimbursement", h2_style))
    story.append(Paragraph(
        "Employees traveling for official company business can claim a daily meal allowance of up to $50 per day. "
        "All business flights and hotel accommodations must be booked at least 14 days in advance through the central corporate travel portal. "
        "Expense reports with itemized receipts must be submitted within 15 days following the conclusion of the trip.",
        body_style
    ))

    doc.build(story)
    print(f"Successfully generated sample PDF at: {filename}")


if __name__ == "__main__":
    create_sample_pdf("sample_test_document.pdf")
