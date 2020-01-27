import PyPDF2 as o
openPDF = open("Bel_Ami.pdf","rb")
pdfRead = o.PdfFileReader(openPDF)
print(pdfRead.getPage(0).extractText())
print(pdfRead.getNumPages())
print(pdfRead.isEncrypted)
print(pdfRead.getDocumentInfo())

i=0

while i < pdfRead.getNumPages():
    page = pdfRead.getPage(i)
    text = page.extractText()
    print(text)
    i = i+1