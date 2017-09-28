from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from word import wordSave
import mistune
import os
import sys


#{line:"dsfdsfsfdsfsdffsd",bold:True,italic:False,underline:False}

class WikiParser:
    def __init__(self):
        self.word = wordSave()
        self.downloadWikiPage()
        self.word.saveFile()
        


    def parseLine(self,htmlLine):
        bs = BeautifulSoup(htmlLine)

        print(bs.prettify())
        body = bs.find('body').findChildren(recursive=False)
        print(body[0].contents)

        for element in body:
            bold = False
            italic = False
            underline = False
            arr = [{"line":"","bold":False,"italic":False,"underline":False}]
            for tag in element.contents:
                self.getInner(arr,tag)
            if (element.name[0:1] == "h"):
                self.word.addHeading(arr)
            else:
                self.word.addParagraph(arr)



    def getInner(self,arr,htmlTag):
        tag = htmlTag.name
        if tag==None:
            arr.append(arr[-1])
            arr[-1]["line"] = htmlTag
        else:
            for tt in htmlTag.contents:
                self.getInner(arr,tt)

        pass



    def getFiles(self,name):
        print(name)
        self.workDir = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\" + name + "\\"
        onlyfiles = [f for f in listdir(self.workDir) if isfile(join(self.workDir, f))]
        print(onlyfiles)
        htmlPage = ""
        for file in onlyfiles:
            self.parseMd(self.workDir + file)

    def parseMd(self,file):
        f = open(file, 'r')
        htmlPage=""
        for line in f:
            htmlPage+=mistune.markdown(line)
        self.parseLine(htmlPage)

    def downloadWikiPage(self):
        link = str(input())
        #link = "https://gist.github.com/subfuzion/0d3f19c4f780a7d75ba2"
        os.system("git clone "+link+".wiki.git")
        self.getFiles(link[link.rfind("/")+1::]+".wiki")
        #print(page)

WikiParser()