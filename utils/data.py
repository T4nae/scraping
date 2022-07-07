import csv
import os
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree


class data:
    def __init__(self, source):
        self.dataframe = None
        self.path = 'data.csv'
        self.source = source
        
    def create_csv(self, headers):
        """
        creates a unique csv file with headers
        """

        if os.path.exists(self.path):
            self.path = self.path + '(1)'

        with open(self.path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
    
    def write_csv(self, row):
        """
        write data into row at a time in already created csv file
        """
        with open(self.path, 'a', encoding='UTF8') as file:
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
        self.dataframe = pd.read_csv(self.path)
        return self.dataframe

    def find_by_id(self, div, ids, type='text'):
        """
        find data in source by div and id
        """
        data = []
        
        soup = BeautifulSoup(self.source, 'lxml')
        if type == 'text':
            for selector in soup.find_all(div, id= ids):
                data.append(selector.text)

        elif type == 'links':    
            for selector in soup.find_all('a', id='video-title', href=True):
                data.append(selector['href'])

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