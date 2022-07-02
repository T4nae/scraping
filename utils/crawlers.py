from selenium import webdriver


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
        options.add_argument('--incognito')
        options.add_argument("--no-sandbox")

        # start chrome
        self.driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER,
                                options=options)

        # read website by url
        self.driver.get(self.url)
        
        # page details
        page_info = 'Page title : "{title}"\nCurrent URL : "{url}"'
        print(page_info.format(title=self.driver.title, url=self.driver.current_url))

        # get page source
        page_source = self.driver.page_source

        return page_source

    def close(self):
        if self.driver != None:
            self.driver.quit()          