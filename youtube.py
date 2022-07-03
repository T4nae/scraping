from utils.crawlers import crawler
from utils.data import data
from bs4 import BeautifulSoup
import csv

def explore():
    """
    get details like titles, links, views and posted ago of videos in explore section
    """

    crawl = crawler('https://www.youtube.com/feed/explore')
    source = crawl.Selenium()
   
    crawl.driver.execute_script(
            'window.scrollTo(0, document.getElementById("page-manager").scrollHeight);')
    crawl.close()

    # making soup and lists
    soup = BeautifulSoup(source, 'lxml')
    titles = []
    links = []
    views = []
    posted = []

    # finding titles from explore section
    titles_selector = soup.find_all(
        'a', class_='yt-simple-endpoint style-scope ytd-video-renderer')

    for title_selector in titles_selector:
        title = title_selector.get_text()
        titles.append(title)

    # getting links of explore section
    links_selector = soup.find_all(
        'a', class_='yt-simple-endpoint style-scope ytd-video-renderer')
    for link_selector in links_selector:
        link = link_selector.get('href')
        links.append("https://www.youtube.com" + link)

    # finding views and posted ago
    views_selector = soup.find_all(
        'span', class_='style-scope ytd-video-meta-block')
    for view_selector in views_selector:
        view = view_selector.get_text()
        if view.endswith("ago"):
            posted.append(view)
        else:
            views.append(view)

    # arranging data        
    file = data()
    file.concatenate(titles,views,posted,links)

    return file


if __name__ == "__main__":
    file = explore()
    print(file.view_data())
