#!/usr/bin/env python3
import subprocess
import sys

# First try to install PyPDF2
print("Installing PyPDF2...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "PyPDF2", "-q"])

import PyPDF2

pdf_path = r"c:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\SCS 4010 FINAL YEAR PROJECT.pdf"
output_path = r"c:\Users\DELL\Projects\FERTILE MAP-AI-POWERED\extracted_pdf_content.txt"

try:
    # Extract text from PDF
    all_text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print(f"Total pages: {len(reader.pages)}\n")
        
        for i, page in enumerate(reader.pages, 1):
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
    print(f"Saved to: {output_path}")
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
