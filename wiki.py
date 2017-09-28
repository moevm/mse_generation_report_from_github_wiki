from os import listdir
from os.path import isfile, join
import requests as rq
import mistune
import os
import sys


class WikiParser:
    def __init__(self):
        self.downloadWikiPage()


    def getFiles(self,name):
        print(name)
        self.workDir = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\" + name + "\\"
        onlyfiles = [f for f in listdir(self.workDir) if isfile(join(self.workDir, f))]
        print(onlyfiles)
        for file in onlyfiles:
            self.parseMd(self.workDir + file)
        pass

    def parseMd(self,file):
        
        f = open(file, 'r')
        for line in f:
            if line!=" ":
                print(mistune.markdown(line),end='')

    def downloadWikiPage(self):
        #link = str(input())
        link = "https://gist.github.com/subfuzion/0d3f19c4f780a7d75ba2"
        os.system("git clone "+link+".wiki.git")
        self.getFiles(link[link.rfind("/")+1::]+".wiki")
        #print(page)

WikiParser()