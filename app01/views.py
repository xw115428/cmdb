# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse
from app01 import models
import json
from pages.page import PagerHelper
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django import views

'''
from django.utils.decorators import method_decorator
def outer(func):
    def inner(request,*args,**kwargs):
        print request.method
        return func(request,*args,**kwargs)
    return inner
class Login(views.View):
    @method_decorator(outer)
    def dispatch(self, request, *args, **kwargs):
        print 111
        ret=super(Login,self).dispatch(request,*args,**kwargs)
        return ret

    # @method_decorator(outer)
    def get(self,request,*args,**kwargs):
        return render(request,"login.html",{"message":""})

    # @method_decorator(outer)
    def post(self,request,*args,**kwargs):
        user=request.POST.get('user')
        passwd=request.POST.get('passwd')
        obj=administrator.objects.filter(user=user,passwd=passwd).count()
        if obj:
            request.session['is_login']=True
            request.session['username']=user
            request.session.set_expiry(5)
            return redirect('/index')
        else:
            message="用户名或密码错误"
            return render(request,"login.html",{"message":message})
'''
def login(request):
    message=""
    if request.method=="POST":
        user=request.POST.get('user')
        passwd=request.POST.get('passwd')
        obj=models.administrator.objects.filter(user=user,passwd=passwd).count()
        if obj:
            request.session['is_login'] = True
            request.session['username'] = user
            request.session.set_expiry(6000)
            return redirect('/index')
        else:
            message="用户名密码错误"
    return render(request,"login.html",{"message":message})

def auth(func):
    def inner(request,*args,**kwargs):
        is_login=request.session.get('is_login')
        if is_login:
            return func(request,*args,**kwargs)
        else:
            return redirect('/login')
    return inner

@auth
def index(request):
    username=request.session.get("username")
    return render(request,"index.html",{"username":username})

@auth
def classes(request):
    if request.method=="GET":
        username=request.session.get("username")
        #当前页
        current_page=request.GET.get('p',1)
        current_page=int(current_page)
        #所有数据的个数
        total_count=models.classes.objects.all().count()


        obj=PagerHelper(total_count,current_page,'/classes.html',5)
        pager=obj.pager_str()
        cl_list=models.classes.objects.all()[obj.db_start:obj.db_end]
        return render(request,"classes.html",{"username":username,"cl_list":cl_list,'str_pager':pager})
    elif request.method=="POST":
        #submit提交
        '''
        caption=request.POST.get("caption")
        obj = models.classes.objects.create(caption=caption)
        print "caption:",caption
        return redirect("classes.html")
        '''
        #ajax提交
        import json
        if request.POST.has_key("add_caption"):
            caption=request.POST.get("add_caption")
            print caption
            cap={"status":True,"mes":None,"data":None}
            if caption:
                obj=models.classes.objects.filter(caption=caption).count()
                if not obj:
                    obj=models.classes.objects.create(caption=caption)
                    cap["data"]={"caption":obj.caption}
                else:
                    cap["status"] = False
                    cap["mes"] = "班级名已存在，请重新输入"

            else:
                cap["status"]=False
                cap["mes"]="班级名不能为空"
            return HttpResponse(json.dumps(cap))
        elif request.POST.has_key("del_id"):
            nid=request.POST.get("del_id")
            print nid
            id_dict = {"status": True, "mes": None, "data": None}
            obj1 = models.classes.objects.filter(id=nid).count()
            if not obj1:
                id_dict["status"] = False
                id_dict["mes"] = "id不存在"
            else:
                models.classes.objects.filter(id=nid).delete()
                id_dict["mes"] = "删除成功"
                id_dict["data"]=nid
                return HttpResponse(json.dumps(id_dict))
        # elif request.POST.has_key("edit_id") and request.POST.has_key("edit_cap"):
        #
        #     nid=request.POST.get("edit_id")
        #     print nid
        #     caption=request.POST.get("edit_cap")
        #     print caption
        #     id_dict = {"status": True, "mes": None, "data": None}
        #     obj1 = models.classes.objects.filter(id=nid).count()
        #     if not obj1:
        #         id_dict["status"] = False
        #         id_dict["mes"] = "id不存在"
        #     else:
        #         models.classes.objects.filter(id=nid).update(caption=caption)
        #         # id_dict["mes"] = "删除成功"
        #         id_dict["data"]=nid
        #         return HttpResponse(json.dumps(id_dict))
