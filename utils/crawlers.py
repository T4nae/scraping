from selenium import webdriver
import selenium.common.exceptions as ex
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait



class crawler:
    def __init__(self, url):
        self.CHROME_DRIVER = 'utils\drivers\chromedriver.exe'
        self.url = url
        self.driver = None

    def Selenium(self, headless = True):
        # set chrome option
        options = webdriver.ChromeOptions()
        options.headless = headless

        options.add_argument("--disable-hang-monitor")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-gpu")
        options.add_argument('--ignore-certificate-errors')
        #options.add_argument('--incognito')
        options.add_argument("--no-sandbox")

        # start chrome
        self.driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER,
                                options=options)

        # read website by url
        self.driver.get(self.url)
        
        # page details
        page_info = 'Page title : "{title}"\nCurrent URL : "{url}"'
        print(page_info.format(title=self.driver.title, url=self.driver.current_url))
        
        return

    def get_source(self):
        source = self.driver.page_source
        return source

    def find(self, type, locator):
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
        try:
            self.find(type, locator)
        except ex.NoSuchElementException:
            return False
        return True

    def locate_await_presence(self, type, locator):
        while self.locate_presence(type, locator) == False:
            WebDriverWait(self.driver, timeout= 15).untill(lambda d: d.presence_of_element_located(locator))
        return True

    def close(self):
        if self.driver != None:
            self.driver.quit()          