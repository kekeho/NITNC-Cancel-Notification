from datetime import time
from bs4 import BeautifulSoup
import requests


class CancelObject:
    def __init__(self, subject: str, major: str or None, grade: int,
                 low_grade_class: int or None, date: time, koma: str,
                 place: str, supplementary_date: time,
                 supplementary_koma: str, teacher: str, memo: str):
        self.subject = subject
        self.major = major
        self.grade = grade
        self.low_grade_class = low_grade_class
        self.date = date
        self.koma = koma
        self.place = place
        self.supplementary_date = supplementary_date
        self.supplementary_koma = supplementary_koma
        self.teacher = teacher
        self.memo = memo


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
    for cancel in cancels:
        print('=======')
        print(cancel)


if __name__ == "__main__":
    get_info(1)
