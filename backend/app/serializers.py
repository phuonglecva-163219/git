from rest_framework import serializers
from .models import  Projects, Images, FormPart, Point, Figures, TracingOptions


class PointSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Point
        fields = ('lng', 'lat')

class TracingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TracingOptions
        fields = ('trace', 'enable', 'smoothing')

class FigureSerializer(serializers.ModelSerializer):
    tracingOptions = TracingOptionSerializer(required=True)
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Figures
        fields = ('id', 'type', 'color', 'points', 'tracingOptions','formId')


class FormPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormPart
        fields = ('id', 'type', 'name')

class ProjectSerializer(serializers.ModelSerializer):
    forms = FormPartSerializer(many=True,  read_only=True)
    class Meta:
        model = Projects
        fields = ('id','name', 'forms')
        

class ImageSerializer(serializers.ModelSerializer):
    imageFigures = FigureSerializer(many=True, read_only=True)
    class Meta:
        model = Images
        fields = ('id', 'originalName', 'link' , 'project', 'labeled', 'imageFigures')

    