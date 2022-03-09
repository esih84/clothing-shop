from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from .models import *
from .serializers import profileserializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from  django.http import  HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
# Create your views here.





@api_view(['POST'])
def problem_view(request):
    if request.method == "POST":
        if not request.data['desc']:
            raise ValueError("title nust be valid")
        question = user_problem.objects.create(desc=request.data['desc'], user_id=request.user.user_id)
        question.save()
        return HttpResponse("ok")


def answer(request):
    context = {
        'answers': user_problem.objects.filter(user_id=request.user.user_id)
    }
    return render(request, 'user_problems/answer_question.html', context)



@api_view(['POST'])
def api_login(request):
    if request.method == "POST":
        username = request.data['email']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("ok")
        else:
            return HttpResponse("no")






@api_view(['POST'])
def profile_api(request):
    if request.method == "POST":
        profile_serializer = profileserializers(data=request.data)
        print(profile_serializer)
        if profile_serializer.is_valid():
            profile_serializer.save(user_id=request.user.user_id)
            return HttpResponse('ok')
        return HttpResponse('no')
