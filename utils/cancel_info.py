from datetime import time
from bs4 import BeautifulSoup
import requests
import zenhan

majorname_to_initial = {'機械工学科': 'M', '電気電子工学科': 'E', '電子制御工学科': 'S',
                        '電子情報工学科': 'J', '環境都市工学科': 'C'}


class CancelObject:
    def __init__(self, cancel_info: dict):
        self.grade = cancel_info['学年']

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

        # 学科の正規化
        if self.major in majorname_to_initial:
            self.major = majorname_to_initial[self.major]
        else:
            if self.subject.split('[')[1].lstrip(' ')[-3] == '科':
                major_initial_zen = self.subject.split('[')[1].lstrip(' ')[-4]
                self.major = zenhan.z2h(major_initial_zen)
            else:
                self.major = None

        # 低学年クラスの正規化
        if self.grade <= 3:
            # 低学年
            if self.subject.split('[')[1].lstrip(' ')[-3] == '組':
                lgc_zen = self.subject.split('[')[1].lstrip(' ')[-4]
                self.low_grade_class = int(lgc_zen)
            else:
                self.low_grade_class = None
        else:
            # 高学年
            self.low_grade_class = None


class SupplementaryObject(CancelObject):
    pass


def get_by_grade(grade: int):
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
        cancel_info_dict = {'学年': grade}
        for tr in cancel.find_all('tr'):
            for th, td in zip(tr.find_all('th'), tr.find_all('td')):
                key = th.text
                value = td.text
                cancel_info_dict[key] = value

        # 休講情報オブジェクトを生成
        cancel = CancelObject(cancel_info_dict)
        returns.append(cancel)

    return returns


def just_for_you(grade: int, major: str, low_grade_class=None):
    all_cancel_in_grade = get_by_grade(grade)
    returns = []
    for cancel in all_cancel_in_grade:
        if cancel.major is None and cancel.low_grade_class is None:
            returns.append(cancel)
        elif cancel.major == major:
            returns.append(cancel)
        elif low_grade_class and cancel.low_grade_class == low_grade_class:
            returns.append(cancel)

    return returns


if __name__ == "__main__":
    myself = just_for_you(grade=1, major='M', low_grade_class=5)