@auth
def add_classes(request):
    mes=""
    if request.method=="GET":
        username = request.session.get("username")
        return render(request, "add_classes.html", {"username": username,"mes":mes})

    elif request.method=="POST":
        username = request.session.get("username")
        caption=request.POST.get("caption",None)


        if caption:
            models.classes.objects.create(caption=caption)
            #mes="添加班级%s成功" %caption
            #return render(request,"add_classes.html",{"username": username,"mes":mes})
            return redirect("/classes")
        else:
            mes="班级名不能为空"
            print username
            return render(request, "add_classes.html", {"username": username,"mes":mes})


    else:
        return redirect("index.html")
@auth
def teacher(request):
    username=request.session.get("username")
    return render(request,"teacher.html",{"username":username})

@auth
def student(request):
    if request.method=="GET":
        username=request.session.get("username")
        # 当前页

        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        # 所有数据的个数
        total_count = models.student.objects.all().count()


        obj = PagerHelper(total_count, current_page, '/student.html', 10)
        pager = obj.pager_str()
        cl_list = models.student.objects.all()[obj.db_start:obj.db_end]

        print cl_list
        return render(request,"student.html",{"username":username,"ret":cl_list,"str_pager":pager,"total_count":total_count})
    elif request.method=="POST":
        nid=request.POST.get("nid")
        cap = {"status": True, "mes": None, "data": None}
        obj_count=models.student.objects.filter(id=nid).count()
        if obj_count:
            models.student.objects.filter(id=nid).delete()
            cap["data"]=nid
            return HttpResponse(json.dumps(cap))
        else:
            cap["mes"]="数据不存在！"
            cap["status"]=False
            return HttpResponse(json.dumps(cap))

@auth
def add_student(request):
    if request.method=="GET":
        username = request.session.get("username")
        sel_classes=models.classes.objects.all()
        return render(request, "add_student.html", {"username": username,"obj_classes":sel_classes})
    elif request.method=="POST":
        ##submit提交
        '''
        username = request.session.get("username")
        name=request.POST.get("name")
        age=request.POST.get("age")
        email=request.POST.get("email")
        caption=request.POST.get("caption")
        print name,age,email,caption
        import re
        if name:
            pass
        else:
            mes="不能为空"
            return render(request, "add_student.html", {"username": username, "mes": mes})
        '''
        #json

        username = request.session.get("username")
        name = request.POST.get("name")
        age = request.POST.get("age")
        email = request.POST.get("email")
        caption = int(request.POST.get("caption"))
        print name,age,email,caption
        add_stu_dic = {"status": True, "mes": None, "data": None}
        if not name:
            add_stu_dic["status"]=False
            add_stu_dic["mes"]="姓名不能为空"
            add_stu_dic["data"]=age
            return HttpResponse(json.dumps(add_stu_dic))
        else:
            models.student.objects.create(name=name,age=age,email=email,caption_id=caption)
            print "添加完成"
            return HttpResponse(json.dumps(add_stu_dic))
            return redirect("/student")

@auth
def edit_student(request):
    if request.method=="GET":
        username = request.session.get("username")
        nid=request.GET.get("nid")
        obj=models.student.objects.filter(id=nid)[0]
        sel_classes = models.classes.objects.all()

        return render(request,"edit_student.html",{"username":username,"obj":obj,"obj_classes":sel_classes})
    elif request.method=="POST":
        username = request.session.get("username")
        nid=request.POST.get("nid")
        name=request.POST.get("name")
        age=request.POST.get("age")
        email=request.POST.get("email")
        caption=request.POST.get("caption")
        models.student.objects.filter(id=nid).update(name=name,age=age,email=email,caption=caption)
        add_stu_dic = {"status": True, "mes": None, "data": None}
        print "修改完成"
        return HttpResponse(json.dumps(add_stu_dic))



@auth
def adm(request):
    username=request.session.get("username")
    return render(request,"adm.html",{"username":username})

# Create your views here.
