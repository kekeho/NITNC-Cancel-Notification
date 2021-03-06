from django.db import models


class Cancel(models.Model):
    grade = models.IntegerField(blank=False, null=False)
    cancel_date = models.DateTimeField(blank=True, null=True)
    supplementary_date = models.DateTimeField(blank=True, null=True)
    subject = models.CharField(max_length=100, blank=False, null=False)
    place = models.CharField(max_length=100, blank=True, null=True)
    major = models.CharField(max_length=1, blank=True, null=True)  # イニシャル
    low_grade_class = models.IntegerField(blank=True, null=True)
    teacher = models.CharField(max_length=50, blank=True, null=True)
    memo = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.grade}{self.major}{self.low_grade_class} {self.subject}'
