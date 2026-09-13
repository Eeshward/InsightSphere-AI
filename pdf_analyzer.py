import pypdf
from text_analyzer import analyze_text

def extract_pdf_text(file_obj):
    file_obj.seek(0)
    reader = pypdf.PdfReader(file_obj)
    pages = []

    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")

    return "\n".join(pages), len(reader.pages)

def analyze_pdf(file_obj, summary_sentences=7, top_keywords=15):
    text, pages = extract_pdf_text(file_obj)
    result = analyze_text(
        text,
        summary_sentences=summary_sentences,
        top_keywords=top_keywords
    )
    result["pages"] = pages
    return result
