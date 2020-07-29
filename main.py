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
        post_elements = soup.findAll('div', {'class': 'author-page-article'})
    
        for post_element in post_elements:
            title = post_element.find('span', {'class': 'author-page-article__title'}).text
            
            image_element = post_element.find('div', {'class': 'author-page-article__preview'})
            image_url1 = re.search(r'\((.*?)\)', image_element['style']).group(1)

            # open article page
            link_element = post_element.find('a', {'class': 'author-page-article__href'})
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
                article_data[f'{CSV_FIELDS["IMAGE_URL"]}{i}'] = image_url

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

def parse_posts():
    """Function for scraping"""
    scraper = Scraper()
    scraper.process_data()

if __name__ == '__main__':
    parse_posts()
