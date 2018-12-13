from datetime import time
from bs4 import BeautifulSoup
import requests


class CancelObject:
    def __init__(self, cancel_info: dict):
        try:
            self.cancel_date = cancel_info['休講日']
        except KeyError:
            self.cancel_date = None

        try:
            self.supplementary_date = cancel_info['補講日']
        except KeyError:
            self.supplementary_date = None

        try:
            self.subject = cancel_info['科目名']
        except KeyError:
            self.subject = None

        try:
            self.place = cancel_info['教室']
        except KeyError:
            self.place = None

        try:
            self.major = cancel_info['学科']
        except KeyError:
            self.major = None

        try:
            self.teacher = cancel_info['教員']
        except KeyError:
            self.teacher = None

        try:
            self.memo = cancel_info['備考']
        except KeyError:
            self.memo = None


class SupplementaryObject(CancelObject):
    pass


def get_info(grade: int):
    if grade == 1:
        url_grade = '1st'
    elif grade == 2:
        url_grade = '2nd'
    elif grade == 3:
        url_grade = '3rd'
    else:
        url_grade = f'{grade}th'

    html = requests.get(
        f"http://www.nagano-nct.ac.jp/current/cancel_info_{url_grade}.php"
        ).content
    soup = BeautifulSoup(html, 'html.parser')

    # 休講及び補講情報を全件取得
    cancels = soup.find_all('table', class_='cancel')

    returns = []
    for cancel in cancels:
        cancel_info_dict = {}
        for tr in cancel.find_all('tr'):
            for th, td in zip(tr.find_all('th'), tr.find_all('td')):
                key = th.text
                value = td.text
                cancel_info_dict[key] = value

        # 休講情報オブジェクトを生成
        cancel = CancelObject(cancel_info_dict)
        returns.append(cancel)

    return returns


if __name__ == "__main__":
    get_info(4)
