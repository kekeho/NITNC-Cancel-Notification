from django.core.management import BaseCommand
from utils import cancel_info
from django.utils.timezone import datetime
from django.core.mail import BadHeaderError, send_mail
from notify.models import Cancel


def date_normalize(cancel: Cancel):
    if cancel.cancel_date:
        if cancel.cancel_date == '未定':
            cancel.cancel_date = None
        else:
            string_cancel_date = cancel.cancel_date  # 2018年12月18日[3-4時限]
            # 2018年12月18日
            string_cancel_date = string_cancel_date.split('[')[0]
            year, without_year = string_cancel_date.split('年')  # 2018, 12月18日
            month, without_month = without_year.split('月')  # 12, 18日
            day = without_month[:-1]

            cancel.cancel_date = datetime(year=int(year), month=int(month),
                                          day=int(day))

    if cancel.supplementary_date:
        if cancel.supplementary_date == '未定':
            cancel.supplementary_date = None
        else:
            # 2018年12月18日[3-4時限]
            string_supplementary_date = cancel.supplementary_date
            # 2018年12月18日
            string_supplementary_date = string_supplementary_date.split('[')[0]
            # 2018, 12月18日
            year, without_year = string_supplementary_date.split('年')
            month, without_month = without_year.split('月')  # 12, 18日
            day = without_month[:-1]

            cancel.supplementary_date = datetime(year=int(year),
                                                 month=int(month),
                                                 day=int(day))

    return cancel


def send_upload_email(cancel: Cancel):
    if cancel.low_grade_class is None:
        lgc = ''
    else:
        lgc = cancel.low_grade_class + '組'

    if cancel.major is None:
        major = ''
    else:
        major = cancel.major + '科'

    subject = f'【更新】{cancel.subject}の休講・補講'
    message = f"""NITNC 休講・補講サービスです。
    {cancel.subject}の休講及び補講情報が更新されましたので通知します。

    通知対象: {cancel.grade}年{lgc}{major}
    科目名: {cancel.subject}
    休講日: {cancel.cancel_date}
    補講日: {cancel.supplementary_date}
    場所: {cancel.place}
    学科: {major}
    教員: {cancel.teacher}
    備考: {cancel.memo}
    """

    from_email = "information@nitncnotify"

    recipient_list = [
        'hirodora@me.com'
    ]

    send_mail(subject, message, from_email, recipient_list)


class Command(BaseCommand):
    help = '休講・補講情報を取得後、DBに保存'

    def handle(self, *args, **options):
        cancels = []
        for grade in range(1, 5+1):
            cancels += cancel_info.get_by_grade(grade)

        for cancel in cancels:
            cancel = date_normalize(cancel)
            new_cancel = Cancel(grade=cancel.grade,
                                cancel_date=cancel.cancel_date,
                                supplementary_date=cancel.supplementary_date,
                                subject=cancel.subject, place=cancel.place,
                                major=cancel.major,
                                low_grade_class=cancel.low_grade_class,
                                teacher=cancel.teacher, memo=cancel.memo)
            
            # 重複するものを検索
            exist = Cancel.objects.filter(grade=cancel.grade,
                                          cancel_date=cancel.cancel_date,
                                          supplementary_date=cancel.supplementary_date,
                                          subject=cancel.subject,
                                          place=cancel.place,
                                          major=cancel.major,
                                          low_grade_class=cancel.low_grade_class,
                                          teacher=cancel.teacher, memo=cancel.memo)
            
            if exist:
                # 重複がある場合は無視
                continue
            else:
                send_upload_email(new_cancel)
                new_cancel.save()
