from utils.crawlers import crawler
from utils.data import data
from getpass import getpass
from os import path
import argparse

def extract_data(source, args):
    # making lists to hold data
    file = data(source)
    lists = []
    headers = []

    # finding titles 
    if args.titles == True:
        if args.feed == 'subscriptions':
            titles = file.find_by_xpath('//*[@id="video-title"]') 
            lists.append(titles)
            headers.append('TITLES')
        elif args.feed == 'explore':
            titles = file.find_by_xpath('//*[@id="video-title"]/yt-formatted-string') 
            lists.append(titles)
            headers.append('TITLES')

    # finding views
    if args.views == True:
        views = file.find_by_xpath("//*[@id='metadata-line']/span[1]")
        lists.append(views)
        headers.append('VIEWS')

    # finding posted ago
    if args.postedago == True:
        posted = file.find_by_xpath('//*[@id="metadata-line"]/span[2]')        
        lists.append(posted)
        headers.append('POSTED AGO')

    # getting links of videos
    if args.links == True:
        links = []
        href = file.find('a', ids= 'video-title', type= 'links')
        for link in href:
            links.append("https://www.youtube.com" + link)
        lists.append(links)
        headers.append('LINKS')  
        

    # arranging data
    file.create_csv(headers)
    file.concatenate(lists)

    if args.v == True:
        print(file.view_data())



def subsciptions(args):
    """
    get video details from the subscriptions feed
    """
    url = 'https://www.youtube.com/feed/subscriptions'
    crawl = crawler(url)
    if path.exists('..\cookies\youtubecookie.pkl') and args.cookie == True:
      crawl.Selenium() # since we using cookies no need to use undetected can be run in headless
      crawl.add_cookies('..\cookies\youtubecookie.pkl')
      crawl.get_url(url)
      crawl.driver.implicitly_wait(5)
      crawl.locate_presence('XPATH', '//*[@id="endpoint"]/tp-yt-paper-item/yt-formatted-string')
    else:
      crawl.Selenium(undetected=True, headless=False)  # can't run in headless mode since UC headlessmode is still WIP
      crawl.driver.implicitly_wait(5)
      crawl.find('LINK', 'SIGN IN').click()
      if args.pwd == '':
          pwd = getpass('Enter Password:')
      else:
          pwd = args.pwd    
 
      loginBox = crawl.find('XPATH', '//*[@id ="identifierId"]')
      loginBox.send_keys(args.id)
      nextButton = crawl.find('XPATH', '//*[@id ="identifierNext"]')
      nextButton.click()
      passWordBox = crawl.find('XPATH', '//*[@id ="password"]/div[1]/div / div[1]/input')
      passWordBox.send_keys(pwd)
      nextButton = crawl.find('XPATH', '//*[@id ="passwordNext"]')
      nextButton.click()
      crawl.locate_presence('XPATH', '//*[@id="endpoint"]/tp-yt-paper-item/yt-formatted-string')
      crawl.get_cookies('..\cookies\youtubecookie.pkl')        

    source = crawl.get_source()
    crawl.close()

    extract_data(source, args)

    return

def explore(args):
    """
    get details like titles, links, views and posted ago of videos in explore section
    """

    crawl = crawler('https://www.youtube.com/feed/explore')
    crawl.Selenium()
    source = crawl.get_source()
    crawl.driver.implicitly_wait(15)

    # scroll to bottom of page
    crawl.driver.execute_script(
            'window.scrollTo(0, document.getElementById("page-manager").scrollHeight);')
    crawl.close()

    extract_data(source, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='process some args')

    parser.add_argument('--feed', choices=['explore', 'subscriptions'], type= str, default= 'explore',
      help='to select between viewing explore feed or subsciption feed. ' 
            'to view Subscription feed you must provide your --id and pass. ')
    parser.add_argument('--id', type=str,
      help='email id to login into your Youtube account')
    parser.add_argument('--pwd', type=str, default='',
      help='password to email id to login into your Youtube account')           
    parser.add_argument('--titles', action='store_false',
      help='to enable Titles in output and enabled by default. ')
    parser.add_argument('--views', action='store_false',
      help='to enable Views count in output and enabled by default. ')
    parser.add_argument('--postedago', action='store_false',
      help='to enable video Posted ago in output and enabled by default. ')
    parser.add_argument('--links', action='store_false',
      help='to enable links of the videos in output and enabled by default. ')
    parser.add_argument('--v', action='store_false',
      help='to enable show data in commandline in output and enabled by default. ')
    parser.add_argument('--cookie', action='store_false',
      help='to enable use of cookie to login to last used account')  

    args = parser.parse_args()  

    if args.feed == 'subscriptions':
        subsciptions(args)
    else:
        explore(args)