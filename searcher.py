import pickle
# import tkinter as tk


class searcher():
    def __init__(self) -> None:
        self.inverted_index = {}

    def pickle_index(self):
        # stores inverted index in disk
        with open("inverted_index.pickle", "wb") as my_file:
            pickle.dump(self.inverted_index, my_file)


    def run(self):
        self.pickle_index()


if __name__ == '__main__':
    ser = searcher()
    ser.run()
