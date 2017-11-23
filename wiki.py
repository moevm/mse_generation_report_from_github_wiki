from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from word import wordSave
import mistune
import os
import sys



# {line:"dsfdsfsfdsfsdffsd",bold:True,italic:False,underline:False}

class WikiParser:
    def __init__(self):
        self.word = wordSave()
        self.downloadWikiPage()
        self.word.saveFile()

    def parseLine(self, htmlLine):
        bs = BeautifulSoup(htmlLine, "lxml")

        # print(bs.prettify())
        body = bs.find('body').findChildren(recursive=False)
        # print(body)

        for element in body:
            bold = False
            italic = False
            underline = False
            arr = [{"type": "text", "line": "", "bold": False, "italic": False, "underline": False}]
            # print(element)
            for tag in element.contents:
                if tag!="\n" and tag!="":
                    self.getInner(arr, element)

            if element.name[0:1] == "h" and element.name[0:2] != "hr":
                self.word.addHeading(arr, int(element.name[1:2]))
            if element.name == "p":
                self.word.addPicture(arr)
            if element.name == "li" or element.name == "ul":
                self.word.addList(arr)
            if element.name == "blockquote":
                self.word.addParagraph(arr)
            if element.name != 'p' and element.name[0:1] != "h":
                print(arr)
                print(element)
                print(element.name)

    def getInner(self, arr, htmlTag):
        tag = htmlTag.name
        print(htmlTag)
        if tag!=None:
            print(tag)
        if tag == None:
            # arr.append(arr[-1])
            arr[-1]["line"] = htmlTag
        else:
            if tag=="img":
                arr[-1]["type"] = "img"
                arr[-1]["src"] = htmlTag['src']
                arr[-1]["line"] = htmlTag['alt']
            if tag=="a":
                arr[-1]["src"] = htmlTag['href']
                arr[-1]["type"] = "link"
            for tt in htmlTag.contents:
                if tt != "\n" and tt != "":
                    self.getInner(arr, tt)

        pass

    def getFiles(self, name):
        print(name)
        self.workDir = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\" + name + "\\"
        onlyfiles = [f for f in listdir(self.workDir) if isfile(join(self.workDir, f))]
        print(onlyfiles)
        htmlPage = ""
        for file in onlyfiles:
            self.parseMd(self.workDir + file)

    def parseMd(self, file):
        f = open(file, 'r')
        htmlPage = ""
        for line in f:
            htmlPage += mistune.markdown(line)
        self.parseLine(htmlPage)

    def downloadWikiPage(self):

        #self.titleDeed()
        #return
        #link = str(input())
        link = "https://niksh81@bitbucket.org/niksh81/wikitest"
        os.system("git clone " + link + ".wiki.git")
        self.getFiles(link[link.rfind("/") + 1::].replace(' ', '') + ".wiki")
        # print(page)


print("---------------------------------------")
print("------------- START -------------")
WikiParser()
