import requests
import re
import pandas as pd

from bs4 import BeautifulSoup as bs

BASE_URL = 'https://vk.com'
GROUP_URL = 'https://vk.com/@yvkurse'
CSV_FILE = 'yvkurse_articles.csv'
CSV_FIELDS = {
    'TITLE': 'Заголовок',
    'TEXT': 'Текст статьи',
    'IMAGE_URL': 'ImageURL'
}


class Scraper:
    """
    Class for parsing articles from VK group and saving to CSV

    Methods
    -------
    scrape()
            Performs parsing articles from VK group

    save_csv()
            Performs saving parsed data to CSV
            
    process_data()
            Main method performing processing articles. It calling methods scrape() and save_csv()
    """
    def __init__(self):
        self.url = GROUP_URL
        self.csv_file = CSV_FILE
        self.session = requests.Session()

    def scrape(self):
        print('Scraping ...')
        self.articles = []
    
        # get group page
        response = self.session.get(self.url)

        soup = bs(response.text, 'lxml')
        article_elements = soup.findAll('div', {'class': 'author-page-article'})
    
        for article_element in article_elements:
            title = article_element.find('span', {'class': 'author-page-article__title'}).text
            
            # open article page
            link_element = article_element.find('a', {'class': 'author-page-article__href'})
            link = f'{BASE_URL}{link_element["href"]}'
        
            article_page = self.session.get(link)
            article_content = bs(article_page.text, 'lxml')
        
            # parse text
            text_elements = article_content.findAll('p', {'class': 'article_decoration_before'})

            text_chunks = [text_element.text for text_element in text_elements]
            text = '\n'.join(text_chunks)

            # get images
            image_elements = article_content.findAll('img', {'class': ['article_object_photo__image_blur', 'article_carousel_img']})
            image_urls = [image['src'] for image in image_elements]

            article_data = {
                'title': title,
                'text': text
            }

            for i, image_url in enumerate(image_urls):
                article_data[f'{CSV_FIELDS["IMAGE_URL"]}{i+1}'] = image_url

            self.articles.append(article_data)

    def save_csv(self):
        print('Saving csv...')
        articles_df = pd.DataFrame.from_dict(self.articles)
        articles_df.rename(columns={ 'title': CSV_FIELDS['TITLE'], 'text': CSV_FIELDS['TEXT'] }, inplace=True)
        articles_df.to_csv(self.csv_file, encoding='utf-16')

    def process_data(self):
        print('Processing data ...')
        self.scrape()
        
        self.save_csv()

def parse_articles():
    """
    Function for scraping articles from VK group. Creating Scraper object.
    """
    scraper = Scraper()
    scraper.process_data()

if __name__ == '__main__':
    parse_articles()
