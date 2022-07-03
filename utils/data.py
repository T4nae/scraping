import csv
import os
import pandas as pd

class data:
    def __init__(self):
        self.dataframe = None
        self.path = 'data.csv'
        
    def create_csv(self):
        if os.path.exists(self.path):
            self.path = self.path + '(1)'

        with open(self.path, 'w'):
            pass
    
    def write_csv(self, row):
        with open(self.path, 'a', encoding='UTF8') as file:
            writter = csv.writer(file)
            writter.writerow(row)
        
    def concatenate(self, *args):
        """
        concatenate 2 or more lists together and make csv file
        """
        lists = []
        for lsts in args:
            lists.append(lsts)

        self.create_csv()

        data = []
        for nelmnts in range(len(lists[0])): # no of elements in list
            for nlsts in range(len(lists)):  # no of lists 
                data.append(lists[nlsts][nelmnts])   
                #print(lists[nlsts][nelmnts])
            self.write_csv(data)
            data = []
        
    def view_data(self):
        self.dataframe = pd.read_csv(self.path)
        return self.dataframe
