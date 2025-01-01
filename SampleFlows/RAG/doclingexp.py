# from docling.document_converter import DocumentConverter
# import os

# pdf_path = os.path.join(os.path.dirname(__file__), "6_B0O3_Fact-Sheet_UK-Smaller-Companies-Index-Fund-LG-PMC-UK-Smaller-Companies-Index-Fund-3_31-10-2024.pdf")
# md_path = pdf_path.replace('.pdf', '.md')

# converter = DocumentConverter()
# result = converter.convert(pdf_path)
# markdown_content = result.document.export_to_markdown()

# with open(md_path, 'w', encoding='utf-8') as f:
#     f.write(markdown_content)

# print(f"Markdown file saved to: {md_path}")

from docling.document_converter import DocumentConverter
import os

class DocumentProcessor:
    def __init__(self):
        self.converter = DocumentConverter()
        self.input_dir = os.path.join(os.path.dirname(__file__), "input")
        
    def process_all_pdfs(self):
        # Create input directory if it doesn't exist
        if not os.path.exists(self.input_dir):
            os.makedirs(self.input_dir)
            
        # Process each PDF file
        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(self.input_dir, filename)
                md_path = pdf_path.replace('.pdf', '.md')
                
                # Skip if markdown file already exists
                if os.path.exists(md_path):
                    print(f"Skipping {filename} - markdown file already exists")
                    continue
                
                # Convert PDF to markdown
                try:
                    result = self.converter.convert(pdf_path)
                    markdown_content = result.document.export_to_markdown()
                    
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    
                    print(f"Successfully converted {filename} to markdown")
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.process_all_pdfs()
