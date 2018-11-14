from StopWordsHolder import *
from string import *
global str
import math
# from nltk.stem import PorterStemmer
class Parser:
    hash_of_words = None
    stopWordsHolder = None
    porter_stemmer = None
    # The constructor of the class
    def __init__(self):
        self.hash_of_words = {}# Maybe add a function that reads a data from a file (if we have already parsed before)
        self.stopWordsHolder = StopWordsHolder()
        #self.porter_stemmer = PorterStemmer()

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
    def word_scan(self,word,dictionary):
        flag = len(word) > 0 and word[0] >= 'A' and word[0] <= 'Z'
        word = self.porter_stemmer.stem(word).encode("ascii")
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

    def is_integer(self,number):
        try:
            int(number)
            return True
        except Exception:
            return False

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
    def full_date(self,term):
        # we check if the date is from the from of dd/mm/yy
        if "/" in term:
            newTerm = term.split("/")
            # we check correction
            if self.is_integer(newTerm[0]) == False or self.is_integer(newTerm[1]) == False or self.is_integer(newTerm[2]) == False:
                return term
            # we check if we can identify if the string id dd/mm/yy or mm/dd/yy
            if (newTerm[0] > 12 or newTerm[1]>12) and len(newTerm[2]) > 1:
                if int(newTerm[1])>12:
                    temp = newTerm[1]
                    newTerm[1] = newTerm[0]
                    newTerm[0] = temp
                if len(newTerm[1]) == 1:
                    newTerm[1] = "0" + newTerm[1]
                arrayOfDates = []
                day=newTerm[0]
                month=newTerm[1]
                year=newTerm[2]
                if len(year)>2:
                    arrayOfDates.append(year)
                    if len(year)==3:
                        year=year[1:]
                    else:
                        year=year[2:]
                arrayOfDates.append(day+"-"+month+"-"+year)
                arrayOfDates.append(day+"-"+month)
                return arrayOfDates
            return term
        # we check if the format is written in words
        else:
            val=term
            term = term.lower()
            term = term.replace("th","")
            term = term.replace(",", "")
            newTerm = term.split(' ')
            if len(newTerm)<3:
                return val
            if self.is_integer(newTerm[1]):
                temp = newTerm[1]
                newTerm[1]=newTerm[0]
                newTerm[0]=temp
            day = self.date(newTerm[0]+" "+newTerm[1])
            if day == "it is not a month":
                return val
            year = self.date(newTerm[1] +" "+ newTerm[2])
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

    def parse_to_unique_terms(self,doc_test):
        index = -1  # The index of the current closest space
        new_doc = []  # The new doc
        current_term = ''  # The current term
        next_term = ''  # The next term
        more_words = index != -1
        save_doc = doc_test
        index_saver = index
        additional_word = ''
        doc_test = ' '.join(doc_test.split())
        exclude = set(punctuation)
        exclude.remove('/')
        exclude.remove('-')
        doc_test = ''.join(ch for ch in doc_test if ch not in exclude)
        # Do while index != -1
        while True:

            print("doc_test = %s" % doc_test)
            print("new_doc = %s" % new_doc)
            index = doc_test.find(' ')
            more_words = index != -1
            # Get the current term and it's length, shorten the doc and find the next space
            if not more_words:
                current_term = doc_test
            else:
                current_term = doc_test[0:index]

            doc_test = doc_test[index + 1:]
            index = doc_test.find(' ')
            length = len(current_term)
            if length == 0:
                continue
            if self.is_integer_that_ends_with_th(current_term):
                current_term = current_term[:-2]
            # If the term is a number
            if self.is_number_term(current_term):
                # If there are no more terms
                if not more_words:
                    # Is just a number
                    new_doc.append(self.convert_number_to_wanted_state(current_term))
                    return new_doc

                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = doc_test
                else:
                    next_term = doc_test[0:index]
                doc_test = doc_test[index + 1:]

                save_next_term = next_term
                save_doc = doc_test
                # If the term is an integer
                if self.is_integer(current_term):
                    if int(current_term).__abs__() < 1000:
                        # If the number is a fraction
                        if self.is_fraction(next_term) or (
                                (next_term[len(next_term) - 1] == '%') and self.is_fraction(next_term[:-1])):

                            flag = next_term[len(next_term) - 1] == '%'
                            current_term = current_term + " " + next_term
                            index = doc_test.find(' ')

                            # If there are no more terms
                            if not more_words:
                                # Is just a number or percent like this 22 3/4%
                                if flag:
                                    new_doc.append(self.percentage_number_parsing(current_term))
                                else:
                                    new_doc.append(self.convert_number_to_wanted_state(current_term))
                                break

                            # If there are more terms
                            more_words = index != -1
                            if not more_words:
                                next_term = doc_test
                            else:
                                next_term = doc_test[0:index]
                            doc_test = doc_test[index + 1:]

                            # If it's a price term
                            lower = next_term.lower()
                            if lower == 'dollars' or lower == 'dollar':
                                current_term = current_term + " " + next_term
                                new_doc.append(self.price_number_parsing(current_term))
                                if not more_words:
                                    break
                                continue
                            # If it's a percent term
                            if lower == 'percent' or lower == 'percentage':
                                current_term = current_term + " " + next_term
                                new_doc.append(self.percentage_number_parsing(current_term))
                                if not more_words:
                                    break
                                continue

                        # This is an integer smaller than 1000 and without a fraction
                        # We will check is it is a date
                        if int(current_term) <= 31 and int(current_term) >= 1:
                            if self.monthToNum(next_term.lower()) != None:
                                current_term = current_term + " " + next_term
                                # If there are no more terms
                                if not more_words:
                                    # It is a date like 20 March
                                    new_doc.append(self.date(current_term))
                                    break

                                index = doc_test.find(' ')
                                # If there are more terms
                                more_words = index != -1
                                if not more_words:
                                    next_term = doc_test
                                else:
                                    next_term = doc_test[0:index]
                                doc_test = doc_test[index + 1:]

                                # Than it is a full date
                                if self.is_integer(next_term) and int(next_term) <= 2500:
                                    current_term = current_term + " " + next_term
                                    new_doc.append(self.full_date(current_term))
                                    if not more_words:
                                        break
                                    continue


                # The term is a number that is not an integer or that it's absolute value is not smaller
                # than 1000 or not one of the checks above
                hyphen_index = next_term.find('-')
                flag = hyphen_index != -1 and self.is_number_describer(next_term[:hyphen_index])
                if self.is_number_describer(next_term) or flag:
                    current_term = current_term + " " + next_term

                index = doc_test.find(' ')
                # If the range is like 13 thousand-..
                if flag:
                    # If the range is like 13 thousand-34.7 ..
                    if self.is_float(next_term[hyphen_index + 1:]):
                        # If the range is like 13 thousand-34.7
                        if not more_words:
                            new_doc = self.combine_lists(new_doc, self.range_term_parser(current_term))
                            break

                        # If there are more terms
                        more_words = index != -1
                        if not more_words:
                            next_term = doc_test
                        else:
                            next_term = doc_test[0:index]
                        doc_test = doc_test[index + 1:]

                        # If the range is like 13 thousand-34.7 million

                        if self.is_number_describer(next_term) or self.is_fraction(next_term):
                            current_term = current_term +" "+ next_term
                            new_doc = self.combine_lists(new_doc, self.range_term_parser(current_term))
                            if not more_words:
                                break
                            continue
                        doc_test = next_term + " " +doc_test


                    else:
                        new_doc = self.combine_lists(new_doc, self.range_term_parser(current_term))
                        if not more_words:
                            break
                        continue
                else:
                    # If there are no more terms it must be a number
                    if not more_words:
                        new_doc.append(self.convert_number_to_wanted_state(current_term))
                        break

                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = doc_test
                    else:
                        next_term = doc_test[0:index]
                    doc_test = doc_test[index + 1:]

                    lower = next_term.lower()
                    if lower == 'percent' or lower == 'percentage':
                        current_term = current_term + " " + next_term
                        new_doc.append(self.percentage_number_parsing(current_term))
                        if not more_words:
                            break
                        continue

                    if lower == 'dollar' or lower == 'dollars':
                        current_term = current_term + " " + next_term
                        new_doc.append(self.price_number_parsing(current_term))
                        if not more_words:
                            break
                        continue

                    if lower == 'u.s.':
                        temp = next_term
                        if not more_words:
                            new_doc.append(self.convert_number_to_wanted_state(current_term))
                            new_doc.append(next_term)
                            break
                        index = doc_test.find(' ')
                        # If there are more terms
                        more_words = index != -1
                        if not more_words:
                            next_term = doc_test
                        else:
                            next_term = doc_test[0:index]
                        doc_test = doc_test[index + 1:]
                        lower = next_term.lower()
                        if lower == 'dollar' or lower == 'dollars':
                            current_term = current_term + " " + temp + " " + next_term
                            new_doc.append(self.price_number_parsing(current_term))
                            if not more_words:
                               break
                            continue

                    new_doc.append(self.convert_number_to_wanted_state(current_term))
                    doc_test = next_term + " " + doc_test
                    continue

            # If the term is not an integer
            # if the tern starts with $
            if current_term[0] == '$':
                if self.is_number_term(current_term[1:]):
                    if current_term[len(current_term) - 1].lower() in ['k', 'm', 'b', 't', 'q']:
                        new_doc.append(self.price_number_parsing(current_term))
                        continue

                    if not more_words:
                        new_doc.append(self.price_number_parsing(current_term))
                        break

                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = doc_test
                    else:
                        next_term = doc_test[0:index]
                    doc_test = doc_test[index + 1:]

                    if self.is_number_describer(next_term):
                        current_term = current_term + " " + next_term

                    new_doc.append(self.price_number_parsing(current_term))
                    if not more_words:
                       break
                    continue

            if current_term.lower() == "between":

                so_far = ''
                if not more_words:
                    new_doc.append(current_term)
                    break

                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = doc_test
                else:
                    next_term = doc_test[0:index]
                doc_test = doc_test[index + 1:]

                so_far = next_term
                if not self.is_number_term(next_term) or not more_words:
                    if more_words:
                        doc_test = so_far + " " + doc_test
                    else:
                        doc_test = so_far
                    new_doc.append(current_term)
                    continue

                index = doc_test.find(' ')
                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = doc_test
                else:
                    next_term = doc_test[0:index]
                doc_test = doc_test[index + 1:]

                if self.is_number_describer(next_term):
                    so_far = so_far + " " + next_term
                    index = doc_test.find(' ')
                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = doc_test
                    else:
                        next_term = doc_test[0:index]
                    doc_test = doc_test[index + 1:]

                so_far = so_far + " " + next_term
                print next_term
                if (next_term.lower() != "and" and next_term.lower() != "to") or not more_words:
                    if more_words:
                        doc_test = so_far + " " + doc_test
                    else:
                        doc_test = so_far
                    new_doc.append(current_term)
                    continue
                print next_term
                index = doc_test.find(' ')
                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = doc_test
                else:
                    next_term = doc_test[0:index]
                doc_test = doc_test[index + 1:]

                so_far = so_far + " " + next_term
                if not self.is_number_term(next_term):
                    if more_words:
                        doc_test = so_far + " " + doc_test
                    else:
                        doc_test = so_far
                    new_doc.append(current_term)
                    continue

                if more_words:
                    index = doc_test.find(' ')
                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = doc_test
                    else:
                        next_term = doc_test[0:index]
                    doc_test = doc_test[index + 1:]
                    if self.is_number_describer(next_term):
                        so_far = so_far + " " + next_term
                    else:
                        if more_words:
                            doc_test = next_term + doc_test
                        else:
                            doc_test = next_term
                        more_words = True


                current_term = current_term + " " + so_far
                new_doc = self.combine_lists(new_doc, self.range_term_parser(current_term))
                if not more_words:
                   break
                continue


            if self.monthToNum(current_term.lower())!= None:
                if not more_words:
                    new_doc.append(next_term)
                    break

                index = doc_test.find(' ')
                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = doc_test
                else:
                    next_term = doc_test[0:index]
                doc_test = doc_test[index + 1:]


                flag1 = self.is_integer(next_term)
                flag2 = self.is_integer_that_ends_with_th(next_term)
                flag3 = self.is_integer_that_ends_with_th(next_term[:-1]) and next_term[len(next_term) - 1] == ','
                flag4 = self.is_integer(next_term[:-1]) and next_term[len(next_term)-1] == ','
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
                        new_doc.append(self.date(current_term))
                        if not more_words:
                           break
                        continue

                    index = doc_test.find(' ')
                    # If there are more terms
                    more_words = index != -1
                    if not more_words:
                        next_term = doc_test
                    else:
                        next_term = doc_test[0:index]
                    doc_test = doc_test[index + 1:]

                    if not self.is_integer(next_term):
                        doc_test = next_term
                        new_doc.append(self.full_date(current_term))

                    current_term = current_term + " " + next_term
                    new_doc.append(self.full_date(current_term))
                    if not more_words:
                       break
                    continue

            if self.is_date(current_term):
                new_doc.append(self.full_date(current_term))
                if not more_words:
                   break
                continue


            if self.is_word_number(current_term):
                if not more_words:
                    new_doc = self.combine_lists(new_doc,self.range_term_parser(current_term))
                    break

                index = doc_test.find(' ')
                # If there are more terms
                more_words = index != -1
                if not more_words:
                    next_term = doc_test
                else:
                    next_term = doc_test[0:index]
                doc_test = doc_test[index + 1:]

                if self.is_number_describer(next_term) or self.is_fraction(next_term):
                    current_term = current_term + " "+ next_term
                    new_doc = self.combine_lists(new_doc, self.range_term_parser(current_term))
                    if not more_words:
                       break
                    continue

                doc_test = next_term +" " + doc_test

            number_of_hyphens = current_term.count('-')
            # If it's word-word or word-word-word
            if number_of_hyphens == 1 or number_of_hyphens == 2:
                new_doc = self.combine_lists(new_doc, self.range_term_parser(current_term))
                if not more_words:
                   break
                continue



            additional_word = additional_word +" " + current_term

            if not more_words:  # Do while index != -1
                break



        additional_word = additional_word[1:]
        print additional_word
        # Remove stop words anf punctuations
        additional_word = ''.join(ch for ch in additional_word if ch not in ['-','/'])
        additional_word = self.remove_stop_words(additional_word)
        print additional_word

        dictionary = self.scan_list_of_word(additional_word)
        print dictionary
        self.add_list_of_terms_to_dictionary(new_doc,dictionary)
        # need to combine the dictionary and the new_doc (also need to maje the new doc a dictionary with a counter)
        return dictionary


    def add_list_of_terms_to_dictionary(self,list_of_terms,dictionary):
        for i in range(0,len(list_of_terms)):
            self.add_to_dictionary(dictionary,list_of_terms[i])
    def add_to_dictionary(self,dictionary,term):
        if term in dictionary:
            dictionary[term] = dictionary[term] + 1
        else:
            dictionary[term] = 1
    def remove_stop_words(self,words):
        words = words.split()
        result = [word for word in words if not self.stopWordsHolder.is_stop_word(word)]
        return result
    def is_word_number(self,term):
        number_of_hyphens = term.count('-')
        if number_of_hyphens != 1:
            return False
        second = term[term.find('-')+1:]
        return self.is_number_term(second)

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

    def combine_lists(self,list1, list2):
        for i in range(0, len(list1)):
            list2.append(list1[i])
        return list2

    def is_number_term(self,term):
        length = len(term)
        term = term.lower()
        if self.is_number(term):
            return True
        if term[length - 1] in ['k', 'm', 'b', 't', 'q']:
            return self.is_number(term[:-1])
        if term[-2:] == 'bn':
            return self.is_number(term[:-2])
        return False

    def is_integer_that_ends_with_th(self,number):
        return number[-2:].lower() == 'th' and self.is_integer(number[:-2])

    def is_fraction(self,term):
        index = term.find('/')
        if index == -1:
            return False
        return self.is_float(term[:index]) and self.is_float(term[index + 1:])

    def is_number_describer(self,word):
        return word.lower() in ['thousand', 'thousands', 'million', 'millions', 'trillions', 'trillion', 'billion',
                                'billions', 'quadrillion', 'quadrillion', 'bn']

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

    #this function should return the begining of a weigth. for example:13kg return 2
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
    #this function shoud give us the number that we neet to mult in in order to get kg
    def how_much_to_mult_for_kg(self, term):
        if term == "gram" or term == "g":
            return math.pow(10, - 3)
        if term == "decagram" or term == "dag":
            return math.pow(10, 1 - 3)
        if term == "hectogram" or term == "hg":
            return math.pow(10, 2 - 3)
        if term == "kilogram" or term == "kg":
            return math.pow(10, 3 - 3)
        if term == "tonne":
            return math.pow(10, 6 - 3)
        if term == "decigram" or term == "dg":
            return math.pow(10, -1 - 3)
        if term == "centigram" or term == "cg":
            return math.pow(10, -2 - 3)
        if term == "milligram" or term == "mg":
            return math.pow(10, -3 - 3)

    # convert any measer unit into kg
    def convert_to_kg(self, weigth):
        weigth=self.convert_to_degit_num(weigth)
        place = int(self.find_the_letter(weigth))
        num = weigth[0:place]
        measure_unit = weigth[place:]
        if num=="":
            return measure_unit
        measure_unit = measure_unit.lower()
        measure_unit=self.how_much_to_mult_for_kg(measure_unit)
        num=float(num)
        measure_unit=float(measure_unit)
        num=num*measure_unit
        return str(num)+" "+"kg"

    def is_string(self,str):
        try:
            str =str+ ''
        except:
            return False
        return True

    #if we get 200 handred kg it will return 20000.0kg
    def convert_to_degit_num(self, str):
        arrStr = str.split()
        if len(arrStr) == 3:
            arrStr = [(self.parseNumber(arrStr[0] + " " + arrStr[1])), arrStr[2]]
        if len(arrStr) == 2:
            x = arrStr[0]
            if self.is_string(x):
                x = arrStr[0]
            else:
                x = "%d" % x
            weigt = x +  (arrStr[1])
            return weigt
        return str






x = Parser()
print(x.convert_to_kg(""))

# check 14-3 3/4
# or word-3 3/4

