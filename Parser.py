class Parser:
    # The constructor of the class
    def __init__(self):
        return

    # This function will receive a text and will return the text after parse using set of rules
    def parseWord(self,text):
        newText=text
        return newText

    def convert_number_to_wanted_state(self,term):
        num = self.parseNumber(term)
        if num < 1000:
            return self.curve_around_the_edges(num)
        if num < 1000 ** 2:
            return "%s%s" % (self.curve_around_the_edges(num /1000),'K')
        if num < 1000 ** 3:
            return "%s%s" % (self.curve_around_the_edges(num /(1000 ** 2)),'M')
        #if num < 1000 ** 4:
        return "%s%s" % (self.curve_around_the_edges(num /(1000 ** 3)),'B')
        #if num < 1000 ** 5:
        #    return "%s%s" % (self.curve_around_the_edges(num /(1000 ** 4)),'T')
       # return "%s%s" % (self.curve_around_the_edges(num /(1000 ** 5)),'Q')

    # This function will change numbers like 180.000 to 180
    def curve_around_the_edges(self,number):
        num_in_string = str(number)
        index = num_in_string.find('.')
        if index == -1:
            return num_in_string
        i = len(num_in_string) - 1
        while num_in_string[i] == '0':
            num_in_string = num_in_string[:-1]
            i = i -1
        if num_in_string[i] == '.':
            num_in_string = num_in_string[:-1]
        return num_in_string



    # This function will return a number after being parsed
    def parseNumber(self,term):
        kind = self.numberKind(term)
        return self.irregular_case_handler(term, kind)

    # This function will return the right shortcut to the right expression
    # For example, 188000 Thousands will return K
    # and "regular" otherwise
    def numberKind(self,term):
        try:
            float(term)
            return 'regular'
        except Exception:
            if term[len(term)-1] == 'k' or term[len(term)-1] == 'K':
                return 'K'
            if term[len(term)-1] == 'm' or term[len(term)-1] == 'M':
                return 'M'
            if term[len(term)-1] == 'b' or term[len(term)-1] == 'B':
                return 'B'
            if term[len(term)-1] == 't' or term[len(term)-1] == 'T':
                return 'T'
            if term[len(term)-1] == 'q' or term[len(term)-1] == 'Q':
                return 'Q'

            end_of = term.lower()

            if len(term) > 8 and (end_of[-8:] == 'thousand' or end_of[-9:] == 'thousands'):
                return 'K'
            if len(term) > 7 and (end_of[-7:] == 'million' or end_of[-8:] == 'millions'):
                return 'M'
            if len(term) > 7 and (end_of[-7:] == 'billion' or end_of[-8:] == 'billions'):
                return 'B'
            if len(term) > 8 and (end_of[-8:] == 'trillion' or end_of[-9:] == 'trillions'):
                return 'T'
            if len(term) > 7 and (end_of[-11:] == 'quadrillion' or end_of[-12:] == 'quadrillions'):
                return 'Q'

           # number_of_commas = self.number_of_commas(term)

           # if number_of_commas == 1:
            #     return 'K'
                # if number_of_commas == 2:
            #return 'M'
                #if number_of_commas == 3:
            #return 'B'
                #if number_of_commas == 4:
            #return 'T'
                #if number_of_commas == 5:
            #return 'Q'

            return 'regular'

    # This function will parse a number like 100,000 or 0.566
    def number_case_handler(self, number):
        number = number.replace(',', '')
        number = float(number)
        return number


    # This function will parse a number in it's irregular form
    def irregular_case_handler(self, number,kind):
        if kind == 'regular':
            return self.number_case_handler(number)
        multi = 1
        if kind == 'M':
            multi = 2
        elif kind == 'B':
            multi = 3
        elif kind == 'T':
            multi = 4
        elif kind == 'Q':
            multi = 5
        return float(self.number_without_extra_content(number)) * (1000 ** multi)



    # This function will return the number of commas (',') in a string
    def number_of_commas(self,term):
        return term.count(',')

    def number_without_extra_content(self,number):
        new_number = ''
        i = 0
        length = len(number)
        while i < length and ((number[i] >= '0' and number[i] <= '9') or number[i] == ',' or number[i] == '.'):
            new_number = new_number + number[i]
            i = i + 1
        return self.number_case_handler(new_number)




