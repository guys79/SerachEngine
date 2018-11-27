import os

class ReadFile:
    my_dict = {}
    indexInFile = 0 # The index in the docsInFile list
    indexInDirectory = 0 # The index of the namesInDirectory list
    namesInDirectory = [] # The paths of all the files in the corpus
    docsInFile = [] # In every cell in there is a number and a list. The number is the docId and the list is the content of the file
    doc_id_generator = 1 #The counter of the document, the counter is the docId vlue
    dictionary_doc_name_id = {} # A dictionary, The key is the name of the doc, and the value is the dicId

    # a helper function that should find the name of the document
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

    # this function should get the name of the file and return arr of strings that contains the lines of the file
    def store_files(self, start, end,content):
        newArrey=[]
        for i in range(start, end+1):
            newArrey.append(content[i])

        name = self.findTheName(content,start)
        tempArr=[self.doc_id_generator,newArrey]
        self.dictionary_doc_name_id[self.doc_id_generator] =name
        self.doc_id_generator = self.doc_id_generator + 1
        self.docsInFile.append(tempArr)
    # returns the next document in the the corpus directory
    def getFile(self):

        # check if all docs have been returned
        if self.indexInDirectory==len(self.namesInDirectory):
            return "all docs are received"
        # in case we have to create a new arrey out of a file that includes a lot of docs
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

    # we initilize the class
    def __init__(self,path):
        self.indexInFile = 0
        self.indexInDirectory = 0
        self.namesInDirectory = []
        self.docsInFile = []
        # initilazation of the namesInDirectory arrey
        for filename in os.listdir(path):
            slesh="A\H"
            slesh=slesh[1]
            filename=path+slesh+filename
            self.namesInDirectory.append(filename)
        return



