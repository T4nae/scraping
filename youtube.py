from utils.crawlers import crawler
from bs4 import BeautifulSoup

def extract_title():
    """
    extract yt titles from source
    """

    crawl = crawler('https://www.youtube.com/feed/explore')
    source = crawl.Selenium()
    #sleep(2)                                  # for some reason script dont work if page is not loaded first
    crawl.driver.execute_script(
            'window.scrollTo(0, document.getElementById("page-manager").scrollHeight);')
    crawl.close()
    # making soup
    soup = BeautifulSoup(source, 'lxml')
    videos = []

    # finding needed divs of source
    videos_selector = soup.find_all(
        'a', class_='yt-simple-endpoint style-scope ytd-video-renderer')

    # iterating and extractig needed data
    for video_selector in videos_selector:
        title = video_selector.get_text()
        videos.append(title)

    return videos

def extract_links():
    """
    extract yt links from source
    """

    crawl = crawler('https://www.youtube.com/feed/explore')
    source = crawl.Selenium()
    #sleep(2)                                  # for some reason script dont work if page is not loaded first
    crawl.driver.execute_script(
            'window.scrollTo(0, document.getElementById("page-manager").scrollHeight);')
    crawl.close()
    # making soup
    soup = BeautifulSoup(source, 'lxml')
    links = []

    # finding needed divs of source
    links_selector = soup.find_all(
        'a', class_='yt-simple-endpoint style-scope ytd-video-renderer')
    for links in links_selector:
        print(links.get('href'))

"""
    # iterating and extractig needed data
    for video_selector in videos_selector:
        title = video_selector.get_text()
        videos.append(title)

    return videos

"""
if __name__ == "__main__":
    #print(extract_title())
    extract_links()
