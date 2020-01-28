# coding: utf8
import PyPDF2 as o
import requests
import json

pdfRead = o.PdfFileReader(open("maupassant_bel_ami.pdf","rb"))

i=0
pages = []

while i < pdfRead.getNumPages():
    pages.append({
        "numero_page" : i,
        "texte" : pdfRead.getPage(i).extractText()
    })

    if len(pages) >= 5:
        requests.post("http://127.0.0.1:5000/create-transaction", json = pages)
        pages = []
    i = i+1