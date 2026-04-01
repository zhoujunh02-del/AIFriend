import fitz, docx

def parse_document(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return parse_pdf(file_path)
    elif file_path.endswith(".docx"):
        return parse_docx(file_path)
    elif file_path.endswith(".txt") or file_path.endswith(".md"):
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

def parse_pdf(file_path):
    res = []
    doc = fitz.open(file_path)
    for page in doc:
        text = page.get_text()
        res.append(text)
    return "".join(res)

def parse_docx(file_path):
    res = []
    doc = docx.Document(file_path)
    for paragraph in doc.paragraphs:
        text = paragraph.text
        res.append(text)
    return "".join(res)

def parse_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()