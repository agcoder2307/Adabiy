from . import model_text
from .punctuation_forserver import inference
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, serializers
from . import models
# Create your views here.


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Text
        fields = '__all__'

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def CheckText(request):
    data = request.data

    text = data['data']
    array = []
    for t in text:
        checked_text = model_text.candidates(t) 
        array.append(checked_text)
    write = models.Text.objects.create(
        checkText = str(array)
    )
  

    return Response(array)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def CheckPunctuation(request):
    data = request.data
    text = data['text']
    print(type(text))
    punctuation_text = inference.inference(text)
   
    
    return Response(str(punctuation_text))