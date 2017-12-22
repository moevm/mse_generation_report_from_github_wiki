from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from word import wordSave
import mistune
import requests
import io
import os
import sys
import json
import re


# {line:"dsfdsfsfdsfsdffsd",bold:True,italic:False,underline:False}

class WikiParser:
    def __init__(self):
        url = str(input("Enter url to repository: ")).strip()
        self.js = json.load(open('settings.json'))
        self.word = wordSave()
        self.downloadWikiPage(url)
        print("Start parse Issue and pull requests")
        self.parseIssues(url)
        self.word.saveFile()
        print("Ok! Saved to ReadyProject.docx")

    def parseHtmlTag(self, arr, htmlTag, type, bold, italic, underline):
        tag = htmlTag.name
        if tag is None:
            arr[-1]["line"] = tag
        for tt in htmlTag.contents:
            if tt != "\n" and tt != "":
                self.getInner(arr, tt)

    def parseLine(self, htmlLine):
        # print(htmlLine)
        bs = BeautifulSoup(htmlLine, "lxml")

        # print(bs.prettify())
        body = bs.find('body').findChildren(recursive=False)
        # print(body)

        for element in body:
            arr = [{"type": "text", "line": "", "bold": False, "italic": False, "underline": False}]
            for tag in element.contents:
                if tag != "\n" and tag != "":
                    self.getInner(arr, tag, arr[-1])
            n = 0
            while n < len(arr):
                if arr[n]['type'] == "text" and arr[n]['line'] == "":
                    del arr[n]
                else:
                    n += 1

            # print(arr)
            if element.name[0:1] == "h" and element.name[0:2] != "hr":
                self.word.addHeading(arr, int(element.name[1:2]))
            else:
                if element.name == "li" or element.name == "ul":
                    self.word.addList(arr)
                else:
                    self.word.addParagraph(arr)

    def getInner(self, arr, htmlTag, parent):
        tag = htmlTag.name
        # print(htmlTag)

        if tag is None:
            arr.append({"type": "text", "line": htmlTag, "bold": parent['bold'], "italic": parent['italic'],
                        "underline": parent['underline']})
        else:
            if tag == "strong":
                arr.append({"type": "text", "line": "", "bold": True, "italic": parent['italic'],
                            "underline": parent['underline']})
            if tag == "em":
                arr.append({"type": "text", "line": "", "bold": parent['bold'], "italic": True,
                            "underline": parent['underline']})
            if tag == "img":
                parent["type"] = "img"
                parent["src"] = htmlTag['src']
                parent["line"] = htmlTag['alt']
            if tag == "a":
                parent["src"] = htmlTag['href']
                parent["type"] = "link"
            current = arr[-1]
            for tt in htmlTag.contents:
                if tt != "\n" and tt != "":
                    self.getInner(arr, tt, current)
        pass

    def getFiles(self, name):
        # print(name)
        self.workDir = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\" + name + "\\"
        if not os.path.isdir(self.workDir):
            return
        onlyfiles = [f for f in listdir(self.workDir) if isfile(join(self.workDir, f))]
        # print(onlyfiles)
        for n, file in enumerate(onlyfiles):
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
            # print(line)
        self.parseLine(htmlPage)

    @staticmethod
    def getAllInnerFiles(path):
        arr = []
        for file in listdir(path):
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
        # print(onlyfiles)
        ignoreStr = []
        chooseStr = []
        for str in self.js['ignoreFiles']:
            ignoreStr.append(str['regExp'])
        for str in self.js['chooseFiles']:
            chooseStr.append(str['regExp'])
        # print(ignoreStr)
        # print(chooseStr)
        regExpIgnore = re.compile("|".join(ignoreStr))
        regExpChoose = re.compile("|".join(chooseStr))
        answer = []
        for p in onlyfiles:
            hlp = regExpIgnore.search(p)
            if hlp is not None and len(hlp.group(0)) > 0:
                continue
            hlp = regExpChoose.search(p)
            if hlp is not None and len(hlp.group(0)) > 0:
                # print("add" + p)
                answer.append(p)
        count = len(answer)
        for n, file in enumerate(answer):
            self.printCode(file)

    def addLink(self, text, url):
        self.word.addLink(
            [{"type": "link", "src": url, "line": text, "bold": False, "italic": False, "underline": False}])

    def addList(self, text):
        self.word.addList(
            [{"type": "text", "line": text, "bold": False, "italic": False, "underline": False}])

    def addHeading(self, text, lvl):
        self.word.addHeading(
            [{"type": "text", "line": text, "bold": False, "italic": False, "underline": False}], lvl)

    def addParagraph(self, text):
        self.word.addParagraph(
            [{"type": "text", "line": text, "bold": False, "italic": False, "underline": False}])

    def issuePage(self, soup, name):
        self.word.addPageBreak()
        title = soup.findAll("span", class_="js-issue-title")
        self.addHeading(name, 1)
        self.addHeading(title[0].text.strip(), 2)
        state = soup.findAll("div", class_="State")
        self.addParagraph("Status: " + state[0].text.strip())
        openedBy = soup.findAll("a", class_="author")
        self.addParagraph("Opened by: " + openedBy[0].text.strip())
        comments = soup.findAll("div", class_="js-discussion")[0]
        for tt in comments.contents:
            if tt.name is not None:

                if tt['class'][0] == "timeline-comment-wrapper":
                    openedBy = tt.findAll("a", class_="author text-inherit")
                    self.addHeading("Commented by: " + openedBy[0].text.strip(), 2)
                    form = tt.findAll("td", class_="comment-body")
                    if len(form) > 0:
                        self.parseLine("".join([str(x) for x in form[0].contents]))
                else:
                    if tt['class'][0] == "discussion-item":
                        mes = tt.findAll("a", class_="message")
                        if len(mes) > 0:
                            self.addList(mes[0].text.strip())
                        else:
                            self.addList(" ".join(tt.text.split()))

    def parseIssues(self, url):
        i = 1
        max = self.js["maxIssueAndPull"]
        regExp = re.compile("/issues/")
        if max is None or max < 0:
            max = 5
        r = requests.get(url + "/pull/1")
        while r.status_code == 200 and i < max:
            i += 1
            print(r.url)
            soup = BeautifulSoup(r.text, "lxml")
            help = regExp.search(r.url)
            if help is not None:
                self.issuePage(soup, "Issue")
            else:
                self.issuePage(soup, "Pull request")
            r = requests.get(url + "/pull/" + str(i))

    def downloadWikiPage(self, link):
        # self.titleDeed()
        # return
        # link = str(input())
        os.system("git clone " + link + ".git")
        os.system("git clone " + link + ".wiki.git")
        print("Start parse wiki pages")
        self.getFiles(link[link.rfind("/") + 1::].replace(' ', '') + ".wiki")
        print("Start parse code files")
        self.addCodeFiles(link[link.rfind("/") + 1::].replace(' ', ''))
        # print(page)

print("------------- START -------------")

WikiParser()
