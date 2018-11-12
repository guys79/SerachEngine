# This class will save the stop words in a list so we can access the list fast
class StopWordsHolder:
    list_of_stop_words = [] # this list will contain all the stop words

     # The constructor will initialize the list with the stop words
    def __init__(self):
        try:
            file = open("stop_words.txt","r")
        except:
            file = None
        print file

        with file:
            lines = file.readlines()
            self.list_of_stop_words = [line.rstrip('\n') for line in lines]
            file.close()
    # This function will return true if the word i9s a stop word
    def is_stop_word(self,word):
        return word.lower() in self.list_of_stop_words








#x = StopWordsHolder()
#print x.is_stop_word("and")
#print x.is_stop_word("aNd")
#print x.is_stop_word("between")
#print x.is_stop_word("is")
#print x.is_stop_word("i am")
#print x.is_stop_word("i'm")
