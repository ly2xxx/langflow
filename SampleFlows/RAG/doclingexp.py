from docling.document_converter import DocumentConverter
import os

pdf_path = os.path.join(os.path.dirname(__file__), "6_B0O3_Fact-Sheet_UK-Smaller-Companies-Index-Fund-LG-PMC-UK-Smaller-Companies-Index-Fund-3_31-10-2024.pdf")
md_path = pdf_path.replace('.pdf', '.md')

converter = DocumentConverter()
result = converter.convert(pdf_path)
markdown_content = result.document.export_to_markdown()

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print(f"Markdown file saved to: {md_path}")