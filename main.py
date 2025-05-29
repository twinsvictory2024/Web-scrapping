from bs4 import BeautifulSoup as bs
import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def analyze_post(url: str):
    response = requests.get(f'https://habr.com{url}')
    if response.status_code == 200:
        # получаем все параграфы в статье в article_body
        article_body = bs(response.text, 'html.parser').find('div',
                                                             class_='article-formatted-body').find_all('p')
        for p in article_body:
            text = re.sub(r'[^\w\s]', '', p.get_text(strip=True)).lower()
            all_text.append(text)  # Добавляем текст параграфа в список

        # Объединяем весь текст в одну строку
        combined_text = "\n".join(all_text)
        if set(combined_text.split(' ')) & set(KEYWORDS):
            time = bs(response.text, 'html.parser').find(
                'span', class_='tm-article-datetime-published').find('time').get('title')
            header = bs(response.text, 'html.parser').find(
                'h1', class_='tm-title tm-title_h1').find('span').get_text(strip=True)
            return time, header, response.url


response = requests.get('https://habr.com/ru/articles/')
if response.status_code == 200:
    print('<дата> – <заголовок> – <ссылка>')
    urls = []
    # получаем все article
    articles = bs(response.text, 'html.parser').find_all('article')
    for article in articles:
        # собираем url статей с нижней кнопки
        link = article.find('a', class_='tm-title__link')
        if link:
            link = link.get('href')
            urls.append(link)
    for url in urls:
        all_text = []
        # Используем ThreadPoolExecutor для параллельных запросов
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(
            analyze_post, url): url for url in urls}
        for future in as_completed(future_to_url):
            print(future.result())
# Ваш код
