# instagram scrapper is in WIP mainly because Instagrammy is better and easier
from utils.crawlers import crawler
from utils.data import data
from os import path
import wget
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
    crawl.Selenium(headless=False)
    crawl.driver.implicitly_wait(5)
    loginbox = crawl.find('XPATH', '//*[@id="loginForm"]/div/div[1]/div/label/input')
    loginbox.send_keys(args.id)
    passWordbox = crawl.find('XPATH', '//*[@id="loginForm"]/div/div[2]/div/label/input')
    passWordbox.send_keys(pwd)
    loginButton = crawl.find('XPATH', '//*[@id="loginForm"]/div/div[3]')
    loginButton.click()
    notnowButton = crawl.find('XPATH', '//*[@id="react-root"]/section/main/div/div/div/div/button')
    notnowButton.click()
    sleep(5)
    #crawl.await_element('XPATH', '//*[@id="mount_0_0_bS"]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[1]')
    #noNotifictions = crawl.find('XPATH', '//*[@id="mount_0_0_bS"]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[1]')
    #noNotifictions.click()

    crawl.get_cookies('..\cookies\instacookie.pkl')
    return crawl

def hompage(args):
    """
    scrape contents of homepage
    """
    if path.exists('..\cookies\instacookie.pkl') and args.cookie == True:
        crawl = crawler('https://www.instagram.com/')
        crawl.Selenium(headless=False)
        crawl.driver.implicitly_wait(5)
        crawl.add_cookies('..\cookies\instacookie.pkl')
        crawl.get_url('https://www.instagram.com/')
    else:    
        crawl = login(args)

    crawl.locate_presence('TAG', 'img')
    crawl.driver.execute_script('window.scrollTo(0, 4000);')

    #select images
    images = crawl.find('TAG', 'img')
    images = [image.get_attribute('src') for image in images]
    images = images[:-2] #slicing-off IG logo and Profile picture

    #download images
    counter = 0
    for image in images:
        save_as = 'image(' + str(counter) + ').jpg'
        wget.download(image, save_as)
        counter += 1

    crawl.close()
    return

def user(args):
    """
    scrape contents of an particular user
    """
    if path.exists('..\cookies\instacookie.pkl') and args.cookie == True:
        crawl = crawler('https://www.instagram.com/')
        crawl.Selenium(headless=False)
        crawl.driver.implicitly_wait(5)
        crawl.add_cookies('..\cookies\instacookie.pkl')
        crawl.get_url('https://www.instagram.com/')
    else:    
        crawl = login(args)

    crawl.get_url('https://www.instagram.com/' + args.user + '/')
    
    crawl.locate_presence('XPATH', '//*[@id="mount_0_0_zW"]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/div[1]/h2')
    source = crawl.get_source()
    with open('source.txt', 'w', encoding='UTF-8') as file:
        file.write(source)



    crawl.close()
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--login', type= bool, default=True,
        help='Login to your instagram account')
    parser.add_argument('--feed', choices=['hompage', 'user'], type= str, default= 'hompage',
      help='to select between viewing hompage feed or some user feed. ' 
            'to view Subscription feed you must provide your --id and --pwd. ')
    parser.add_argument('--id', type=str,
      help='email id to login into your instagram account')
    parser.add_argument('--pwd', type=str, default='',
      help='password to email id to login into your instagram account'
             'you can leave this param and get more secure pass screen in terminal') 
    parser.add_argument('--user', type=str, default='',
        help='username for user to get feed from')
    parser.add_argument('--cookie', type=bool, default=True,
      help='to enable use of cookie to login to last used account')


    args = parser.parse_args()


    if args.feed == 'user':
        user(args)
    else:
        hompage(args)