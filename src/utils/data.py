import csv
import pandas as pd
from os import path
from bs4 import BeautifulSoup
from lxml import etree


class data:
    def __init__(self, source= ''):
        self.dataframe = None
        self.path = '../data/data'
        self.source = source
        
    def create_csv(self, headers):
        """
        creates a unique csv file with headers to avoid overwrite of usefull data
        """
        # length of deafult path
        size = len(self.path) + 1

        # checks if path exists after adding 1 each time
        while path.exists(self.path + '.csv'):
            # adds 1 each time to path 
            if self.path.endswith(')') and self.path[size:][:-1].isnumeric() and self.path[size - 1] == '(':
                self.path = self.path[:size] + str(int(self.path[size:][:-1]) + 1) + ')'
            else:
                self.path = self.path + '(1)'

        # creates a unique csv file    
        with open(self.path + '.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(headers) 
               
    def write_csv(self, row):
        """
        write data into row at a time in already created csv file
        """
        with open(self.path + '.csv', 'a', encoding='UTF8') as file:
            writter = csv.writer(file)
            writter.writerow(row)
        
    def concatenate(self, lists):
        """
        concatenate list of lists together and make csv file
        """
        # lists to hold temp data
        data = [] 
        items = []

        # findind minimum no. of elements out of all lists
        for i in lists:
            if i != []:
                items.append(len(i))
            else:
                pass 
        size = min(items)

        for nelmnts in range(size): # minimium no of elements in list
            for nlsts in range(len(lists)):  # no of lists 
                data.append(lists[nlsts][nelmnts])   
                #print(lists[nlsts][nelmnts])
            self.write_csv(data)
            data = []
        
    def view_data(self):
        """
        prints dataframe from csv file in a more readable manner
        """
        self.dataframe = pd.read_csv(self.path + '.csv')
        return self.dataframe

    def find(self, div, ids= '', CLASS= '', type='text'):
        """
        find data in source by div and ID or CLASS
        """
        data = []
        
        soup = BeautifulSoup(self.source, 'lxml')
        if type == 'text' and ids != '':
            for selector in soup.find_all(div, id= ids):
                data.append(selector.text)
        elif type == 'text' and CLASS != '':
            mydiv = soup.find_all(div, class_ = CLASS)
            for selector in mydiv:
                data.append(selector.get_text())               
        elif type == 'links' and ids != '':    
            for selector in soup.find_all(div, id=ids, href=True):
                data.append(selector['href'])
        elif type == 'links' and CLASS != '':
            mydiv = soup.find_all(div, class_ = CLASS, href=True)
            for selector in mydiv:
                data.append(selector['href'])
        else:
            data = None

        return data

    def find_by_xpath(self, xpath):
        """
        find data in source by their xpath
        """
        data = []
        soup = BeautifulSoup(self.source, 'lxml')

        dom = etree.HTML(str(soup))
        for element in dom.xpath(xpath):
            data.append(element.text)

        return data