from django.core.management import BaseCommand
from utils import cancel_info
from django.utils.timezone import datetime
from notify.models import Cancel


def date_normalize(cancel: Cancel):
    if cancel.cancel_date:
        if cancel.cancel_date == '未定':
            cancel.cancel_date = None
        else:
            string_cancel_date = cancel.cancel_date  # 2018年12月18日[3-4時限]
            # 2018年12月18日
            string_cancel_date, time = string_cancel_date.split('[')
            year, without_year = string_cancel_date.split('年')  # 2018, 12月18日
            month, without_month = without_year.split('月')  # 12, 18日
            day = without_month[:-1]

            cancel.cancel_date = datetime(year=int(year), month=int(month),
                                          day=int(day))
            cancel.cancel_time = time[:-1]

    if cancel.supplementary_date:
        if cancel.supplementary_date == '未定':
            cancel.supplementary_date = None
        else:
            # 2018年12月18日[3-4時限]
            string_supplementary_date = cancel.supplementary_date
            # 2018年12月18日
            string_date, time = string_supplementary_date.split('[')
            # 2018, 12月18日
            year, without_year = string_date.split('年')
            month, without_month = without_year.split('月')  # 12, 18日
            day = without_month[:-1]

            cancel.supplementary_date = datetime(year=int(year),
                                                 month=int(month),
                                                 day=int(day))
            cancel.supplementary_time = time[:-1]

            

    return cancel


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
                                cancel_time=cancel.cancel_time,
                                supplementary_date=cancel.supplementary_date,
                                supplementary_time=cancel.supplementary_time,
                                subject=cancel.subject, place=cancel.place,
                                major=cancel.major,
                                low_grade_class=cancel.low_grade_class,
                                teacher=cancel.teacher, memo=cancel.memo)
            
            # 重複するものを検索
            exist = Cancel.objects.filter(grade=cancel.grade,
                                          cancel_date=cancel.cancel_date,
                                          cancel_time=cancel.cancel_time,
                                          supplementary_date=cancel.supplementary_date,
                                          supplementary_time=cancel.supplementary_time,
                                          subject=cancel.subject,
                                          place=cancel.place,
                                          major=cancel.major,
                                          low_grade_class=cancel.low_grade_class,
                                          teacher=cancel.teacher, memo=cancel.memo)
            
            if exist:
                # 重複がある場合は無視
                continue
            else:
                # send_upload_email(new_cancel)
                new_cancel.save()
