import os
from Parser import Parser
from ReadFile import ReadFile
import Queue
import  threading
from ParserThread import ParserThread
from AddToDictionaryThread import AddToDictionaryThread
# This class will index all the terms in the collection
class Indexer:
    name_of_files = None # The names of the initial posting files
    file_type = None # The file type of the posting files
    parser = None # The parser of the project
    read_file = None # The ReadFile of the class
    main_dictionary = None
    empty_semaphores = None
    queue_of_parser = None
    # The constructor of the class
    def __init__(self, corpus_file_path):
        self.queue_of_parser = Queue.Queue()
        self.name_of_files = []
        # Initializing the names of the files
        for i in range(0,26):
            self.name_of_files.append(chr(ord('a')+i))
        for i in range(0,10):
            self.name_of_files.append('%d' % i)
        self.name_of_files.append('other')

        # The file type is txt
        self.file_type = 'txt'

        # Creating the initial posting files
        self.create_initial_posting_file()

        # Initializing the Parser
        self.parser = Parser()
        # Initializing the ReadFile
        self.read_file = ReadFile(corpus_file_path)

        # Initializing the array of semaphores
        self.empty_semaphores = []

        # Initializing the dictionary
        self.main_dictionary = {}

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

    def add_to_dicts(self,texts):
        for i in range(0,len(texts)):
            dictionary_of_words, dictionary_of_unique_terms, max_freq = self.parser.parse_to_unique_terms(texts[i][0])
            self.add_to_main_dictionary_spacial(dictionary_of_unique_terms)
            for key in dictionary_of_words:
                self.add_term_to_dictionary(key, dictionary_of_words[key])
            self.read_file.add_to_max_values_dict(max_freq, texts[i][1])


    def add_to_dic_threads(self,num_of_docs):
        numOfDoc, text = self.read_file.getFile()
        coun = 0
        texts = []
        threads = []
        while text is not "all docs are received" and coun!=6000:
            coun+=1
            print(coun)
            if coun% num_of_docs == 0:
                thread = threading.Thread(target=self.add_to_dicts(texts))
                texts = []
                threads.append(thread)
                thread.start()
            text = self.find_sub("TEXT", text)
            texts.append((text,numOfDoc))
            numOfDoc, text = self.read_file.getFile()

        for i in range(0,len(threads)):
            threads[i].join()

    def add_to_dicts2(self):
        numOfDoc, text = self.read_file.getFile()
        coun=0
        while text is not "all docs are received":
            coun+=1
            print(coun)
            text = self.find_sub("TEXT", text)
            if coun==11563:
                print text
            if coun>11562:
                dictionary_of_words, dictionary_of_unique_terms, max_freq = self.parser.parse_to_unique_terms(text)
                self.add_to_main_dictionary_spacial(dictionary_of_unique_terms)
                for key in dictionary_of_words:
                    self.add_term_to_dictionary(key, dictionary_of_words[key])
                self.read_file.add_to_max_values_dict(max_freq, numOfDoc)
            numOfDoc, text = self.read_file.getFile()
    def add_to_main_dictionary_spacial(self,dict):
        for key in dict:
            if key in self.main_dictionary:
                self.main_dictionary[key] = self.main_dictionary[key] + dict[key]
            else:
                self.main_dictionary[key]=dict[key]


    # This function will create the initial posting files
    def create_initial_posting_file(self):
        # Go through every file name and create it
        for i in range(0,len(self.name_of_files)):
            file = open("%s.%s" % (self.name_of_files[i],self.file_type),"w")
            file.close()
            os.remove(file.name) # just for now

    # This function will add a term to the dictionary
    def add_term_to_dictionary(self,term,count):
        # If the term is already in the dictionary
        if term in self.main_dictionary:
            self.main_dictionary[term] = self.main_dictionary[term] + count
            return

        # If the term starts with a capital letter
        if term[0]>='A' and term[0]<='Z':
            lower = term.lower()
            # If the term is already in the dictionary in small letters
            if lower in self.main_dictionary:
                self.main_dictionary[lower] = self.main_dictionary[lower] + count
                return

        elif term[0] >= 'a' and term[0] <= 'z':
            upper = term.upper()
            # If the term is already in the dictionary in small letters
            if upper in self.main_dictionary:
                self.main_dictionary[term] = self.main_dictionary[upper] + count
                del self.main_dictionary[upper]
                return

        # If the term is new in the dictionary
        self.main_dictionary[term] = count

    # This function will return the string between two tags
    def find_sub(self, tag, string):
        start = "<" + tag + ">"
        end1 = "</" + tag + ">"
        string = string[string.find(start) + len(start):string.find(end1)]
        return string





x = Indexer("C:\Users\guy schlesinger\Desktop\corpus")
x.add_to_dicts2()
#import time
#y = time.time()
#x.add_to_dic_threads(2000)
#z=-(y-time.time())
#y = time.time()
#d = Indexer("C:\Users\guy schlesinger\Desktop\corpus")
#d.add_to_dic_threads(3000)
#print(z)
#print(-(y-time.time()))