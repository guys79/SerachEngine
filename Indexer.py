import os
from Parser import Parser
from ReadFile import ReadFile

# This class will index all the terms in the collection
class Indexer:
    name_of_files = None # The names of the initial posting files
    file_type = None # The file type of the posting files
    parser = None # The parser of the project
    read_file = None # The ReadFile of the class
    main_dictionary = None
    empty_semaphores = None

    # The constructor of the class
    def __init__(self, corpus_file_path):
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
        end = "<" + tag + "/>"
        string = string[string.find(start) + len(start):string.find(end)]
        return string














f = Indexer('C:\Users\guys79\Desktop\corpus')
f.add_term_to_dictionary("guy")
f.add_term_to_dictionary("GUY")
f.add_term_to_dictionary("GUY")
f.add_term_to_dictionary("UY")
f.add_term_to_dictionary("uy")
f.add_term_to_dictionary("uy")
f.add_term_to_dictionary("0ss")
f.add_term_to_dictionary("guyss")
f.add_term_to_dictionary("GUYSS")
f.add_term_to_dictionary("guyss")
print(f.main_dictionary)




