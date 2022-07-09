import pickle
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import selenium.common.exceptions as ex
from selenium.webdriver.common.by import By


class crawler:
    def __init__(self, url):
        self.CHROME_DRIVER = 'utils\drivers\chromedriver.exe'
        self.url = url
        self.driver = None

    def Selenium(self, undetected = False, headless = True):
        """
        initalize the webdriver
        """
        # set chrome option
        # check if needs undetected
        if undetected:
            options = uc.ChromeOptions()
        else:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument('--ignore-certificate-errors')

        options.headless = headless

        options.add_argument("--window-size=1080,1080")
        options.add_argument('--allow-running-insecure-content')
        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-gpu")
        #options.add_argument('--incognito')
    

        # start chrome
        # check if needs undetected
        if undetected:
            self.driver = uc.Chrome(driver_executable_path=self.CHROME_DRIVER,
                                    options=options, use_subprocess=True)                      
        else:                 
            self.driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER,
                                    options=options)

        # read website by url
        self.driver.get(self.url)
        
        # page details
        page_info = 'Page title : "{title}"\nCurrent URL : "{url}"'
        print(page_info.format(title=self.driver.title, url=self.driver.current_url))
        
        return

    def get_url(self, url):
        """
        go to the given url
        """
        self.url = url
        self.driver.get(self.url)
        return

    def get_source(self):
        """
        get source code of current webpage
        """
        source = self.driver.page_source
        return source

    def find(self, type, locator):
        """
        find any element on an webpage using any type
        """
        if type == 'XPATH':
            element = self.driver.find_element(By.XPATH , locator)
        elif type == 'CLASS':
            element = self.driver.find_element(By.CLASS_NAME , locator)        
        elif type == 'TAG':
            element = self.driver.find_element(By.TAG_NAME , locator)
        elif type == 'CSS':
            element = self.driver.find_element(By.CSS_SELECTOR , locator)    
        elif type == 'ID':
            element = self.driver.find_element(By.ID , locator)
        elif type == 'LINK':
            element = self.driver.find_element(By.LINK_TEXT, locator)
        elif type == 'PARTIAL_LINK':
            element = self.driver.find_element(By.PARTIAL_LINK_TEXT(locator))
        else:
            raise Exception('Not a Valid Type')

        return element

    def locate_presence(self, type, locator):
        """
        checks if element is located or not
        """
        try:
            self.find(type, locator)
        except ex.NoSuchElementException:
            return False
        return True

    def await_element(self, type, locator):
        """
        wait for the element to load
        """

        try:
            if type == 'XPATH':
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator)))
            elif type == 'CLASS':
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, locator)))        
            elif type == 'TAG':
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, locator)))
            elif type == 'CSS':
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, locator)))    
            elif type == 'ID':
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, locator)))
            elif type == 'LINK':
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, locator)))
            elif type == 'PARTIAL_LINK':
                element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, locator)))
            else:
                raise Exception('Not a Valid Type')
        except ex.NoSuchElementException:
            return

        return 

    def get_cookies(self, name):
        """
        get cookies from the browser to stop repetative task everytime program runs
        """
        pickle.dump(self.driver.get_cookies(), open(name,"wb"))

        return   

    def add_cookies(self, name):
        """
        add cookies from the browser to stop repetative task everytime program runs
        """
        cookies = pickle.load(open(name, "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        return

    def close(self):
        """
        close the broswer and driver
        """
        if self.driver != None:
            self.driver.quit()         