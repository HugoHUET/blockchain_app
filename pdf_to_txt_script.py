import requests
import PyPDF2 as o
openPDF = open("Bel_Ami.pdf","rb")
pdfRead = o.PdfFileReader(openPDF)
print(pdfRead.getPage(0).extractText())
print(pdfRead.getNumPages())


i=0

pages_arr = []
pages = {}

while i < pdfRead.getNumPages():
    page = pdfRead.getPage(i)
    text = page.extractText()
    print(text)
    i = i+1
    pages = {
        'numero_page': page,
        'texte': text,
    }
    pages_arr.append(pages)
    if len(pages_arr)==4:
        print(pages_arr)
        requests.post("http://127.0.0.1:5000/create-transaction", json = pages_arr)
        pages_arr= []