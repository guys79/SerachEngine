import os
my_dict = {}
indexInFile=0
indexInDirectory=0
namesInDirectory=[]
docsInFile=[]
class justATest:

    def findTheName(self,content,firstLine):
        found1 = -1
        i = firstLine
        while found1==-1:
            found1=content[i].find("<DOCNO>")
            i=i+1
        start= "<DOCNO>"
        i=i-1
        end= "</DOCNO>"
        myString=content[i]
        nameOfFile=myString[myString.find(start)+len(start)+1:myString.find(end)-1]
        return nameOfFile

    def storeFiles(self, start, end,content,path):
        try:
            slesh = "A\H"
            slesh = slesh[1]
            myFile= open(os.path.join("allDocs", self.findTheName(content,start)), 'a+')
        except IOError:
            print("there has been a problem creating the file")
        with myFile:
            for i in range(start,end):
                myFile.write(content[i])

    def store_files(self, start, end,content):
        newArrey=[]
        for i in range(start, end+1):
            newArrey.append(content[i])
        tempArr=[self.findTheName(content,start),newArrey]
        self.docsInFile.append(tempArr)

    def getFile(self):
        if self.indexInDirectory==len(self.namesInDirectory):
            return "all docs are received"
        if self.indexInFile==len(self.docsInFile):
            self.docsInFile=[]
            for file in os.listdir(self.namesInDirectory[self.indexInDirectory]):
                slesh = "A\H"
                slesh = slesh[1]
                file = self.namesInDirectory[self.indexInDirectory] + slesh + file
                the_file = open(file, "r")
                with the_file:
                    arreyOfFile = the_file.readlines()
                    for i in range(0, len(arreyOfFile)):
                        if "<DOC>" in arreyOfFile[i]:
                            num = i
                            while False == ("</DOC>" in arreyOfFile[num]):
                                num = num + 1
                            self.store_files(i, num, arreyOfFile)
                the_file.close()
            self.indexInFile=0
            return self.getFile()
        else:
            self.indexInFile=self.indexInFile+1
            if self.indexInFile == len(self.docsInFile):
                self.indexInDirectory = self.indexInDirectory + 1
            return self.docsInFile[self.indexInFile-1]

    def __init__(self,path):
        self.indexInFile = 0
        self.indexInDirectory = 0
        self.namesInDirectory = []
        self.docsInFile = []
        for filename in os.listdir(path):
            slesh="A\H"
            slesh=slesh[1]
            filename=path+slesh+filename
            self.namesInDirectory.append(filename)
        return


