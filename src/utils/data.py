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
        creates a unique csv file with headers
        """
        
        while path.exists(self.path + '.csv'):
            if self.path.endswith(')') and self.path[-2:-1].isnumeric() and self.path[-3:-2] == '(':
                self.path = self.path[:-2] + str(int(self.path[-2:-1]) + 1) + ')'
            else:
                self.path = self.path + '(1)'
            
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

        data = []
        for nelmnts in range(len(lists[0])): # no of elements in list
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