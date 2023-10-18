from django.contrib import admin
from .models import Lecture, Category, LectureView
# Register your models here.

class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_modified')
    

admin.site.register(Lecture, LectureAdmin)
admin.site.register(Category)
admin.site.register(LectureView)
