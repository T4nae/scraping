from utils.crawlers import crawler
from utils.data import data
from bs4 import BeautifulSoup
from getpass import getpass
import argparse

def subsciptions(args):
    """
    get video details from the subscriptions feed
    """

    crawl = crawler('https://www.youtube.com/feed/subscriptions')
    crawl.Selenium(False)
    crawl.driver.implicitly_wait(15)

    if crawl.locate_presence('LINK', 'SIGN IN'):
        crawl.find('LINK', 'SIGN IN').click()
        pwd = getpass('Enter Password:')
 
        loginBox = crawl.find('XPATH', '//*[@id ="identifierId"]')
        loginBox.send_keys(args.id)
        nextButton = crawl.find('XPATH', '//*[@id ="identifierNext"]')
        nextButton.click()
        passWordBox = crawl.find('XPATH', '//*[@id ="password"]/div[1]/div / div[1]/input')
        passWordBox.send_keys(pwd)
        nextButton = crawl.find('XPATH', '//*[@id ="passwordNext"]')
        nextButton.click()

    source = crawl.get_source()
    crawl.close()

    #print(source)

  
    
    return

def explore(args):
    """
    get details like titles, links, views and posted ago of videos in explore section
    """

    crawl = crawler('https://www.youtube.com/feed/explore')
    crawl.Selenium()
    source = crawl.get_source()
    crawl.driver.implicitly_wait(15)

    crawl.driver.execute_script(
            'window.scrollTo(0, document.getElementById("page-manager").scrollHeight);')
    crawl.close()

    # making soup and lists
    soup = BeautifulSoup(source, 'lxml')
    titles = []
    links = []
    views = []
    posted = []
    lists = []
    headers = []

    # finding titles from explore section
    if args.titles == True:
        titles_selector = soup.find_all(
            'a', class_='yt-simple-endpoint style-scope ytd-video-renderer')

        for title_selector in titles_selector:
            title = title_selector.get_text()
            titles.append(title)
        lists.append(titles)
        headers.append('TITLES')


    # finding views and posted ago
    if args.views == True or args.postedon == True:
        views_selector = soup.find_all(
            'span', class_='style-scope ytd-video-meta-block')
        for view_selector in views_selector:
            view = view_selector.get_text()
            if view.endswith("ago"):
                posted.append(view)
            else:
                views.append(view)
        if args.views == True:
            lists.append(views)
            headers.append('VIEWS')
        if args.postedon == True:
            lists.append(posted)
            headers.append('POSTED')

    # getting links of explore section
    if args.links == True:
        links_selector = soup.find_all(
            'a', class_='yt-simple-endpoint style-scope ytd-video-renderer')
        for link_selector in links_selector:
            link = link_selector.get('href')
            links.append("https://www.youtube.com" + link)
        lists.append(links)
        headers.append('LINKS')  
        

    # arranging data
    file = data()
    file.create_csv(headers)
    file.concatenate(lists)

    if args.v == True:
        print(file.view_data())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='process some args')

    parser.add_argument('--feed', choices=['explore', 'subscriptions'], type= str,
      help='to select between viewing explore feed or subsciption feed. ' 
            'to view Subscription feed you must provide your --id and pass. ')
    parser.add_argument('--id', type=str,
      help='email id to login into your Youtube account')     
    parser.add_argument('--titles', type=bool, default=True,
      help='to enable Titles in output and enabled by default. ')
    parser.add_argument('--views', type=bool, default=True,
      help='to enable Views count in output and enabled by default. ')
    parser.add_argument('--postedon', type=bool, default=True,
      help='to enable video Posted ago in output and enabled by default. ')
    parser.add_argument('--links', type=bool, default=True,
      help='to enable links of the videos in output and enabled by default. ')
    parser.add_argument('--v', type=bool , default=True,
      help='to enable show data in commandline in output and enabled by default. ')  

    args = parser.parse_args()  

    if args.feed == 'subscriptions':
        subsciptions(args)
    else:
        explore(args)