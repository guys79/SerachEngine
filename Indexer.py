import os
from Parser import Parser
from ReadFile import ReadFile
import Queue
import  threading
from Consumer import Consumer
from ParserThread import ParserThread
from AddToDictionaryThread import AddToDictionaryThread
# This class will index all the terms in the collection
class Indexer:
    name_of_files = None # The names of the initial posting files
    file_type = None # The file type of the posting files
    parser = None # The parser of the project
    read_file = None # The ReadFile of the class
    main_dictionary = None
    temp_position_dic = None
    # The constructor of the class
    def __init__(self, corpus_file_path):
        self.name_of_files = {}
        # Initializing the names of the files
        for i in range(0,26):
            for j in range(0, 26):
                self.name_of_files["%s%s"%((chr(ord('a')+i)),(chr(ord('a')+j)))] = Queue.Queue()
        for i in range(0,10):
            for j in range(0, 10):
                self.name_of_files["%s%s"%(('%d' % i),('%d' % j))] = Queue.Queue()
        self.name_of_files['other'] = Queue.Queue()

        # The file type is txt
        self.file_type = 'txt'

        # Creating the initial posting files
        self.create_initial_posting_file()

        # Initializing the Parser
        self.parser = Parser()
        # Initializing the ReadFile
        self.read_file = ReadFile(corpus_file_path)


        # Initializing the dictionary
        self.main_dictionary = {}

        self.temp_position_dic = {}



   # def add_to_dicts(self):
    #    numOfDoc, text = self.read_file.getFile()
    #    counter = 0
    #    num_of_docs = 1000
    #    parser_threads = []
    #    add_to_dictionary_threads = []
    #    text_to_thread = []
    #    while text is not "all docs are received" and counter!=1000:
    #        counter += 1
        #       print(counter)
        #    if counter % num_of_docs ==0:
        #        thread = ParserThread(self.queue_of_parser,self.parser,text_to_thread)
        #        text_to_thread = []
        #        parser_threads.append(thread)
        #        thread.start()
        #        thread = AddToDictionaryThread(self.queue_of_parser,num_of_docs,self.read_file,self.main_dictionary)
        #        add_to_dictionary_threads.append(thread)
        #        thread.start()


        #    text=self.find_sub("TEXT",text)
        #    text_to_thread.append((text,counter))
            #dictionary_of_words, dictionary_of_unique_terms, max_freq=self.parser.parse_to_unique_terms(text)
            #self.add_to_main_dictionary_spacial(dictionary_of_unique_terms)
            #for key in dictionary_of_words:
            #    self.add_term_to_dictionary(key,dictionary_of_words[key])
            #self.read_file.add_to_max_values_dict(max_freq,numOfDoc)
        #    numOfDoc, text = self.read_file.getFile()
        #if len(text_to_thread)!=0:
        #   thread = ParserThread(self.queue_of_parser, self.parser, text_to_thread)
        #    parser_threads.append(thread)
        #    thread.start()
        #    thread = AddToDictionaryThread(self.queue_of_parser, len(text_to_thread), self.read_file, self.main_dictionary)
        #    add_to_dictionary_threads.append(thread)
        #    thread.start()
        #print "wait for parsing"
        #for i in range(0,len(parser_threads)):
        #    parser_threads[i].join()
        #print "wait for dic"
        #for i in range(0,len(add_to_dictionary_threads)):
        #    add_to_dictionary_threads[i].join()
    #print(self.main_dictionary)



    def add_to_dicts2(self):
        numOfDoc, text = self.read_file.getFile()
        coun=0
        num =0
        while text is not "all docs are received" and coun!=1000:
            coun+=1
            print(coun)

            text = self.find_sub("TEXT", text)
            dictionary_of_words, dictionary_of_unique_terms, max_freq = self.parser.parse_to_unique_terms(text)
            self.add_to_main_dictionary_spacial(dictionary_of_unique_terms, numOfDoc)
            for key in dictionary_of_words:
                key = self.add_term_to_dictionary(key)
                self.add_term_to_queue(key, numOfDoc, dictionary_of_words[key])
            self.read_file.add_to_max_values_dict(max_freq, numOfDoc)
            numOfDoc, text = self.read_file.getFile()

    def index_files(self):
        thread_add_to_dic = threading.Thread(target=self.add_to_dicts2())
        threads = []
        for name in self.name_of_files:
            thread = Consumer(self.name_of_files[name],name,self.file_type,self.main_dictionary,1,self.temp_position_dic)
            threads.append(thread)
            thread.start()
        thread_add_to_dic.start()
        thread_add_to_dic.join()
        for i in range(0,len(threads)):
            threads[i].stop_thread()
        for i in range(0, len(threads)):
            threads[i].join()

    def add_to_main_dictionary_spacial(self,dict,doc_id):
        for key in dict:
            if key in self.main_dictionary:
                self.main_dictionary[key][0] = self.main_dictionary[key][0] + 1
            else:
                self.main_dictionary[key] = [1,-1]
                self.temp_position_dic[key] = [-1,-1]

            self.add_term_to_queue(key,doc_id,self.main_dictionary[key][0])

    def add_term_to_queue(self,term,doc_id,tf):
        note = term[0].lower()
        note2=note
        flag1=(note>='a' and note<='z')
        flag2=(note>='0' and note<='9')
        if flag1 or flag2:
            if len(term) > 1:
                low = term[1].lower()
                if ((low>='a' and low<='z') and flag1) or ((low>='0' and low<='9') and flag2):
                    note2 = term[1].lower()
            self.name_of_files["%s%s"%(note,note2)].put((term,doc_id,tf))
            return
        self.name_of_files['other'].put((term, doc_id, tf))
    # This function will create the initial posting files
    def create_initial_posting_file(self):
        # Go through every file name and create it
        for name in self.name_of_files:
            file = open("%s.%s" % (name,self.file_type),"w")
            file.close()
            #os.remove(file.name) # just for now

    # This function will add a term to the dictionary
    def add_term_to_dictionary(self,term):
        # If the term is already in the dictionary
        if term in self.main_dictionary:
            self.main_dictionary[term][0] = self.main_dictionary[term][0] + 1
            return term

        # If the term starts with a capital letter
        if term[0]>='A' and term[0]<='Z':
            lower = term.lower()
            # If the term is already in the dictionary in small letters
            if lower in self.main_dictionary:
                self.main_dictionary[lower][0] = self.main_dictionary[lower][0] + 1
                return lower

        elif term[0] >= 'a' and term[0] <= 'z':
            upper = term.upper()
            # If the term is already in the dictionary in small letters
            if upper in self.main_dictionary:
                self.main_dictionary[term] = [self.main_dictionary[upper][0] + 1,-1]
                self.temp_position_dic[term] = [self.temp_position_dic[key][0], self.temp_position_dic[key][1]]
                del self.temp_position_dic[upper]
                del self.main_dictionary[upper]
                return term
        # If the term is new in the dictionary
        self.main_dictionary[term] = [1,-1]
        self.temp_position_dic[term]=[-1,-1]
        return term

    # This function will return the string between two tags
    def find_sub(self, tag, string):
        start = "<" + tag + ">"
        end1 = "</" + tag + ">"
        string = string[string.find(start) + len(start):string.find(end1)]
        return string


def print_dif(dicsss):
    lists = []
    for key in dicsss:
        lists.append(key)
    lists.sort()
    for i in range(0,len(lists)):
        print("%s %d %d" % (lists[i], dicsss[lists[i]][0], dicsss[lists[i]][1]))

import time
y = time.time()
x = Indexer("C:\Users\guy schlesinger\Desktop\corpus")
x.index_files()
sorted(x.main_dictionary)
print_dif(x.main_dictionary)
flag =True
for key in x.name_of_files:
    if not x.name_of_files[key].empty():
        print("problem - "+key)
    flag = flag and x.name_of_files[key].empty()
print(flag)
print(time.time()-y)




#x.add_to_dic_threads(2000)
#z=-(y-time.time())
#y = time.time()
#d = Indexer("C:\Users\guy schlesinger\Desktop\corpus")
#d.add_to_dic_threads(3000)
#print(z)
#print(-(y-time.time()))
