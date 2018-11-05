import os
my_dict = {}
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
        nameOfFile=myString[myString.find(start)+len(start)+1:myString.find(end)]
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
        for i in range(start, end):
            newArrey.append(content[i])
        my_dict[self.findTheName(content,start)]=newArrey

    def sepereteFiles(self):
        #try:
         #   os.mkdir("allDocs")
        #except IOError:
         #   print("already exist")
        path= "C:\Users\yonatan\Desktop\corpus"
        #input("Enter a path:   ")
        yosy=0
        for filename in os.listdir(path):
            print("i is")
            print(yosy)
            yosy=yosy+1
            slesh="A\H"
            slesh=slesh[1]
            filename=path+slesh+filename
            for file in os.listdir(filename):
                file=filename+slesh+file
                the_file= open(file,"r")
                with the_file:
                    arreyOfFile= the_file.readlines()
                    for i in range(0,len(arreyOfFile)):
                        if "<DOC>" in arreyOfFile[i]:
                            num=i
                            while False == ("</DOC>" in arreyOfFile[num]):
                                num=num+1
                            self.store_files(i,num,arreyOfFile)
                the_file.close()

    def inite(self):
        return
x= justATest()
x.sepereteFiles()