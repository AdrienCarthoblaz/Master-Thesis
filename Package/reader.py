""" This class will implement the Composite Design Pattern"""
import pandas as pd 

class ReaderComponent:
    def add(self, comp):
        raise NotImplementedError

    def remove(self, comp):
        raise NotImplementedError

    def getChild(self, i):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    
class ReaderComposite(ReaderComponent):
    def __init__(self):
        self.readers = []

    def add(self, comp):
        self.readers.append(comp)

    def remove(self, comp):
        self.readers.remove(comp)

    def read(self):
        for r in self.readers:
            r.read()
        self.df = pd.concat([r.df for r in self.readers])
        self.df.sort_values(["date"],axis=0,ascending=True,inplace=True)


class Reader(ReaderComponent):
    def __init__(self, path):
        self.path = path
        self.df = {}

    def read(self):
        """ Each reader will have to implement this function and store the result in self.df """
        raise NotImplementedError
