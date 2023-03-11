import pickle
import re
from nltk.stem.snowball import SnowballStemmer
import time
import tkinter as tk

class Search:
    def __init__(self):
        # initializes the indexes
        self.inverted_index = {}
        self.doc_id = {}

    def load_index(self):
        # loads in inverted index
        with open("inverted_index.pickle", "rb") as myFile:
            self.inverted_index = pickle.load(myFile)

    def load_doc_id(self):
        # loads in document id mapping
        with open("doc_id.pickle", "rb") as myFile:
            self.doc_id = pickle.load(myFile)

    def stem_tokens(self, token_list):
        # gets the tokenize list and uses stemming on all words
        stemmer = SnowballStemmer("english")
        stem_words = []
        for token in token_list:
            stem_words.append(stemmer.stem(token))
        return stem_words

    def process_query(self, user_input):
        # splits and stems the tokens
        user_input = re.sub(r'[^a-z0-9\']+', ' ', user_input)
        user_input = re.sub(r'([^a-z0-9]\'|\'[^a-z0-9])', ' ', user_input)
        token_list = user_input.split()
        token_list = self.stem_tokens(token_list)
        return token_list

    def retrieve_doc_id(self, query_token):
        # given a token, retrieve doc id
        if query_token in self.inverted_index.keys():
            return self.inverted_index[query_token]
        else:
            return {}

    def merge(self, dic1, dic2):
        # given 2 dics return intersection
        merge = {}
        for key in dic1.keys():
            if key in dic2.keys():
                merge[key] = dic1[key] + dic2[key]
        return merge

    def get_documents(self, query_list):
        merge_dic = {}
        # find a page that all tokens have in common
        for i in range(len(query_list)):
            # iterates through each token
            if i == 0:
                merge_dic = self.retrieve_doc_id(query_list[i])
            else:
                # merges similar docs between current similar docs and docs in current token iteration
                doc_id_dic = self.retrieve_doc_id(query_list[i])
                merge_dic = self.merge(merge_dic, doc_id_dic)
        return sorted(merge_dic.items(), key=lambda x: x[1], reverse=True)

    def print_result(self, doc_list):
        # prints out the top 5 results
        try:
            print("Top 5 Results:")
            for i in range(5):
                print(self.doc_id[doc_list[i][0]])
        except:
            print("Could not find 5 results.")
        print()

    def run(self):
        # figures out which search tool to use
        self.load_doc_id()
        self.load_index()
        which_one = input('0 - use console\n'
                          '1 - use local GUI\n'
                          'Pick one of these numbers to proceed:')
        print()
        while which_one not in {'0', '1'}:
            which_one = input('0 - use console\n'
                              '1 - use local GUI\n'
                              'Please enter one of these numbers:')
            print()
        if which_one == '0':
            self.run_text()
        elif which_one == '1':
            self.run_tkinter()
        else:
            assert which_one in {'0', '1'}, "This should not have happened."

    @staticmethod
    def obtain_proper_input():
        # checks whether person does or does not want to continue querying
        possible = input('Continue querying from here? (Y or y to continue, N or n to quit):')
        print()
        while possible not in {'Y', 'y', 'N', 'n'}:
            possible = input('Please enter one of the following: Y, y, N, n:')
            print()
        return possible

    def run_text(self):
        # uses the console to search the index
        time_list = []
        repeat = 0
        while self.obtain_proper_input() in {'Y', 'y'}:
            queries = self.process_query(input("Query: ").lower())
            print()
            start_time = time.time()
            self.print_result(self.get_documents(queries))
            finished_time = time.time() - start_time
            time_list.append(finished_time)
            repeat += 1
        if repeat > 0:
            print("My program took", sum(time_list) / repeat, "s to run")
        print(time_list)

    def run_tkinter(self):
        # uses tkinter to search the index
        root = tk.Tk()
        window = tk.Frame(root)
        window.pack(expand=1)

        output_text = tk.StringVar(window, value="")

        def change_output():
            query_as_string = query_entry_box.get(1.0, "end-1c")
            doc_list = self.get_documents(self.process_query(query_as_string))
            doc_string = ''
            try:
                for i in range(5):
                    doc_string += f"{self.doc_id[doc_list[i][0]]}\n"
            except:
                doc_string += "Could not find 5 results."
            output_text.set(doc_string)
            window.update()

        tk.Label(window).grid(row=0, column=0, rowspan=6)
        tk.Label(window,text="Local GUI").grid(row=0, column=1, columnspan=4)
        tk.Label(window).grid(row=0, column=5, rowspan=6)
        tk.Label(window,text="Search Results Here").grid(row=2, column=1, columnspan=4)
        tk.Label(window, textvariable=output_text).grid(row=3, column=1, rowspan=4)

        tk.Label(window, text="Query Entry Box: ").grid(row=1, column=1)
        query_entry_box = tk.Text(window, height=1, width=20)
        query_entry_box.grid(row=1, column=2, columnspan=2)

        set_query_button = tk.Button(window, text="Enter Query", width=8, command=change_output)
        set_query_button.grid(row=1, column=4)

        root.mainloop()


if __name__ == "__main__":
    a = Search()
    a.run()

