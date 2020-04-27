from django.db import models
import datetime
from jsonfield import JSONField

class Projects(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    
class Images(models.Model):
    originalName = models.CharField(max_length=30)
    link = models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d')
    externalLink = models.CharField(max_length=100)
    localPath = models.CharField(max_length=100)
    labeled = models.BooleanField(default=False)
    lastEdited = models.DateField()
    project = models.ForeignKey(Projects,  on_delete=models.CASCADE)
    labelData = models.TextField()

    def __str__(self):
        return self.originalName
    

class FormPart(models.Model):
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=22)
    project = models.ForeignKey(Projects, related_name='forms', on_delete=models.CASCADE)
    def __str__(self):
        return self.name


# class Figures(models.Model):
#     type = moods.CharField(max_length=100)
class TracingOptions(models.Model): 
    trace = models.CharField(max_length=10)
    enable = models.BooleanField(default=False)
    smoothing = models.IntegerField()


class Figures(models.Model):
    type = models.CharField(max_length=100)
    color = models.CharField(max_length=10)
    tracingOptions = models.OneToOneField(TracingOptions, on_delete=models.CASCADE)
    formId = models.ForeignKey(FormPart, on_delete=models.CASCADE)
    imageFigures = models.ForeignKey(Images, related_name="imageFigures", on_delete=models.CASCADE)


class Point(models.Model):
    lng = models.FloatField()
    lat = models.FloatField()
    figure = models.ForeignKey(Figures, related_name="points" , on_delete=models.CASCADE)


