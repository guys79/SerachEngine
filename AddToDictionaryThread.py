import threading
class AddToDictionaryThread (threading.Thread):
    queue_of_result = None
    number_of_docs = -1
    main_dictionary = None
    file_read = None


    # The constructor of the class
    def __init__(self,queue_of_results,number_of_docs,file_read,main_dictionary):
        threading.Thread.__init__(self)
        self.queue_of_result = queue_of_results
        self.number_of_docs = number_of_docs
        self.main_dictionary = main_dictionary
        self.file_read = file_read



    def run(self):
        self.consume()

    def consume(self):
        for i in range(0,self.number_of_docs-1):
            print("add to dictionary %d" % i)
            item = self.queue_of_result.get()
            print("the king")
            self.process(item[0],item[1],item[2],item[3])
            self.queue_of_result.task_done()

    def process(self,dictionary_of_words,dictionary_of_unique_terms,max_freq,doc_num):
        self.add_to_main_dictionary_spacial(dictionary_of_unique_terms)
        self.add_to_dicts(dictionary_of_words)
        self.file_read.add_to_max_values_dict(max_freq, doc_num)



    def add_to_main_dictionary_spacial(self,dict):
        for key in dict:
            if key in self.main_dictionary:
                self.main_dictionary[key] = self.main_dictionary[key] + dict[key]
            else:
                self.main_dictionary[key]=dict[key]

    def add_to_dicts(self,dictionary_of_words):
        for key in dictionary_of_words:
            self.add_term_to_dictionary(key, dictionary_of_words[key])



    # This function will add a term to the dictionary
    def add_term_to_dictionary(self,term,count):
        # If the term is already in the dictionary
        if term in self.main_dictionary:
            self.main_dictionary[term] = self.main_dictionary[term] + count
            return
