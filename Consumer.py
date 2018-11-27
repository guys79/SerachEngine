import threading
from StopWordsHolder import StopWordsHolder
# This class will be the consumer of the index
# This class will be responsible for one file and will update it
# Using the list of the index
class Consumer (threading.Thread):
    list_of_terms = None # The list of terms, each term is (term,doc_num,number of occurrences, new or not)
    file_path = None # The path of the file
    posting_file = None # The posting file
    list_of_line_positions = None # List of all the line positions in char (the position of the first character in the line)
    # The constructor of the class
    def __init__(self,list_of_terms,file_name,file_type):
        threading.Thread.__init__(self)
        self.list_of_terms = list_of_terms
        self.file_path = "%s.%s" % (file_name,file_type)
        #self.posting_file = open(self.file_path,"w")
        self.posting_file = open(self.file_path,"r")
        self.posting_file.close()
        self.list_of_line_positions = [0]



    def run(self):
        print("implemented function")

    def consume(self):
        while True:
            item = self.list_of_terms.get()
            self.process(item)
            self.list_of_terms.task_done()

    def process(self,item):
        #If new, find the right place to insert, and than insert and update the list of line positions
        #if not new, find the term, add the gap, update the list
        self.posting_file = open(self.file_path,"r+")
        begin = 0
        end = self.posting_file.tell()
        self.posting_file.seek()

    # If this is the first appearance of the term
    def new_case(self,term,doc_id,number_of_occurrences):
        self.posting_file = open(self.file_path, "r+")
        index = self.binary_search_nearest(term)
        new_line = "%s[%d_%d]" % (term,doc_id,number_of_occurrences)
        print(index)
        self.posting_file.seek(index)
        self.posting_file.write(new_line)
        self.posting_file.close()
        return

    # If this is not the first appearance of the term
    def old_case(self,term,doc_id,number_of_occurrences):
        return

    def binary_search_nearest(self, key):

        begin = 0
        end = len(self.list_of_line_positions) - 1
        index = -1
        line = ""
        while begin <= end:
            middle = (begin + end) / 2
            self.posting_file.seek(self.list_of_line_positions[middle])
            if middle != len(self.list_of_line_positions) -1:
                line = self.posting_file.read(self.list_of_line_positions[middle+1]-self.list_of_line_positions[middle]-1)
            else:
                line = self.posting_file.read()
            term = self.get_term(line)
            if key > term:
                begin = middle + 1
            else:
                index = self.list_of_line_positions[middle]
                end = middle - 1
        return index

    def get_term(self,long_string):
        return long_string[:long_string.find(",[")]



x = Consumer([],"test","txt")
s = StopWordsHolder()
indices = [0]

for i in range(0,len(s.list_of_stop_words)-1):
    if i == 179:
        print s.list_of_stop_words[i]
    indices.append(indices[i]+2+len(s.list_of_stop_words[i]))
x.list_of_line_positions = indices
print(indices)

filrd = open("test.txt","w")
sd=""
for i in range(0,len(s.list_of_stop_words)):
    sd = sd + s.list_of_stop_words[i] +",["
sd=sd[:-1]
filrd.writelines(sd)
filrd.close()
x.new_case("guy",7,6)







