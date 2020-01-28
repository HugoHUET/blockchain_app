# coding: utf8
import PyPDF2 as o
import requests
import json

pdfRead = o.PdfFileReader(open("maupassant_bel_ami.pdf","rb"))

i=0
pages = []

pages_arr = []
pages = {}

while i < pdfRead.getNumPages():
    pages.append({
        "numero_page" : i,
        "texte" : pdfRead.getPage(i).extractText()
    })

    if len(pages) >= 5:
        requests.post("http://127.0.0.1:5000/create-transaction", json = pages)
        pages = []
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