from rest_framework import viewsets
from .models import  Projects, Images, FormPart, Figures, TracingOptions, Point
from .serializers import  ProjectSerializer, ImageSerializer, FormPartSerializer, PointSerializer, TracingOptionSerializer, FigureSerializer
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer

class FormPartViewSet(viewsets.ModelViewSet):
    queryset = FormPart.objects.all()
    serializer_class = FormPartSerializer


class PointViewSet(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class FigureViewSet(viewsets.ModelViewSet):
    queryset = Figures.objects.all()
    serializer_class = FigureSerializer


class TrancingViewSet(viewsets.ModelViewSet):
    queryset = TracingOptions.objects.all()
    serializer_class = TracingOptionSerializer


@csrf_exempt
def Images_Detail(request, projectId, imageId):
   
    try:
        # snippet = Snippet.objects.get(pk=pk)
        project = Projects.objects.get(pk=projectId)
        image = Images.objects.get(pk=imageId)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        # serializer = SnippetSerializer(snippet)
        # return JsonResponse(serializer.data)
        projectSerializer = ProjectSerializer(project)
        imageSerializer = ImageSerializer(image)
        jsonData = {}
        labels = {}
        for label in projectSerializer.data['forms']:
            labels[label['id']] = []
        
        for figure in imageSerializer.data['imageFigures']:
            labelId = figure['formId']
            labels[labelId].append(figure)
        image = {
            "id": imageSerializer.data["id"],
            "originalName": imageSerializer.data['originalName'],
            "link": imageSerializer.data['link'],
            "externalLink": '',
            "localPath": '',
            "labeled": imageSerializer.data['labeled'],
            "labelData": {
                "labels": labels,
            }        
        }


        jsonData['project'] = projectSerializer.data
        jsonData['image'] = image
        return JsonResponse(jsonData)
    # elif request.method == 'PUT':
    #     # data = JSONParser().parse(request)
    #     # serializer = SnippetSerializer(snippet, data=data)
    #     # if serializer.is_valid():
    #     #     serializer.save()
    #     #     return JsonResponse(serializer.data)
    #     # return JsonResponse(serializer.errors, status=400)

    # elif request.method == 'DELETE':
    #     # snippet.delete()
    #     # return HttpResponse(status=204)


    #  image: {
    #         id: 1,
    #         originalName: 'demo.jpg',
    #         link: demoImg,
    #         externalLink: null,
    #         localPath: null,
    #         labeled: 0,
    #         labelData: {
    #           labels: {
    #             // mzs64divv: [
    #             //   {
    #             //     id: 'hpctbyvju7k5t68znsphx3',
    #             //     type: 'polygon',
    #             //     points,
    #             //     tracingOptions: {
    #             //       trace: [],
    #             //       enabled: false,
    #             //       smoothing: 1.2,
    #             //     },
    #             //   },
    #             //   {
    #             //     id: 'hpctbyvju7k5t68znsphx4',
    #             //     type: 'polygon',
    #             //     points: points2,
    #             //     tracingOptions: {
    #             //       trace: [],
    #             //       enabled: false,
    #             //       smoothing: 1.2,
    #             //     },
    #             //   },
    #             // ],
    #           },
    #         },
    #         lastEdited: 1552629203129,
    #         projectsId: 'demo',
    #       },