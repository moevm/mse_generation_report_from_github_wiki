from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from word import wordSave
import mistune
import io
import os
import sys
import json
import re


# {line:"dsfdsfsfdsfsdffsd",bold:True,italic:False,underline:False}

class WikiParser:
    def __init__(self):
        self.js = json.load(open('settings.json'))
        self.word = wordSave()
        self.downloadWikiPage()
        self.word.saveFile()

    def parseLine(self, htmlLine):
        # print(htmlLine)
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
                if tag != "\n" and tag != "":
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

        if tag is None:
            # arr.append(arr[-1])
            arr[-1]["line"] = htmlTag
        else:
            if tag == "img":
                arr[-1]["type"] = "img"
                arr[-1]["src"] = htmlTag['src']
                arr[-1]["line"] = htmlTag['alt']
            if tag == "a":
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
        for file in onlyfiles:
            try:
                self.parseMd(self.workDir + file)
            except Exception:
                print("encoding file Exception")
                continue

    def parseMd(self, file):
        with io.open(file, 'r', encoding='utf8') as fileHelp:
            f = fileHelp.readlines()
        htmlPage = ""
        for line in f:
            htmlPage += mistune.markdown(line)
            print(line)
        self.parseLine(htmlPage)

    @staticmethod
    def getAllInnerFiles(path):
        arr = []
        for file in listdir(path):
            print(isfile(file))
            if os.path.isfile(join(path, file)):
                arr.append(join(path, file))
            else:
                if os.path.isdir(join(path, file)):
                    arr += WikiParser.getAllInnerFiles(join(path, file))
        return arr

    def printCode(self, filePath):
        with io.open(filePath, 'r', encoding='utf8') as fileHelp:
            f = fileHelp.readlines()
        self.word.addPageBreak()
        self.word.addHeadCode(filePath[len(os.path.dirname(sys.argv[0])) + 1:])
        self.word.addCode(f)

    def addCodeFiles(self, name):
        path = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\" + name + "\\"
        onlyfiles = WikiParser.getAllInnerFiles(path)
        print(onlyfiles)
        ignoreStr = []
        chooseStr = []
        for str in self.js['ignoreFiles']:
            ignoreStr.append(str['regExp'])
        for str in self.js['chooseFiles']:
            chooseStr.append(str['regExp'])
        print(ignoreStr)
        print(chooseStr)
        regExpIgnore = re.compile("|".join(ignoreStr))
        regExpChoose = re.compile("|".join(chooseStr))
        answer = []
        for p in onlyfiles:
            hlp = regExpIgnore.search(p)
            if hlp is not None and len(hlp.group(0)) > 0:
                print("ignore" + p)
                continue
            hlp = regExpChoose.search(p)
            if hlp is not None and len(hlp.group(0)) > 0:
                print("add" + p)
                answer.append(p)
        for file in answer:
            self.printCode(file)

    # def parseIssue(self):

    def downloadWikiPage(self):
        # self.titleDeed()
        # return
        # link = str(input())
        link = "https://github.com/facebook/react"
        os.system("git clone " + link + ".git")
        os.system("git clone " + link + ".wiki.git")
        self.getFiles(link[link.rfind("/") + 1::].replace(' ', '') + ".wiki")
        self.addCodeFiles(link[link.rfind("/") + 1::].replace(' ', ''))
        # print(page)


print("---------------------------------------")
print("------------- START -------------")

WikiParser()
