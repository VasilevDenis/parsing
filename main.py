from pprint import pprint
from bs4 import BeautifulSoup
import requests
from fake_headers import Headers
import json


def make_request(url):
    headers = Headers(headers=True).generate()
    request = requests.get(url, headers=headers)
    return request


def get_vacancies(url):
    vacancies = []
    i = 0
    while True:
        url = url.replace('page_number', str(i))
        i += 1
        request = make_request(url)
        print(request.status_code)
        if request.status_code == 200:
            page = BeautifulSoup(request.text, 'html.parser')
            for link in page.find_all('a', class_='serp-item__title'):
                vacancy = {}
                url_of_a_vacancy = link.get('href')
                request_for_a_vacancy_page = make_request(url_of_a_vacancy)
                page_for_a_vacancy = BeautifulSoup(request_for_a_vacancy_page.text, 'html.parser')
                key_words_soup = page_for_a_vacancy.find_all('span', class_='bloko-tag__section bloko-tag__section_text')
                key_words = [key_word.text for key_word in key_words_soup
                             if 'Django' in key_word.text or 'Flask' in key_word.text]
                if key_words:
                    # ссылка, вилка зп, название компании, город.
                    vacancy['link'] = url_of_a_vacancy
                    vacancy['salary'] = page_for_a_vacancy.find(
                        attrs={'data-qa': 'vacancy-salary-compensation-type-net'}).text
                    vacancy['company'] = page_for_a_vacancy.find(attrs={'data-qa': 'bloko-header-2'}).text
                    vacancy['city'] = page_for_a_vacancy.find(attrs={'data-qa': 'vacancy-view-raw-address'}).text
                    vacancies.append(vacancy)
        else:
            break
    return vacancies


if __name__ == '__main__':
    link = 'https://spb.hh.ru//search/vacancy?text=python&area=1&area=2&page=page_number&hhtmFrom=vacancy_search_list'
    vacancies = get_vacancies(link)
    print(vacancies)
    with open('vacancies', 'w') as fp:
        json.dump(vacancies, fp, ensure_ascii=False)
