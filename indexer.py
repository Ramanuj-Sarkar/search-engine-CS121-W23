import os
import json
from bs4 import BeautifulSoup
import re
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import pickle
import math

class indexer:
    def __init__(self) -> None:
        self.doc_id = {} #will map doc_id to url
        self.doc_id_gen  = 0 #value to assign to a doc
        self.num_pages = 0 #number of indexed documents 
        self.partial_pages = 0 #number of total indexed documents for current partial index
        self.inverted_index = {} #{token:{doc_id1: fequency, doc_id2: frequency}}
        self.unique_words = 0
        self.current_doc_id = 0
        self.currentPartial = 0
        self.partial_files = []
    
    def create_index(self):
        #opens up the directory with all the pages
        target_pages = os.getcwd()
        target_pages += '\\DEV'

        #gets all the pages and attaches it with correct path names
        for root, dirs, files in os.walk(target_pages):
            for file in files:
                file = os.path.join(root, file)
                #load the json file
                file = self.load_json(file)
                #file is now a json(dic format with 'url' 'content' 'encoding')
                soup = BeautifulSoup(file['content'], "lxml")
                self.num_pages += 1
                self.partial_pages += 1
                #tokenize everything in the content json
                tokens = self.tokenize(soup)
                #tokenize important words
                tokens_important = []
                for i in soup.find_all(['b', 'strong', 'h1', 'h2', 'h3', 'title']):
                    #tokenize everything that is within the tags above
                    tok = self.tokenize(i)
                    for i in tok:
                        tokens_important.append(i)
                #stems the words
                stem_tokens = self.stem_tokens(tokens)
                stem_tokens_important = self.stem_tokens(tokens_important)
                #get all the words in the page into a frequency dictionary
                freq_dict = self.compute_word_frequencies(stem_tokens)
                freq_dict_important = self.compute_word_frequencies(stem_tokens_important)
                #add to index
                self.add_to_index(freq_dict, freq_dict_important)
                #Dump partial index into disk if files currently read through is larger than 13,000
                if self.partial_pages >= 13000 :
                    file_name = "inverted_index" + str(self.currentPartial)+ ".pickle"
                    self.partial_files.append(file_name)
                    self.currentPartial+= 1
                    self.partial_pages = 0
                    self.pickle_index(file_name)
                    self.inverted_index = {}

    def add_to_index(self, freq_dict, freq_dict_important):
        #loop through dict and add each token to inverted_index
        for token in freq_dict.keys():
            if token in self.inverted_index:
                self.inverted_index[token][self.current_doc_id] = freq_dict[token]
                if token in freq_dict_important:
                    self.inverted_index[token][self.current_doc_id] += freq_dict_important[token]
            else:
                self.unique_words += 1
                self.inverted_index[token] = {}
                self.inverted_index[token][self.current_doc_id] = freq_dict[token]
                if token in freq_dict_important:
                    self.inverted_index[token][self.current_doc_id] += freq_dict_important[token]

    def compute_score(self):
        for token in self.inverted_index.keys():
            for doc in self.inverted_index[token].keys():
                self.inverted_index[token][doc] = (1 + math.log(self.inverted_index[token][doc])) * math.log(self.num_pages/ len(self.inverted_index[token]))

    def stem_tokens(self, token_list):
        #gets the tokenize list and uses stemming on all words
        stemmer = SnowballStemmer("english")
        stem_words = []
        for token in token_list:
            stem_words.append(stemmer.stem(token))
        return stem_words

    def tokenize(self, soup_content):
        # get all the text from the html page
        # and make it lowercase
        html_text = soup_content.get_text().lower()
        # this takes out non-word characters everything except
        # sequences of alphanumeric characters and apostrophes
        html_text = re.sub(r'[^a-z0-9\']+', ' ', html_text)
        # this takes out apostrophes which aren't surrounded by
        # alphanumeric characters on at least one side because I figure
        # those are not actually "in" the words
        html_text = re.sub(r'([^a-z0-9]\'|\'[^a-z0-9])', ' ', html_text)
        # puts all the words into a list
        return html_text.split()

    def compute_word_frequencies(self, token_list):
        frequencies = defaultdict(int)
        for token in token_list:
            frequencies[token] += 1
        return frequencies
                
    def load_json(self, file):
        #opens json
        j_file = json.load(open(file))
        #assigns each file a doc id and maps it to the url
        self.assign_doc_id(j_file["url"])
        return j_file

    def assign_doc_id(self, file):
        #maps the doc id to the url
        self.doc_id[self.doc_id_gen] = file
        self.current_doc_id = self.doc_id_gen
        self.doc_id_gen += 1
    
    def write_report(self):
        #write stats to report
        with open("report.txt", "w") as my_file:
            my_file.write("The number of indexed document: {}\n".format(self.num_pages))
            my_file.write("The number of unique words: {}\n".format(self.unique_words))
            my_file.write("The total size of index on disk: {} KB\n".format(self.get_index_file_size()))

    def pickle_index(self,file_name ):
        #stores inverted index in disk
        with open(file_name, "wb") as my_file:
            pickle.dump(self.inverted_index, my_file)
    
    def pickle_doc_id(self):
        #stores inverted index in disk
        with open("doc_id.pickle", "wb") as my_file:
            pickle.dump(self.doc_id, my_file)

    def get_index_file_size(self):
        #get the path of pickle file
        file = os.getcwd()
        file += "\\inverted_index.pickle"
        #returns the size
        return os.path.getsize(file) / 1000 #to get in KB
    

    def merge_partial(self, partial_list):
        #merges all files into final inverted index file
        merged_index = defaultdict(dict)
        for file in partial_list:
            with open(file, 'rb') as given:
                partial_index = pickle.load(given)
                for token, docID in partial_index.items():
                    merged_index[token].update(docID)
        with open("merged_index_final.pickle", 'wb') as my_file:
            pickle.dump(merged_index, my_file)
        



    def run(self):
        self.create_index()
        self.compute_score()
        file_name = "inverted_index" + str(self.currentPartial)+ ".pickle"
        self.partial_files.append(file_name)
        self.pickle_index(file_name) #remember to add last pickle_index with file name of last partial index
        self.merge_partial(self.partial_files) #merges partial indexes
        self.pickle_doc_id()
        self.write_report()

if __name__ == "__main__":
    ini = indexer()
    ini.run()
