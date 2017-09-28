from docx import Document

class wordSave:
	def __init__(self):
		self.document = Document()

	def reform(self, mass, line):
		for element in mass:
			x=line.add_run(element["line"])
			x.bold = element["bold"]
			x.italic = element["italic"]
			x.undetline = element["underline"]
		


	def addHeading(self, mass, lvl=1):
		line=self.document.add_heading('',level = lvl)
		self.reform(mass, line)


			
	def addParagraph(self, mass):
		line = self.document.add_paragraph('')
		self.reform(mass, line)

	#ЧТО ПЕРЕДАЕШЬ??
	def addPicture(self, mass):
		line = element["name"]
		wig = element["wight"]
		leng = element["lenght"]
		document.add_picture(name, wight = wig, lenght = leng)

	def saveFile(self):
		self.document.save('demo.docx')