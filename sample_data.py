"""
Sample Data Module for Demo Mode
Contains sample company policy text to allow instant demonstration without uploading a PDF.
"""

from typing import List, Dict, Any

SAMPLE_DOCUMENT_NAME = "company_policy.pdf"

SAMPLE_PAGES: List[Dict[str, Any]] = [
    {
        "page": 1,
        "text": (
            "Company Policy Document - Chapter 1: General Employee Rules & Conduct. "
            "Working hours are 9:00 AM to 5:00 PM Monday through Friday. "
            "Remote work is permitted up to 2 days per week with prior supervisor approval. "
            "All employees are expected to maintain professional conduct and arrive punctually."
        )
    },
    {
        "page": 2,
        "text": (
            "Company Policy Document - Chapter 2: Refund & Return Rules. "
            "Customers can return purchased items within 30 days of purchase for a full refund "
            "if accompanied by the original receipt. Returns requested after 30 days but within 60 days "
            "are eligible for store credit only. Non-refundable items include custom merchandise."
        )
    },
    {
        "page": 3,
        "text": (
            "Company Policy Document - Chapter 3: Leave & Time Off Policy. "
            "Full-time employees are entitled to 20 days of paid annual leave per calendar year. "
            "Sick leave is granted up to 10 paid days annually. Maternity and paternity leave "
            "provide 12 weeks of fully paid leave following the birth or adoption of a child."
        )
    },
    {
        "page": 4,
        "text": (
            "Company Policy Document - Chapter 4: Cybersecurity & Data Protection. "
            "All employees must enforce multi-factor authentication (MFA) on all corporate accounts. "
            "Workstations must be locked whenever leaving your desk. Passwords must be updated every 90 days "
            "and must contain at least 12 characters including symbols."
        )
    }
]

SAMPLE_QUERIES = [
    "What is the refund policy?",
    "How many days of leave are allowed?",
    "What are the security guidelines?",
    "What are the working hours?"
]
