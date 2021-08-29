import re
from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime
from functools import reduce
import IPython


def clean_txt(txt):
    return re.sub(r'[\.\r\n\t, ]', '', txt)


def get_row_datas(tds):
    res_dict = {
        'title': clean_txt(tds[0].text),
        'date': re.sub(r'[年月]', '-', clean_txt(tds[1].text)).replace('日', ''),
        'numbers': [int(clean_txt(tds[i].text)) for i in range(2, 8)],
        'number_B': int(clean_txt(tds[8].text)),
        'first_hits': int(clean_txt(tds[9].text)),
        'first_amount': int(clean_txt(tds[10].text)),
        'second_hits': int(clean_txt(tds[11].text)),
        'second_amount': int(clean_txt(tds[12].text)),
        'third_hits': int(clean_txt(tds[13].text)),
        'third_amount': int(clean_txt(tds[14].text)),
        'fourth_hits': int(clean_txt(tds[15].text)),
        'fourth_amount': int(clean_txt(tds[16].text)),
        'fifth_hits': int(clean_txt(tds[17].text)),
        'fifth_amount': int(clean_txt(tds[18].text)),
        'carryover': int(clean_txt(tds[19].text)),
    }
    return res_dict


def get_numbers_roto(target_times='loto61551'):

    url = f'https://takarakuji-loto.jp/loto6-mini/{target_times}.html'

    # 検索結果のページのHTMLをBeautifulSoupに流し込む
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all(class_='tb1 resulttb text12')

    res_tables = reduce(
        lambda a, b: a + b,
        [
            table.find_all('tr')[2:]
            for table in tables
        ]
    )
    res = [
        get_row_datas(tr.find_all('td'))
        for tr in res_tables
        if tr.find_all('td')[1].text != ''
    ]
    return res


def get_index():
    url = 'https://takarakuji-loto.jp/tousenlist/loto6.html'

    # 検索結果のページのHTMLをBeautifulSoupに流し込む
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find(class_='bg w95').find_all('a')

    targets = [
        l_tag['href'].split('/')[-1].split('.')[0]
        for l_tag in links
    ]

    return targets
