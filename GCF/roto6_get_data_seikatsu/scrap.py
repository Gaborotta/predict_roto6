from urllib import request
from bs4 import BeautifulSoup
import re

# 過去全て
# SETTINGS = {
#     "LOTO6": {"table": "bun_box1", "title": "w7", "main": "w4", "bonus": "w6", "url": 'http://sougaku.com/loto6/data/list1/'},
#     "LOTO7": {"table": "bun_box2", "title": "w6", "main": "w5", "bonus": "w4", 'url': 'http://sougaku.com/loto7/data/list1/'},
#     "MINI_LOTO": {"table": "bun_box2", "title": "w6", "main": "w5", "bonus": "w4", 'url': 'http://sougaku.com/miniloto/data/list1/'},
# }

# 最新10件
SETTINGS = {
    "LOTO6": {"table": "bun_box1", "title": "w7", "main": "w4", "bonus": "w6", "url": 'http://sougaku.com/loto6/data/list1/index_10.html'},
    "LOTO7": {"table": "bun_box2", "title": "w6", "main": "w5", "bonus": "w4", 'url': 'http://sougaku.com/loto7/data/list1/index_10.html'},
    "MINI_LOTO": {"table": "bun_box2", "title": "w6", "main": "w5", "bonus": "w4", 'url': 'http://sougaku.com/miniloto/data/list1/index_10.html'},
}


def clean_txt(txt):
    return re.sub(r'[\.\r\n\t, ]', '', txt)


def get_results(loto_name="LOTO7"):

    setting = SETTINGS[loto_name]
    url = setting["url"]
    html = request.urlopen(url)

    soup = BeautifulSoup(html, "html.parser")
    result_list = (
        soup.find('table', class_=setting["table"])
        .find('tbody')
        .find_all('tr')
    )

    res_dict = []
    for res in result_list:
        if len(res.find_all('th')) > 0:
            continue

        res_dict.append(
            {
                "title": clean_txt(res.find(class_=setting["title"]).text),
                "main": [clean_txt(r.text) for r in res.find_all(class_=setting["main"])],
                "bonus": [clean_txt(r.text) for r in res.find_all(class_=setting["bonus"])],
                "set": clean_txt(res.find(class_="").text)
            }
        )
    return res_dict
