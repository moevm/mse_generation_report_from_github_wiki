import io
import json
from docx import Document
from sphinx.util import requests
from docxtpl import DocxTemplate, RichText
import docx.enum.style as style


class wordSave:
    def __init__(self):
        self.makeTitul()
        self.document = Document('compileTitul.docx')

    def makeTitul(self):
        tpl = DocxTemplate('patternTitle.docx')
        js = json.load(open('settings.json'))
        context = {
            'cathedra': RichText(js['cathedra'].encode('cp1251', 'ignore')),
            'discipline': RichText(js['discipline'].encode('cp1251', 'ignore')),
            'theme': RichText(js['theme'].encode('cp1251', 'ignore')),
            'group': RichText(js['group'].encode('cp1251', 'ignore')),
            'name': RichText(js['name'].encode('cp1251', 'ignore')),
            'teacher': RichText(js['teacher'].encode('cp1251', 'ignore')),
            'initialData': RichText(js['initialData'].encode('cp1251', 'ignore')),
            'content': RichText(js['content'].encode('cp1251', 'ignore')),
            'numberPages ': RichText(js['numberPages'].encode('cp1251', 'ignore')),
            'surrender': RichText(js['surrender'].encode('cp1251', 'ignore')),
            'numberPages': RichText(js['numberPages'].encode('cp1251', 'ignore')),
            'extradition': RichText(js['extradition'].encode('cp1251', 'ignore')),
            'protection': RichText(js['protection'].encode('cp1251', 'ignore')),
            'annotation': RichText(js['annotation'].encode('cp1251', 'ignore')),
            'summary': RichText(js['summary'].encode('cp1251', 'ignore')),
            'introduction': RichText(js['introduction'].encode('cp1251', 'ignore')),
        }

        tpl.render(context)
        tpl.save('compileTitul.docx')

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
        line = self.document.add_paragraph('')
        self.reform(mass, line)

    def addLink(self, mass):
        line = self.document.add_paragraph('')
        # add_hyperlink(line,url=mass[0]['src'])
        self.reform(mass, line)

    def addParagraph(self, mass):
        line = self.document.add_paragraph('')
        self.reform(mass, line)

    def getImgByUrl(self, url):
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
