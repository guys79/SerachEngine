class Parser:
    # The constructor of the class
    def __init__(self):
        return

    # This function will receive a text and will return the text after parse using set of rules
    def parseWord(self,text):
        newText=text
        return newText

    # This function will return a number after being parsed
    def parseNumber(self,term):

        return

    #This function will return "K" if the number is in the range of 1000-999,999
    #,"M" if the number is in the range of 1,000,000-999,999,999, "B" if th number is in range of 1,000,000,000-999,999,999,999, and "regular" otherwise
    def numberKind(self,term):
        try:
            num = int(term)
            return 'regular'
        except Exception:

            if term[len(term)-1] == 'k' or term[len(term)-1] == 'K':
                return 'K'
            if term[len(term)-1] == 'm' or term[len(term)-1] == 'M':
                return 'M'
            if term[len(term)-1] == 'b' or term[len(term)-1] == 'B':
                return 'B'
            if len(term) > 8 and term[-8:].lower() == 'thousand':
                return 'K'
            if len(term) > 7 and term[-7:].lower() == 'million':
                return 'M'
            if len(term) > 7 and term[-7:].lower() == 'billion':
                return 'B'
            number_of_commas = self.number_of_commas(term)

            if number_of_commas == 1:
                return 'K'
            if number_of_commas == 2:
                return 'M'
            if number_of_commas == 3:
                return 'B'

            return 'regular'

    # This function will parse a number in it's regular form
    def regular_case_handler(self,number):
        return

    # This function will parse a number in it's irregular form
    def irregular_case_handler(self,number):
        return





    def number_of_commas(self,term):
        return term.count(',')


