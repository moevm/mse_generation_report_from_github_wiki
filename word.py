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


	#style='IntenseQuote'-цитата
	#style='ListBullet'-точки	
	#style='ListNumber'-цифры	
	def addParagraph(self, mass):
		style='ListBullet'
		line = self.document.add_paragraph('', style)
		self.reform(mass, line)


	def addPicture(self, mass):
		line = element["name"]
		wig = element["width"]
		leng = element["length"]
		document.add_picture(name, width = wig, length = leng)

	def saveFile(self):
		self.document.save('demo.docx')
