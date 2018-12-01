import threading
import Queue
# This class will be the consumer of the index
# This class will be responsible for one file and will update it
# Using the list of the index
class Consumer (threading.Thread):
    list_of_terms = None # The list of terms, each term is (term,doc_num,number of occurrences)
    file_path = None # The path of the file
    posting_file = None # The posting file
    list_of_line_positions = None # List of all the line positions in char (the position of the first character in the line)
    line_length = -1 # The constant length of the line
    doc_id_length = -1# The constant length of the doc_id
    tf_length = -1# The constant length of the tf
    pointer_length = -1# The constant length of the pointer
    number_last_line = -1 # number of lines on the file
    dictionary_of_terms = None # The main dictionary in the indexer
    index_of_location_in_file = -1 # The index in the dictionary value that represents the number of line in the posting that the term begins
    exit_sign = None
    is_waiting = None
    lock = None
    temp_position_dic = None
    # The constructor of the class
    def __init__(self,list_of_terms,file_name,file_type,dictionary_of_terms,index_of_location_in_file,temp_position_dic):
        threading.Thread.__init__(self)
        self.list_of_terms = list_of_terms
        self.file_path = "%s.%s" % (file_name,file_type)
        self.list_of_line_positions = [0]
        self.line_length = 22
        self.doc_id_length = 7
        self.tf_length = 5
        self.pointer_length = 10
        self.number_last_line = 0
        self.dictionary_of_terms = dictionary_of_terms
        self.index_of_location_in_file = index_of_location_in_file
        self.exit_sign = False
        self.is_waiting = True
        self.lock = threading.Lock()
        self.temp_position_dic =temp_position_dic


    def run(self):
        self.consume()
        print(self.file_path+" Done!")

    def consume(self):
        while not self.exit_sign or not self.list_of_terms.empty():
            try:
                item = self.list_of_terms.get(True,1)
                self.process(item)
                self.list_of_terms.task_done()
            except Queue.Empty:
                1



    def process(self,item):
        self.add_new_line(self.dictionary_of_terms[item[0]][self.index_of_location_in_file], item[1], item[2],item[0])
        if self.dictionary_of_terms[item[0]][self.index_of_location_in_file] == -1:
            self.dictionary_of_terms[item[0]][self.index_of_location_in_file] = self.number_last_line - 1
        return

    def stop_thread(self):
        self.exit_sign = True


    # doc_id = 7 digits
    # tf = 5 digits
    # pointer 10 digit
    def find_term_location(self,term_location):


        returned_pointer = -1
        # doc_id = line[:doc_id_length]
        # tf = line[doc_id_length:doc_id_length+tf_length]
        # print line
        # print(doc_id)
        # print(tf)
        # print(pointer)
        last_doc_id = 0
        term_location = term_location * self.line_length
        returned_pointer = term_location
        null_pointer = self.define_null_pointer()
        self.posting_file.seek(term_location)
        line = self.posting_file.read(self.line_length)
        pointer = line[self.doc_id_length + self.tf_length:]
        last_doc_id = last_doc_id + self.string_to_number(line[:self.doc_id_length])
        pointer_in_num = self.string_to_number(pointer)
        pointer_in_num = pointer_in_num * self.line_length

        while (pointer != null_pointer):
            self.posting_file.seek(pointer_in_num)
            line = self.posting_file.read(self.line_length)
            pointer = line[self.doc_id_length + self.tf_length:]
            last_doc_id = last_doc_id + self.string_to_number(line[:self.doc_id_length])
            returned_pointer = pointer_in_num
            pointer_in_num = self.string_to_number(pointer)
            pointer_in_num = pointer_in_num * self.line_length
        return returned_pointer, last_doc_id

    def define_null_pointer(self):
        null_pointer = ""
        for i in range(0, self.pointer_length):
            null_pointer = null_pointer + "0"
        return null_pointer

    def string_to_number(self,string_num):
        return int(string_num)

    def number_to_string(self,num, string_length):
        new_string = ""
        num_as_string = str(num)
        for i in range(0, string_length - len(num_as_string)):
            new_string = new_string + "0"
        new_string = new_string + num_as_string
        return new_string

    def add_new_line(self,term_location,  doc_id,tf,term):

        null_pointer = self.define_null_pointer()
        self.posting_file = open(self.file_path, "r+")
        if term_location != -1:
            #index, last_doc_id = self.find_term_location(term_location)
            index = self.temp_position_dic[term][1]
            last_doc_id = self.temp_position_dic[term][0]
            doc_id = doc_id - last_doc_id  # The gap
            self.posting_file.seek(index + self.tf_length + self.doc_id_length)
            self.posting_file.write(self.number_to_string(self.number_last_line, self.pointer_length))

        new_string = "%s%s%s" % (self.number_to_string(doc_id, self.doc_id_length), self.number_to_string(tf, self.tf_length), null_pointer)
        self.posting_file.close()
        self.posting_file = open(self.file_path, "a")
        self.posting_file.write(new_string)
        self.posting_file.close()
        self.temp_position_dic[term][0] = doc_id
        self.temp_position_dic[term][1] = self.number_last_line
        self.number_last_line = self.number_last_line + 1







