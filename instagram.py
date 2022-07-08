from utils.crawlers import crawler
from utils.data import data
from bs4 import BeautifulSoup
from getpass import getpass
import argparse
from time import sleep




def login(args):
    """
    login to your instagram account
    """
    if args.pwd == '':
        pwd = getpass('Enter Password:')
    else:
        pwd = args.pwd

    url = 'https://www.instagram.com/accounts/login/'
    crawl = crawler(url)
    crawl.Selenium()
    crawl.driver.implicitly_wait(5)
    loginbox = crawl.find('XPATH', '//*[@id="loginForm"]/div/div[1]/div/label/input')
    loginbox.send_keys(args.id)
    passWordbox = crawl.find('XPATH', '//*[@id="loginForm"]/div/div[2]/div/label/input')
    passWordbox.send_keys(pwd)
    loginButton = crawl.find('XPATH', '//*[@id="loginForm"]/div/div[3]')
    loginButton.click()

    sleep(9999)

    return

def hompage(args):
    """
    scrape contents of homepage
    """
    return

def user(args):
    """
    scrape contents of an particular user
    """
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--login', type= bool, default=True,
        help='Login to your instagram account')
    parser.add_argument('--feed', choices=['hompage', 'user'], type= str, default= 'hompage',
      help='to select between viewing hompage feed or some user feed. ' 
            'to view Subscription feed you must provide your --id and pass. ')
    parser.add_argument('--id', type=str,
      help='email id to login into your instagram account')
    parser.add_argument('--pwd', type=str, default='',
      help='password to email id to login into your instagram account') 
    parser.add_argument('--user', type=str, default='',
        help='username for user to get feed from')

    args = parser.parse_args()


    if args.feed == 'user':
        user(args)
    else:
        hompage(args)    