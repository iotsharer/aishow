#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/8/1 10:35
# @Author : LiFH
# @Site : 
# @File : index.py
# @Software: PyCharm Community Edition

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from model.sceneRecognition.main import *
from model.superResolution.main import *

def save_img(request):
    filename = os.path.dirname(__file__)
    myFile = request.FILES.get("img-name", None)  # 获取上传的文件，如果没有文件，则默认为None
    if not myFile:
        return HttpResponse("no files for upload!")
        # return HttpResponse(request,"upload_form.html")
    img_name = os.path.join(filename + "/upload/", myFile.name)
    destination = open(img_name, 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    return img_name


@csrf_exempt
def sceneRecognition(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        img_name = save_img(request)
        # 放入CNN模块计算
        result = run_placesCNN(img_name)
        ctx = {}
        ctx['result'] = result
        return JsonResponse(ctx)
    return HttpResponse("error!!")

@csrf_exempt
def faceRecognition(request):
    ctx = {}
    ctx['name'] = "人脸识别"
    return JsonResponse(ctx)

@csrf_exempt
def sexRecognition(request):
    if request.method == "POST":
        ctx = {}
        ctx['name'] = "色情识别"
        return JsonResponse(ctx)

@csrf_exempt
def superResolution(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        img_name = save_img(request)
        # 放入CNN模块计算
        print(img_name)
        result = SR(img_name)
        ctx = {}
        ctx['result'] = result
        return JsonResponse(ctx)
    return HttpResponse("error!!")
