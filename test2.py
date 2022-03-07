import pdfplumber

pdf = pdfplumber.open("아뱅.pdf")

plum = len(pdf.pages)

for i in range(plum):
    
    p = pdf.pages[i]
    print(p.extract_text())