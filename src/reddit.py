from utils.crawlers import crawler
from utils.data import data
import argparse
from time import sleep


def extractdata(source, args):
    """
    extract rawdata from the website
    """
    # making lists to hold data
    file = data(source)
    lists = []
    headers = []

    # Finding op of post
    if args.name == True:
        usernames = []
        slash = file.find('div', CLASS='_2mHuuvyV9doV3zwbZPtIPG')
        for username in slash:
            if username[0] == 'u':
                usernames.append(username)
            else:
                pass            
        lists.append(usernames)
        headers.append('USERNAME')

    # finding titles
    if args.titles == True:
        titles = file.find('h3', CLASS='_eYtD2XCVieq6emjKBH3m')
        lists.append(titles)
        headers.append('TITLES')

    # finding reactions
    if args.reactions == True:
        # Finding Upvotes on a post
        upvotes = file.find('div', CLASS='_1E9mcoVn4MYnuBQSVDt1gC')
        lists.append(upvotes)
        headers.append('UPVOTES')

        # Finding no. of Comments on a post
        comments = file.find('span', CLASS='FHCV02u6Cp2zYL0fhQPsO')
        lists.append(comments)
        headers.append('COMMENTS')

    # finding posted ago
    if args.postedon == True:
        posted = file.find('span', CLASS='_2VF2J19pUIMSLJFky-7PEI')
        lists.append(posted)
        headers.append('POSTED AGO')

    # getting links of videos
    if args.links == True:
        links = []
        href = file.find(
            'a', CLASS='SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE', type='links')
        for link in href:
            links.append("https://www.reddit.com" + link)
        lists.append(links)
        headers.append('LINKS')

    # arranging data
    file.create_csv(headers)
    file.concatenate(lists)

    if args.v == True:
        print(file.view_data())

    return



def subreddit(args):
    """
    scrapes posts on your homepage
    """
    crawl = crawler('https://reddit.com/r/' + args.sub)
    crawl.Selenium()
    crawl.driver.implicitly_wait(15)
    crawl.locate_presence('CLASS', '_eYtD2XCVieq6emjKBH3m')

    height = 0
    while height <= args.pages:
        # Scroll down to bottom
        crawl.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(1)
        height = height + 1

    source = crawl.get_source()
    extractdata(source, args)
    crawl.close()
    return


def user(args):
    """
    scrapes reddit posts of given user
    """
    crawl = crawler('https://reddit.com/user/' + args.username + '/submitted/')
    crawl.Selenium()
    crawl.driver.implicitly_wait(15)
    crawl.await_element('CLASS', '_eYtD2XCVieq6emjKBH3m')

    height = 0
    while height <= args.pages:
        # Scroll down to bottom
        crawl.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(1)
        height = height + 1

    source = crawl.get_source()
    extractdata(source, args)
    crawl.close()
    return


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='How to use-\npy reddit.py --feed subreddit')

    parser.add_argument('--feed', choices=['subreddit', 'user'], type=str, default='subreddit',
                        help='to select between viewing subreddit feed or user feed. ')
    parser.add_argument('--username', type=str,
                        help='user you want to scrape posts from ')
    parser.add_argument('--sub', type=str, default='popular',
                        help='subreddit you want to scrape posts from ')
    parser.add_argument('--pages', type=int, default= 10,
                        help='no. of times to scroll down or pages to include in the result'
                        'higher no. means more posts will be included in output, default is 10. ')                    
    parser.add_argument('--titles', action='store_false',
                        help='to enable title in output and enabled by default. ')
    parser.add_argument('--name', action='store_false',
                        help='to enable name in output and enabled by default. ')
    parser.add_argument('--postedon', action='store_false',
                        help='to enable post Posted on in output and enabled by default. ')
    parser.add_argument('--links', action='store_false',
                        help='to enable links of the post in output and enabled by default. ')
    parser.add_argument('--reactions', action='store_false',
                        help='to enable reactons on posts like upvotes and comments in output and enabled by default. ')
    parser.add_argument('--v', action='store_false',
                        help='to enable show data in commandline in output and enabled by default. ')

    args = parser.parse_args()

    if args.feed == 'user':
        user(args)
    else:
        subreddit(args)