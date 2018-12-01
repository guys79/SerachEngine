from StopWordsHolder import *
from string import *
import math
from nltk.stem import PorterStemmer
class Parser:

    stopWordsHolder = None
    porter_stemmer = None

    # The constructor of the class
    def __init__(self):
        self.stopWordsHolder = StopWordsHolder()
        self.porter_stemmer = PorterStemmer()

    # Adding a list of words to the dictionary
    def scan_list_of_word(self,list_words):
        dictionary = {}
        for i in range(0,len(list_words)):
            self.word_scan(list_words[i],dictionary)
        return dictionary

    # This function will convert the number term to the wanted state as stated in the assignment
    def convert_number_to_wanted_state(self,term):
        try:
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
        except Exception:
            return None

    # This function will change numbers like 180.000 to 180
    def curve_around_the_edges(self,number):
        num_in_string = str(number)
        index = num_in_string.find('.')
        if index == -1:
            return num_in_string
        if len(num_in_string)-index>3:
            if num_in_string[index+3]>='5':
                return num_in_string[:index+2]+chr(ord(num_in_string[index+2])+1)
            return num_in_string[:index + 3]
        return num_in_string

    # This function will return the maximum frequency of a certain ter in two dictionaries
    def max_frequency(self,dictionary, dictionary_of_unique_terms):
        max_freq = 0
        # For the first dictioanary
        for key in dictionary:
            if max_freq < dictionary[key]:
                max_freq = dictionary[key]
        for key in dictionary_of_unique_terms:
            if max_freq < dictionary_of_unique_terms[key]:
                max_freq = dictionary_of_unique_terms[key]
        return max_freq

    # This function ill add a term to the dictionary
    def add_to_term_dic(self,dictionary_of_unique_terms,key):
        if key in dictionary_of_unique_terms:
            dictionary_of_unique_terms[key] = dictionary_of_unique_terms[key] + 1
            return
        dictionary_of_unique_terms[key] = 1

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

    # This function removes anything that is not a digit or , or . from the string
    def number_without_extra_content(self,number):
        new_number = ''
        i = 0
        length = len(number)
        while i < length and ((number[i] >= '0' and number[i] <= '9') or number[i] == ',' or number[i] == '.'):
            new_number = new_number + number[i]
            i = i + 1
        return self.number_case_handler(new_number)

    # This function will handle a word regard to small and big letters and adds the word the the dictionary
    def word_scan(self,word,dictionary):
        flag = len(word) > 0 and word[0] >= 'A' and word[0] <= 'Z'
        try:
            word = self.porter_stemmer.stem(word).encode("ascii")
        except UnicodeDecodeError:
            1
        upper_word = word.upper()
        numer_of_app = 0
        if flag:
            if upper_word in dictionary:
                numer_of_app = dictionary[upper_word]
            dictionary[upper_word] = numer_of_app + 1
        elif len(word)>0 and word[0]>='a' and word[0]<='z':
            lower_word = word.lower()
            if lower_word in dictionary:
                numer_of_app = dictionary[lower_word]
            elif upper_word in dictionary:
                numer_of_app = dictionary[upper_word]
                del dictionary[upper_word]
            dictionary[lower_word] = numer_of_app + 1

        else:
            dictionary[upper_word] = numer_of_app + 1

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
            num = price_term[:-7]
        num = self.parseNumber(num)
        if '/' in str(num):
            return "%s %s" % (num,term_fo_dollars)
        if num >= 1000000:
            return "%s M %s" % (self.curve_around_the_edges(num / (1000 ** 2)), term_fo_dollars)
        return "%s %s" % (self.curve_around_the_edges(num), term_fo_dollars)

    # This function will return the number of the given month term
    def monthToNum(self,NameOfMonth):
        try:
            return {
                'jan': 1,'feb': 2,'mar': 3,'apr': 4,'may': 5,'jun': 6,'jul': 7,'aug': 8,'sep': 9,'oct': 10,'nov': 11,'dec': 12,
                'january': 1,'february': 2,'march': 3,'april': 4,'may': 5,'june': 6,'july': 7,'august': 8,'september': 9,'october': 10,'november': 11,'december': 12
            }[NameOfMonth]
        except Exception:
            return None

    # returns a date from the kind of mm/dd or mm/yy depends on the given term
    def date(self, term):
        term = term.lower()
        newTerm = term.split(' ')
        if self.is_integer(newTerm[0]):
            month = self.monthToNum(newTerm[1])
            if month == "it is not a month":
                return month
            day = newTerm[0]
        else:
            month = self.monthToNum(newTerm[0])
            day = newTerm[1]
        month = str(month)
        if len(month) < 2:
            month = "0" + month
        if len(day) < 2:
            day = "0" + day
        if int(day) < 32:
            return month + "-" + day
        return day + "-" + month

    # This function will return True if the string is an integer
    def is_integer(self,number):
        try:
            int(number)
            return True
        except Exception:
            return False

    # This function will return True if the string is a float
    def is_float(self,number):
        try:
            float(number)
            return True
        except Exception:
            return False

    # This function will get a range parameter and will parse it
    def range_term_parser(self,range_term):
        # number of - in the term
        number_of_hyphens = range_term.count('-')

        # If the term is word-word-word
        if number_of_hyphens == 2:
            return [range_term]

        first_half = ''
        second_half = ''
        # if the term is 'Between number and number'
        if number_of_hyphens == 0:
            end_of_ex = range_term[8:]
            index = end_of_ex.find(' and')
            if index == -1:
                index = end_of_ex.find(' to')
                first_half = end_of_ex[: index]
                second_half = end_of_ex[end_of_ex.find(' to') + 4:]
            else:
                first_half = end_of_ex[: index]
                second_half = end_of_ex[end_of_ex.find(' and') + 5:]

        # if the term is word-word or word-number or number-word or number-number
        elif number_of_hyphens == 1:
            index = range_term.find('-')
            first_half = range_term[:index]
            second_half = range_term[index + 1:]

        list_to_return = []
        temp = self.convert_number_to_wanted_state(first_half)
        if temp != None:
            first_half = temp
            list_to_return.append(first_half)

        temp = self.convert_number_to_wanted_state(second_half)
        if temp != None:
            second_half = temp
            list_to_return.append(second_half)
        list_to_return.append('%s-%s' % (first_half,second_half))
        return list_to_return

    # This function will get the String that will represent the doc
    # and will Parse it
    def parse_doc(self,doc_text):
        temp_text = doc_text

    # this function should return DD-MM-YY format for all the formats of how to write full date
    def full_date(self, term):
        # we check if the date is from the from of dd/mm/yy
        if "/" in term:
            newTerm = term.split("/")
            # we check correction
            if self.is_integer(newTerm[0]) == False or self.is_integer(newTerm[1]) == False or self.is_integer(
                    newTerm[2]) == False:
                return term
            # we check if we can identify if the string id dd/mm/yy or mm/dd/yy
            if (newTerm[0] > 12 or newTerm[1] > 12) and len(newTerm[2]) > 1:
                if int(newTerm[1]) > 12:
                    temp = newTerm[1]
                    newTerm[1] = newTerm[0]
                    newTerm[0] = temp
                if len(newTerm[1]) == 1:
                    newTerm[1] = "0" + newTerm[1]
                arrayOfDates = []
                day = newTerm[0]
                month = newTerm[1]
                year = newTerm[2]
                if len(year) > 2:
                    arrayOfDates.append(year)
                    if len(year) == 3:
                        year = year[1:]
                    else:
                        year = year[2:]
                arrayOfDates.append(day + "-" + month + "-" + year)
                arrayOfDates.append(day + "-" + month)
                return arrayOfDates
            return term
        # we check if the format is written in words
        else:
            val = term
            term = term.lower()
            term = term.replace("th", "")
            term = term.replace(",", "")
            newTerm = term.split(' ')
            if len(newTerm) < 3:
                return val
            if self.is_integer(newTerm[1]):
                temp = newTerm[1]
                newTerm[1] = newTerm[0]
                newTerm[0] = temp
            day = self.date(newTerm[0] + " " + newTerm[1])
            if day == "it is not a month":
                return val
            year = self.date(newTerm[1] + " " + newTerm[2])
            day = day[3:]
            year = year.split("-")
            month = year[1]
            year = year[0]
            arrayOfDates = []
            if len(year) > 2:
              arrayOfDates.append(year)
            if len(year) == 3:
                year = year[1:]
            else:
                year = year[2:]
            arrayOfDates.append(day + "-" + month + "-" + year)
            arrayOfDates.append(day + "-" + month)
            return arrayOfDates
            return day + "-" + month + "-" + year



    # This is the mother of all functions.
    # The function will get a text as a long string and will return 3 parameters:
    # First dictionary - The dictionary of all the words in the text.
    # Second dictionary - The dictionary with all the unique terms
    # Max frequency - The frequency of the term that appear most number of times in the text
    def parse_to_unique_terms(self,text):
        index = -1  # The index of the current closest space
        dictionary_of_unique_terms = {}  # The new doc
        current_term = ''  # The current term
        next_term = ''  # The next term
        more_words = index != -1
        additional_word = ''
        text = ' '.join(text.split())
        exclude = set(punctuation)
        exclude.remove('/')
        exclude.remove('-')
        text = ''.join(ch for ch in text if ch not in exclude)
        # Do while index != -1
        while True:

            #print("text = %s" % text)
            #print("dictionary_of_unique_terms = %s" % dictionary_of_unique_terms)
            index = text.find(' ')
            more_words = index != -1
            # Get the current term and it's length, shorten the doc and find the next space
            if not more_words:
                current_term = text
            else:
                current_term = text[0:index]
            text = text[index + 1:]
            index = text.find(' ')
            length = len(current_term)
            if length == 0:
                if len(text) == 0:
                    break
                continue
            if self.is_integer_that_ends_with_th(current_term):
                current_term = current_term[:-2]
            # If the term is a number
            if self.is_number_term(current_term):
                # If there are no more terms
                if not more_words:
                    # Is just a number
                    self.add_to_term_dic(dictionary_of_unique_terms,self.convert_number_to_wanted_state(current_term))
                    break

                more_words_save = more_words
                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = text
                else:
                    next_term = text[0:index]
                text = text[index + 1:]


                if self.is_fraction(current_term):
                    if more_words:
                        text = next_term + " "+text
                    more_words = more_words_save
                    next_term = current_term
                    current_term = "0"


                # If the term is an integer
                if self.is_integer(current_term):
                    if int(current_term).__abs__() < 1000:
                        # If the number is a fraction
                        if len(next_term) !=0 and (self.is_fraction(next_term) or (
                                (next_term[len(next_term) - 1] == '%') and self.is_fraction(next_term[:-1]))):

                            flag = next_term[len(next_term) - 1] == '%'
                            current_term = current_term + " " + next_term
                            index = text.find(' ')

                            # If there are no more terms
                            if not more_words:
                                # Is just a number or percent like this 22 3/4%
                                if flag:
                                    self.add_to_term_dic(dictionary_of_unique_terms,self.percentage_number_parsing(current_term))
                                else:
                                    self.add_to_term_dic(dictionary_of_unique_terms,self.convert_number_to_wanted_state(current_term))
                                break

                            # If there are more terms
                            more_words = index != -1
                            if not more_words:
                                next_term = text
                            else:
                                next_term = text[0:index]
                            text = text[index + 1:]

                            lower = next_term.lower()
                            # If it's a price term
                            if lower == 'dollars' or lower == 'dollar':
                                current_term = current_term + " " + next_term
                                self.add_to_term_dic(dictionary_of_unique_terms,self.price_number_parsing(current_term))
                                if not more_words:
                                    break
                                continue
                            # If it's a percent term
                            if lower == 'percent' or lower == 'percentage':
                                current_term = current_term + " " + next_term
                                self.add_to_term_dic(dictionary_of_unique_terms,self.percentage_number_parsing(current_term))
                                if not more_words:
                                    break
                                continue

                            if self.is_weight_measurement(lower):
                                current_term = current_term + " " + next_term
                                self.add_to_term_dic(dictionary_of_unique_terms,
                                                     self.convert_to_kg(current_term))
                                if not more_words:
                                    break
                                continue

                            text = next_term + " " + text
                            self.add_to_term_dic(dictionary_of_unique_terms,self.convert_number_to_wanted_state(current_term))
                            continue

                        # This is an integer smaller than 1000 and without a fraction
                        # We will check is it is a date
                        if int(current_term) <= 31 and int(current_term) >= 1:
                            if self.monthToNum(next_term.lower()) != None:
                                current_term = current_term + " " + next_term
                                # If there are no more terms
                                if not more_words:
                                    # It is a date like 20 March
                                    self.add_to_term_dic(dictionary_of_unique_terms,self.date(current_term))
                                    break

                                index = text.find(' ')
                                # If there are more terms
                                more_words = index != -1
                                if not more_words:
                                    next_term = text
                                else:
                                    next_term = text[0:index]
                                text = text[index + 1:]

                                # Than it is a full date
                                if self.is_integer(next_term) and int(next_term) <= 2500:
                                    current_term = current_term + " " + next_term
                                    self.combine_list_and_dictionary(dictionary_of_unique_terms,self.full_date(current_term))
                                    if not more_words:
                                        break
                                    continue
                                text = next_term + " " +text
                                self.add_to_term_dic(dictionary_of_unique_terms,
                                                     self.date(current_term))
                                continue

                    lower = next_term.lower()
                    # If it's a price term
                    if lower == 'dollars' or lower == 'dollar':
                        current_term = current_term + " " + next_term
                        self.add_to_term_dic(dictionary_of_unique_terms, self.price_number_parsing(current_term))
                        if not more_words:
                            break
                        continue
                    # If it's a percent term
                    if lower == 'percent' or lower == 'percentage':
                        current_term = current_term + " " + next_term
                        self.add_to_term_dic(dictionary_of_unique_terms, self.percentage_number_parsing(current_term))
                        if not more_words:
                            break
                        continue

                    if self.is_weight_measurement(lower):
                        current_term = current_term + " " + next_term
                        self.add_to_term_dic(dictionary_of_unique_terms,
                                             self.convert_to_kg(current_term))
                        if not more_words:
                            break
                        continue

                # The term is a number that is not an integer or that it's absolute value is not smaller
                # than 1000 or not one of the checks above
                hyphen_index = next_term.find('-')
                flag = hyphen_index != -1 and self.is_number_describer(next_term[:hyphen_index])
                if self.is_number_describer(next_term) or flag:
                    current_term = current_term + " " + next_term

                index = text.find(' ')
                # If the range is like 13 thousand-..
                if flag:
                    # If the range is like 13 thousand-34.7 ..
                    if self.is_float(next_term[hyphen_index + 1:]):
                        # If the range is like 13 thousand-34.7
                        if not more_words:
                            self.combine_list_and_dictionary(dictionary_of_unique_terms, self.range_term_parser(current_term))
                            break

                        # If there are more terms
                        more_words = index != -1
                        if not more_words:
                            next_term = text
                        else:
                            next_term = text[0:index]
                        text = text[index + 1:]

                        # If the range is like 13 thousand-34.7 million

                        if self.is_number_describer(next_term) or self.is_fraction(next_term):
                            current_term = current_term +" "+ next_term
                            self.combine_list_and_dictionary(dictionary_of_unique_terms, self.range_term_parser(current_term))
                            if not more_words:
                                break
                            continue
                        text = next_term + " " +text


                    else:
                        self.combine_list_and_dictionary(dictionary_of_unique_terms, self.range_term_parser(current_term))
                        if not more_words:
                            break
                        continue
                else:
                    # If there are no more terms it must be a number
                    if not more_words:
                        self.add_to_term_dic(dictionary_of_unique_terms,self.convert_number_to_wanted_state(current_term))
                        break
                    if more_words:
                        text = next_term + " "+text
                        index= len(next_term)


                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = text
                    else:
                        next_term = text[0:index]
                    text = text[index + 1:]

                    lower = next_term.lower()
                    if lower == 'percent' or lower == 'percentage':
                        current_term = current_term + " " + next_term
                        self.add_to_term_dic(dictionary_of_unique_terms,self.percentage_number_parsing(current_term))
                        if not more_words:
                            break
                        continue

                    if lower == 'dollar' or lower == 'dollars':
                        current_term = current_term + " " + next_term
                        self.add_to_term_dic(dictionary_of_unique_terms,self.price_number_parsing(current_term))
                        if not more_words:
                            break
                        continue


                    if self.is_weight_measurement(lower):
                        current_term = current_term + " " + next_term

                        self.add_to_term_dic(dictionary_of_unique_terms, self.convert_to_kg(current_term))
                        if not more_words:
                            break
                        continue

                    if lower == 'u.s.':
                        temp = next_term
                        if not more_words:
                            self.add_to_term_dic(dictionary_of_unique_terms,self.convert_number_to_wanted_state(current_term))
                            self.add_to_term_dic(dictionary_of_unique_terms,next_term)
                            break
                        index = text.find(' ')
                        # If there are more terms
                        more_words = index != -1
                        if not more_words:
                            next_term = text
                        else:
                            next_term = text[0:index]
                        text = text[index + 1:]
                        lower = next_term.lower()
                        if lower == 'dollar' or lower == 'dollars':
                            current_term = current_term + " " + temp + " " + next_term
                            self.add_to_term_dic(dictionary_of_unique_terms,self.price_number_parsing(current_term))
                            if not more_words:
                               break
                            continue

                    self.add_to_term_dic(dictionary_of_unique_terms,self.convert_number_to_wanted_state(current_term))
                    text = next_term + " " + text
                    continue
            # If the term is not an integer
            # if the tern starts with $
            if current_term[0] == '$':
                if self.is_number_term(current_term[1:]):
                    if current_term[len(current_term) - 1].lower() in ['k', 'm', 'b', 't', 'q']:
                        self.add_to_term_dic(dictionary_of_unique_terms,self.price_number_parsing(current_term))
                        continue

                    if not more_words:
                        self.add_to_term_dic(dictionary_of_unique_terms,self.price_number_parsing(current_term))
                        break

                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = text
                    else:
                        next_term = text[0:index]
                    text = text[index + 1:]

                    if self.is_number_describer(next_term):
                        current_term = current_term + " " + next_term

                    self.add_to_term_dic(dictionary_of_unique_terms,self.price_number_parsing(current_term))
                    if not more_words:
                       break
                    continue

            # If the curret term starts with the word between
            if current_term.lower() == "between":

                so_far = ''
                if not more_words:
                    self.add_to_term_dic(dictionary_of_unique_terms,current_term)
                    break

                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = text
                else:
                    next_term = text[0:index]
                text = text[index + 1:]

                so_far = next_term
                if not self.is_number_term(next_term) or not more_words:
                    if more_words:
                        text = so_far + " " + text
                    else:
                        text = so_far
                    self.add_to_term_dic(dictionary_of_unique_terms,current_term)
                    continue

                index = text.find(' ')
                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = text
                else:
                    next_term = text[0:index]
                text = text[index + 1:]

                if self.is_number_describer(next_term):
                    so_far = so_far + " " + next_term
                    index = text.find(' ')
                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = text
                    else:
                        next_term = text[0:index]
                    text = text[index + 1:]

                so_far = so_far + " " + next_term
                if (next_term.lower() != "and" and next_term.lower() != "to") or not more_words:
                    if more_words:
                        text = so_far + " " + text
                    else:
                        text = so_far
                    self.add_to_term_dic(dictionary_of_unique_terms,current_term)
                    continue
                index = text.find(' ')
                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = text
                else:
                    next_term = text[0:index]
                text = text[index + 1:]

                so_far = so_far + " " + next_term
                if not self.is_number_term(next_term):
                    if more_words:
                        text = so_far + " " + text
                    else:
                        text = so_far
                    self.add_to_term_dic(dictionary_of_unique_terms,current_term)
                    continue

                if more_words:
                    index = text.find(' ')
                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = text
                    else:
                        next_term = text[0:index]
                    text = text[index + 1:]
                    if self.is_number_describer(next_term):
                        so_far = so_far + " " + next_term
                    else:
                        if more_words:
                            text = next_term + " "+text
                        else:
                            text = next_term
                        more_words = True


                current_term = current_term + " " + so_far

                self.combine_list_and_dictionary(dictionary_of_unique_terms, self.range_term_parser(current_term))
                if not more_words:
                   break
                continue

            # if the term is a term for month
            if self.monthToNum(current_term.lower())!= None:
                if not more_words:
                    self.add_to_term_dic(dictionary_of_unique_terms,next_term)
                    break

                index = text.find(' ')
                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = text
                else:
                    next_term = text[0:index]
                text = text[index + 1:]


                flag1 = self.is_integer(next_term)
                flag2 = self.is_integer_that_ends_with_th(next_term)
                flag3 = len(next_term)!=0 and (self.is_integer_that_ends_with_th(next_term[:-1]) and next_term[len(next_term) - 1] == ',')
                flag4 = len(next_term)!=0 and (self.is_integer(next_term[:-1]) and next_term[len(next_term)-1] == ',')
                if flag2 or flag1 or flag3 or flag4:

                    day = next_term
                    flag = True

                    if flag2:
                        day = next_term[:-2]
                    if flag3:
                        day = next_term[:-3]
                    if flag4:
                        day = next_term[:-1]

                    flag = int(day) <= 31 and int(day) >= 0
                    current_term = current_term + " " + day
                    if not flag or not more_words:
                        self.add_to_term_dic(dictionary_of_unique_terms,self.date(current_term))
                        if not more_words:
                           break
                        continue

                    index = text.find(' ')
                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = text
                    else:
                        next_term = text[0:index]
                    text = text[index + 1:]

                    if not self.is_integer(next_term):
                        text = next_term
                        self.combine_list_and_dictionary(dictionary_of_unique_terms,self.full_date(current_term))
                        continue

                    current_term = current_term + " " + next_term
                    self.combine_list_and_dictionary(dictionary_of_unique_terms,self.full_date(current_term))
                    if not more_words:
                       break
                    continue
            # If the term is a term for a full date
            if self.is_date(current_term):
                self.combine_list_and_dictionary(dictionary_of_unique_terms,self.full_date(current_term))
                if not more_words:
                   break
                continue


            # If the term is a type of range term
            if self.is_word_number(current_term):
                if not more_words:
                    self.combine_list_and_dictionary(dictionary_of_unique_terms,self.range_term_parser(current_term))
                    break

                index = text.find(' ')
                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = text
                else:
                    next_term = text[0:index]
                text = text[index + 1:]

                if self.is_number_describer(next_term) or self.is_fraction(next_term):
                    current_term = current_term + " "+ next_term
                    self.combine_list_and_dictionary(dictionary_of_unique_terms, self.range_term_parser(current_term))
                    if not more_words:
                       break
                    continue

                text = next_term +" " + text

            number_of_hyphens = current_term.count('-')
            # If it's word-word or word-word-word
            if number_of_hyphens == 1 or number_of_hyphens == 2:
                self.combine_list_and_dictionary(dictionary_of_unique_terms, self.range_term_parser(current_term))
                if not more_words:
                   break
                continue


            # If the term is not a unique term, add it to the string of words
            additional_word = additional_word +" " + current_term

            if not more_words or text == '':  # Do while index != -1
                break



        additional_word = additional_word[1:]
        # Remove stop words anf punctuations
        additional_word = ''.join(ch for ch in additional_word if ch not in ['-','/'])
        # Removing stop words
        additional_word = self.remove_stop_words(additional_word)
        # Assigning all the words in the text to a dictionary of words
        dictionary_of_words = self.scan_list_of_word(additional_word)
        # getting the frequency of the term that appears most in the text
        max_freq= self.max_frequency(dictionary_of_words,dictionary_of_unique_terms)
        # Returning the dictionary of words, the dictionary of unique term, and the max frequency
        return dictionary_of_words,dictionary_of_unique_terms,max_freq

    # This function will remove the stop words from the string
    def remove_stop_words(self,words):
        words = words.split()
        result = [word for word in words if not self.stopWordsHolder.is_stop_word(word)]
        return result

    # This function will return if the term is a term of range that the second half of the range is a number only ony hyphen)
    def is_word_number(self,term):
        number_of_hyphens = term.count('-')
        if number_of_hyphens != 1:
            return False
        second = term[term.find('-')+1:]
        if len(second) == 0:
            return False
        return self.is_number_term(second)

    # Returns True if the term is a number (like 100,000 and not 10,0,0)
    def is_number(self,term):
        index = term.find('.')
        if index == len(term) - 1:
            return False
        temp = term
        if index != -1:
            temp = temp[:index]
        import re
        indices = [m.start() for m in re.finditer(',', temp)]
        length = len(indices)
        if length > 0:
            if indices[length - 1] != len(temp) - 4:
                return False
            if indices[0] < 1 or indices[0] > 3:
                return False
            for i in range(0, length - 1):
                if indices[i + 1] - indices[i] != 4:
                    return False

        temp = temp.replace(',', '')
        if index != -1:
            temp = temp + term[index:]
        return self.is_float(temp)

    # This function will add a list of terms to the dictionart
    def combine_list_and_dictionary(self,dic, list):
        for i in range(0, len(list)):
            self.add_to_term_dic(dic,list[i])

    # If the term ia=s a term number like 50, 50K and so on
    def is_number_term(self,term):
        length = len(term)
        if len(term) ==0:
            return False
        term = term.lower()
        if self.is_number(term):
            return True
        if term[length - 1] in ['k', 'm', 'b', 't', 'q']:
            return self.is_number(term[:-1])
        if term[-2:] == 'bn':
            return self.is_number(term[:-2])
        return self.is_fraction(term)

    # This function will check if the number is soething like this 14th,30th..
    def is_integer_that_ends_with_th(self,number):
        return number[-2:].lower() == 'th' and self.is_integer(number[:-2])

    # This function will return True if the term is a fraction. like 34 1/3
    def is_fraction(self,term):
        index = term.find('/')
        if index == -1:
            return False
        return self.is_float(term[:index]) and self.is_float(term[index + 1:])

    # This function will return if the string is a discriber of quantity like thousands, millions and so on..
    def is_number_describer(self,word):
        return word.lower() in ['thousand', 'thousands', 'million', 'millions', 'trillions', 'trillion', 'billion',
                                'billions', 'quadrillion', 'quadrillion', 'bn']

    # Ths function returns True if the term si a full date like this 12/3/2016
    def is_date(self,term):
        num_of_slashes = term.count('/')
        if num_of_slashes != 2:
            return False
        index = term.find('/')
        first = term[:index]
        rindex = term.rfind('/')
        second = term[index + 1: rindex]
        third = term[rindex+1:]

        if not (self.is_integer(first) and self.is_integer(second) and self.is_integer(third)):
            return False

        first = int(first)
        second = int(second)
        if not (first >= 1 and second >= 1):
            return False

        return (first <= 31 and second <= 12) or (first <= 12 and second <= 31)

    # this function should return the begining of a weigth. for example:13kg return 2
    def find_the_letter(self, weith):
        place = len(weith)
        weith = weith.lower()
        if weith.find('a') != -1 and weith.find('a') < place:
            place = weith.find('a')
        if weith.find('b') != -1 and weith.find('b') < place:
            place = weith.find('b')
        if weith.find('c') != -1 and weith.find('c') < place:
            place = weith.find('c')
        if weith.find('d') != -1 and weith.find('d') < place:
            place = weith.find('d')
        if weith.find('e') != -1 and weith.find('e') < place:
            place = weith.find('e')
        if weith.find('f') != -1 and weith.find('f') < place:
            place = weith.find('f')
        if weith.find('g') != -1 and weith.find('g') < place:
            place = weith.find('g')
        if weith.find('h') != -1 and weith.find('h') < place:
            place = weith.find('h')
        if weith.find('i') != -1 and weith.find('i') < place:
            place = weith.find('i')
        if weith.find('j') != -1 and weith.find('j') < place:
            place = weith.find('j')
        if weith.find('k') != -1 and weith.find('k') < place:
            place = weith.find('k')
        if weith.find('l') != -1 and weith.find('l') < place:
            place = weith.find('l')
        if weith.find('m') != -1 and weith.find('m') < place:
            place = weith.find('m')
        if weith.find('n') != -1 and weith.find('n') < place:
            place = weith.find('n')
        if weith.find('o') != -1 and weith.find('o') < place:
            place = weith.find('o')
        if weith.find('p') != -1 and weith.find('p') < place:
            place = weith.find('p')
        if weith.find('q') != -1 and weith.find('q') < place:
            place = weith.find('q')
        if weith.find('r') != -1 and weith.find('r') < place:
            place = weith.find('r')
        if weith.find('s') != -1 and weith.find('s') < place:
            place = weith.find('s')
        if weith.find('t') != -1 and weith.find('t') < place:
            place = weith.find('t')
        if weith.find('u') != -1 and weith.find('u') < place:
            place = weith.find('u')
        if weith.find('v') != -1 and weith.find('v') < place:
            place = weith.find('v')
        if weith.find('w') != -1 and weith.find('w') < place:
            place = weith.find('w')
        if weith.find('x') != -1 and weith.find('x') < place:
            place = weith.find('x')
        if weith.find('y') != -1 and weith.find('y') < place:
            place = weith.find('y')
        if weith.find('z') != -1 and weith.find('z') < place:
            place = weith.find('z')
        return place
    # this function shoud give us the number that we neet to mult in in order to get kg
    def how_much_to_mult_for_kg(self, term):
        term = term.lower()
        if term in ["gram","g","grams"]:
            return math.pow(10, - 3)
        if term in ["decagram","dag","decagrams"]:
            return math.pow(10, 1 - 3)
        if term in ["hectogram","hg","hectograms"]:
            return math.pow(10, 2 - 3)
        if term in ["kilogram","kg","kilograms"]:
            return math.pow(10, 3 - 3)
        if term in ["tonne","ton","tons"]:
            return math.pow(10, 6 - 3)
        if term in ["decigram","dg","decigrams"]:
            return math.pow(10, -1 - 3)
        if term in ["centigram","cg","centigrams"]:
            return math.pow(10, -2 - 3)
        if term in ["milligram","mg","milligrams"]:
            return math.pow(10, -3 - 3)

    def is_weight_measurement(self,term):
        return term.lower() in ["gram","g","grams","decagram","dag","decagrams","hectogram","hg","hectograms","kilogram","kg","kilograms","tonne","ton","tons","decigram","dg","decigrams","centigram","cg","centigrams","milligram","mg","milligrams"]
    # convert any measer unit into kg
    def convert_to_kg(self, weigth):
        weigth = self.convert_to_degit_num(weigth)
        place = int(self.find_the_letter(weigth))
        num = weigth[0:place]
        measure_unit = weigth[place:]
        if num == "":
            return measure_unit
        measure_unit = measure_unit.lower()
        measure_unit = self.how_much_to_mult_for_kg(measure_unit)
        num = float(num)
        measure_unit = float(measure_unit)
        num = num * measure_unit
        return self.curve_around_the_edges(self.convert_number_to_wanted_state(str(num))) + " " + "kg"

    # This function will return True if variable is a string
    def is_string(self, str):
        try:
            str = str + ''
        except:
            return False
        return True

    # if we get 200 hundred kg it will return 20000.0kg
    def convert_to_degit_num(self, str):
        arrStr = str.split()
        if len(arrStr)==3 and self.is_fraction(arrStr[1]):
            arrStr = [self.fraction_to_number(arrStr[0],arrStr[1]),arrStr[2]]
        if len(arrStr) == 3:
            arrStr = [(self.parseNumber(arrStr[0] + " " + arrStr[1])), arrStr[2]]
        if len(arrStr) == 2:
            x = arrStr[0]
            if self.is_string(x):
                x = arrStr[0]
            else:
                x = "%f" % x
            weigt = x + (arrStr[1])
            return weigt
        return str

    def fraction_to_number(self,integer,fraction):
        index = fraction.find("/")
        return float(integer)+(float(fraction[:index])/float(fraction[index+1:]))



#x = Parser()
#ng = open("test.txt","r")
#strr = ""
#for line in ng:
#    strr = strr +line
#print(strr)
#dic , dictionary_of_unique_terms,max_f=x.parse_to_unique_terms(strr)
#print(dic)
#print(dictionary_of_unique_terms)
#print(max_f)

# check 14-3 3/4
# or word-3 3/4


