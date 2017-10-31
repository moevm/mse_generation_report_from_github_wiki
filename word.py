import io

from docx import Document
from sphinx.util import requests


class wordSave:
    def __init__(self):
        self.document = Document()

    def reform(self, mass, line):
        for element in mass:
            x = line.add_run(element["line"])
            x.bold = element["bold"]
            x.italic = element["italic"]
            x.undetline = element["underline"]

    def addHeading(self, mass, lvl=1):
        line = self.document.add_heading('', level=lvl)
        self.reform(mass, line)

    # style='IntenseQuote'-цитата
    # style='ListBullet'-точки
    # style='ListNumber'-цифры

    def addList(self, mass):
        line = self.document.add_paragraph('',style="ListBullet")
        self.reform(mass, line)

    def addLink(self,mass):
        line = self.document.add_paragraph('')
        #add_hyperlink(line,url=mass[0]['src'])
        self.reform(mass, line)

    def addParagraph(self, mass):
        line = self.document.add_paragraph('')
        self.reform(mass, line)

    def getImgByUrl(self,url):
        response = requests.get(url, stream=True)
        return io.BytesIO(response.content)

    def addPicture(self, mass):
        for elem in mass:
            if elem['type'] == 'img':
                url = elem["src"]
                self.addParagraph([elem])
                print(url)
                self.document.add_picture(self.getImgByUrl(url))
            else:
                if elem['type'] == 'link':
                    self.addLink([elem])
                else:
                    self.addParagraph([elem])

    def saveFile(self):
        self.document.save('demo.docx')
