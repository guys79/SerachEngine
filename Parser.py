class Parser:
    hash_of_words = None

    # The constructor of the class
    def __init__(self):
        self.hash_of_words = {}# Maybe add a function that reads a data from a file (if we have already parsed before)
        return

    # This function will receive a text and will return the text after parse using set of rules
    def parseWord(self,text):
        newText=text
        return newText



    # This function will convert the number term to the wanted state as stated in the assignment
    def convert_number_to_wanted_state(self,term):
        num = self.parseNumber(term)
        if '/' in str(num):
            return num
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

            if end_of[-2:] == 'bn' or end_of[-3:] == ' bn':
                return 'B'
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
        if '/' in number:
            return number
        new_number = float(number)
        return new_number


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

    # This function will handle a word regard to small and big letters and adds the word the the dictionary
    def word_scan(self,word):
        upper_word = word.upper()
        numer_of_app = 0
        if len(word)>0 and word[0]>='A' and word[0]<='Z':
            if upper_word in self.hash_of_words:
                numer_of_app = self.hash_of_words[upper_word]
            self.hash_of_words[upper_word] = numer_of_app + 1
        elif len(word)>0 and word[0]>='a' and word[0]<='z':
            lower_word = word.lower()
            if lower_word in self.hash_of_words:
                numer_of_app = self.hash_of_words[lower_word]
            elif upper_word in self.hash_of_words:
                numer_of_app = self.hash_of_words[upper_word]
                del self.hash_of_words[upper_word]
            self.hash_of_words[lower_word] = numer_of_app + 1
        else:
            self.hash_of_words[upper_word] = numer_of_app + 1

    # This function will parse the percentage term
    def percentage_number_parsing(self, percent_term):
        length = len(percent_term)
        num = None
        if percent_term[length -1] == '%':
            if percent_term[length -2] == ' ':
                num = self.convert_number_to_wanted_state(percent_term[:-2])
            else:
                num = self.convert_number_to_wanted_state(percent_term[:-1])
        elif percent_term[-8:].lower() == ' percent':
            num = self.convert_number_to_wanted_state(percent_term[:-8])
        elif percent_term[-11:].lower() == ' percentage':
            num = self.convert_number_to_wanted_state(percent_term[:-11])
        return '%s%s' % (num,'%')

    # This function will parse a price number term like $12000000000 to 12000 M dollars
    def price_number_parsing(self,price_term):
        length = len(price_term)
        term_fo_dollars = 'Dollars'
        if length == 0:
            return None
        if price_term[0] == '$':
            num = price_term[1:]
        elif price_term[-12:].lower() == 'u.s. dollars':
            num = price_term[:-13]
        elif price_term[-11:].lower() == 'u.s. dollar':
            num = price_term[:-12]
        elif price_term[-7:].lower() == 'dollars':
            num = price_term[:-8]
        else: # dollar
            print(price_term[-7:])
            num = price_term[:-7]
        num = self.parseNumber(num)
        if '/' in str(num):
            return "%s %s" % (num,term_fo_dollars)
        if num >= 1000000:
            return "%s M %s" % (self.curve_around_the_edges(num / (1000 ** 2)), term_fo_dollars)
        return "%s %s" % (self.curve_around_the_edges(num), term_fo_dollars)


    def monthToNum(self,NameOfMonth):
        return {
            'Jan': 1,'Feb': 2,'Mar': 3,'Apr': 4,'May': 5,'Jun': 6,'Jul': 7,'Aug': 8,'Sep': 9,'Oct': 10,'Nov': 11,'Dec': 12,
            'jan': 1,'feb': 2,'mar': 3,'apr': 4,'may': 5,'jun': 6,'jul': 7,'aug': 8,'sep': 9,'oct': 10,'nov': 11,'dec': 12,
            'JAN': 1,'FEB': 2,'MAR': 3,'APR': 4,'MAY': 5,'JUN': 6,'JUL': 7,'AUG': 8,'SEP': 9,'OCT': 10,'NOV': 11,'DEC': 12,
            'January': 1,'February': 2,'March': 3,'April': 4,'May': 5,'June': 6,'July': 7,'August': 8,'September': 9,'October': 10,'November': 11,'December': 12,
            'january': 1,'february': 2,'march': 3,'april': 4,'may': 5,'june': 6,'july': 7,'august': 8,'september': 9,'october': 10,'november': 11,'december': 12,
            'JANUARY': 1,'FEBRUARY': 2,'MARCH': 3,'APRIL': 4,'MAY': 5,'JUNE': 6,'JULY': 7,'AUGUST': 8,'SEPTEMBER': 9,'OCTOBER': 10,'NOVEMBER': 11,'DECEMBER': 12
        }[NameOfMonth]

    def date(self,term):
        newTerm= term.split()
        if "1" in newTerm[0] or "2" in newTerm[0] or "3" in newTerm[0] or "4" in newTerm[0] or "5" in newTerm[0] or "6" in newTerm[0] or "7" in newTerm[0] or "8" in newTerm[0] or "9" in newTerm[0]:
            month=self.monthToNum(newTerm[1])
            day=newTerm[0]
        else:
            month=self.monthToNum(newTerm[0])
            day=newTerm[1]
        month=str(month)
        if len(month)<2:
            month="0"+month
        if len(day)<2:
            day="0"+day
        if int(day)<32:
            return month + "-" + day
        return day + "-" + month
