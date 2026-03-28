import io
import PyPDF2

try:
    import pdfplumber
except ImportError:
    pdfplumber = None



def read_pdf(file):
    text = ""

    try:
        pdf_bytes = file.read()

        # Try pdfplumber first
        if pdfplumber is not None:
            try:
                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()

                        if page_text:
                            text += page_text + "\n"
            except Exception:
                pass

        # Fallback to PyPDF2
        if text.strip() == "":
            try:
                reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

                for page in reader.pages:
                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"
            except Exception:
                pass

        if text.strip() == "":
            return "No readable text found in PDF."

        return text.strip()

    except Exception as e:
        return "Error reading PDF: " + str(e)
