import pickle
import re
from nltk.stem.snowball import SnowballStemmer
import time

class Search:
    def __init__(self):
        #initializes the indexes
        self.inverted_index = {}
        self.doc_id = {}
        self.loop = True

    def load_index(self):
        #loads in inverted index
        with open("inverted_index.pickle", "rb") as myFile:
            self.inverted_index = pickle.load(myFile)

    def load_doc_id(self):
        #loads in document id mapping
        with open("doc_id.pickle", "rb") as myFile:
            self.doc_id = pickle.load(myFile)

    def stem_tokens(self, token_list):
        #gets the tokenize list and uses stemming on all words
        stemmer = SnowballStemmer("english")
        stem_words = []
        for token in token_list:
            stem_words.append(stemmer.stem(token))
        return stem_words

    def process_query(self, user_input):
        #splits and stems the tokens
        user_input = re.sub(r'[^a-z0-9\']+', ' ', user_input)
        user_input = re.sub(r'([^a-z0-9]\'|\'[^a-z0-9])', ' ', user_input)
        token_list = user_input.split()
        token_list = self.stem_tokens(token_list)
        return token_list

    def get_user_query(self):
        #get query from user and proccess it
        print("Query: ", end = "")
        user_input = input().lower()
        print()
        self.start_time = time.time() #keep track of how ong to fetch each query
        return self.process_query(user_input)
    
    def retrieve_doc_id(self, query_token):
        #given a token, retrive doc id
        if query_token in self.inverted_index.keys():
            return self.inverted_index[query_token]
        else:
            return {}

    def merge(self, dic1, dic2):
        #given 2 dics return intersection
        merge = {}
        for key in dic1.keys():
            if key in dic2.keys():
                merge[key] = dic1[key] + dic2[key]
        return merge

    def get_documents(self):
        query_list = self.get_user_query()
        if (len(query_list) == 0):
            self.loop = False
            return
        merge_dic = {}
        #find a page that all tokens have in common
        for i in range(len(query_list)):
            #iterates through each token
            if (i == 0):
                merge_dic = self.retrieve_doc_id(query_list[i])
            else:
                #merges similar docs between current similar docs and docs in current token iteration
                doc_id_dic = self.retrieve_doc_id(query_list[i])
                merge_dic = self.merge(merge_dic, doc_id_dic)
        return sorted(merge_dic.items(), key=lambda x: x[1], reverse=True)

    def print_result(self, doc_list):
        #prints out the top 5 results
        try:
            print("Top 5 Results:")
            for i in range(5):
                print(self.doc_id[doc_list[i][0]])
        except:
            print("Could not find 5 results.")
        print()
        print("Finished in {}ms\n".format(round((time.time() - self.start_time) * 1000)))

    def run(self):
        self.load_doc_id()
        self.load_index()
        while(self.loop):
            self.print_result(self.get_documents())

if __name__ == "__main__":
    a = Search()
    a.run()
