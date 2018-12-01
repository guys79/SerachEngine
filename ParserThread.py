import threading

class ParserThread (threading.Thread):
    queue_of_result = None
    parser = None
    list_of_texts = ""


    # The constructor of the class
    def __init__(self,queue_of_results,parser,list_of_texts):
        threading.Thread.__init__(self)
        self.parser = parser
        self.queue_of_result = queue_of_results
        self.list_of_texts = list_of_texts



    def run(self):
        self.consume()

    def consume(self):
        for i in range(0,len(self.list_of_texts)):
            print("parser %d"% i)
            dictionary_of_words, dictionary_of_unique_terms, max_freq = self.parser.parse_to_unique_terms(self.list_of_texts[i][0])
            self.queue_of_result.put((dictionary_of_words,dictionary_of_unique_terms,max_freq,self.list_of_texts[i][1]))










