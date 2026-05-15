import pdfplumber
import sys

pdf_path = r"c:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\SCS 4010 FINAL YEAR PROJECT.pdf"
output_path = r"c:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\extracted_pdf_content.txt"

try:
    # Extract text from PDF
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}\n")
        
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                all_text += f"\n--- PAGE {i} ---\n{text}"
            else:
                all_text += f"\n--- PAGE {i} ---\n[No text extracted from this page]"
    
    # Save the extracted text to a file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(all_text)
    
    print("Content saved successfully!")
    print(f"Total length: {len(all_text)} characters")
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
