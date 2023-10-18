from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=50, unique=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Lecture(models.Model):

    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True, default=None)
    file = models.FileField(upload_to='pdf', blank=True, null=True, default=None, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    date_modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

class LectureView(models.Model):
    
    lecture = models.ForeignKey(Lecture, on_delete=models.DO_NOTHING)
    date = models.DateField()

    def __str__(self):
        return f'{self.lecture.name} viewed on {self.date}'



