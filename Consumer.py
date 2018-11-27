import threading
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
        self.posting_file = open(self.file_path,"w")
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
        # If new, find the right place to insert, and than insert and update the list of line positions
        #if not new, find the term, add the gap, update the list
        self.posting_file = open(self.file_path,"r+")
        begin = 0
        end = self.posting_file.tell()
        self.posting_file.seek()

    # If this is the first appearance of the term
    def new_case(self,term,doc_id,number_of_occurrences):

        return

    # If this is not the first appearance of the term
    def old_case(self,term,doc_id,number_of_occurrences):
        return











