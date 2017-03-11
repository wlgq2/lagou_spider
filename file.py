# coding=utf-8

class File:
    def __init__(self,name):
        self.name =name;

    def saveText(self,content):
        fd = open(self.name, 'w', buffering=-1)
        fd.write(content)
        fd.close()

    def startAddText(self):
        fd = open(self.name, 'w', buffering=-1)
        fd.write('***lagou message get*** \n')
        fd.close()

    def addSaveText(self,content):
        fd = open(self.name, 'a', buffering=-1)
        fd.write(content+'\n')
        fd.close()
