from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


MAJORS_DIC = {'M': '機械工学科', 'E': '電気電子工学科', 'S': '電子制御工学科',
              'J': '電子情報工学科', 'C': '環境都市工学科'}


class User(AbstractUser):
    username = models.CharField(_('username'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Grade(models.Model):
    grade = models.IntegerField(primary_key=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.grade}年"


class Major(models.Model):
    # M/E/S/J/C
    initial = models.CharField(max_length=1)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return MAJORS_DIC[self.initial]


class LowGradeClass(models.Model):
    low_grade_class = models.IntegerField(primary_key=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.low_grade_class}組"
