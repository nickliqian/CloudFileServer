from django.shortcuts import render
from django.views.generic import View
from .models import Upload
from django.http import HttpResponsePermanentRedirect, HttpResponse
import random
import string
import json
import datetime


# index
class HomeView(View):
    # get请求直接获得首页
    def get(self, request):
        return render(request, "base.html", {})

    # 如果上次文件则会发送post请求
    def post(self, request):
        # request -> request.FILES ->
        # ('_files', <MultiValueDict: {'file': [<InMemoryUploadedFile: 2018-01-24 10-41-26屏幕截图.png (image/png)>]}>)
        # 如果请求中文件不为空
        if request.FILES:
            # 获得file对象, 文件名称, 文件大小 -> File对象
            file = request.FILES.get("file")
            name = file.name
            size = int(file.size)
            # 新建一个文件用于储存传输过来的文件
            with open('static/file/' + name, 'wb') as f:
                f.write(file.read())
            # 随机生成的文件编号
            code = ''.join(random.sample(string.digits, 8))
            # 构造新文件对象
            u = Upload(
                path='static/file/' + name,
                name=name,
                Filesize=size,
                code=code,
                PCIP=str(request.META['REMOTE_ADDR']),
            )
            u.save()
            # 重定向到指定页面
            return HttpResponsePermanentRedirect("/s/" + code)


# 显示视图
class DisplayView(View):
    # get请求文件编号
    def get(self, request, code):
        # 根据文件编号查找数据对象
        u = Upload.objects.filter(code=str(code))
        # 如果存在则传递对象信息，否则传递空到此页面
        if u:
            for i in u:
                i.DownloadDocount += 1
                i.save()
        return render(request, 'content.html', {"content": u})


# 个人页面
class MyView(View):
    def get(self, request):
        # 使用 request.META['REMOTE_ADDR'] 记录IP
        IP = request.META['REMOTE_ADDR']
        print(IP)
        u = Upload.objects.filter(PCIP=str(IP))
        for i in u:
            i.DownloadDocount += 1
            i.save()
        return render(request, 'content.html', {"content": u})


# 搜索页面
class SearchView(View):
    def get(self, request):
        # 查找指定对象
        name = request.GET.get("kw")
        u = Upload.objects.filter(name__icontains=name)
        data = {}
        if u:
            for i in range(len(u)):
                u[i].DownloadDocount += 1
                u[i].save()
                data[i] = {}
                data[i]['download'] = u[i].DownloadDocount
                data[i]['filename'] = u[i].name
                data[i]['id'] = u[i].id
                data[i]['ip'] = str(u[i].PCIP)
                data[i]['size'] = u[i].Filesize
                data[i]['time'] = str(u[i].Datatime.strftime('%Y-%m-%d %H:%M:%S'))
                data[i]['key'] = u[i].code
        return HttpResponse(json.dumps(data), content_type="application/json")


# 下载功能是直接打开media url
