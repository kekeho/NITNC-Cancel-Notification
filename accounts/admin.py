from django.contrib import admin
from .models import User, Grade, Major, LowGradeClass

admin.site.register([User, Grade, Major, LowGradeClass])
