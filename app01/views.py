from django.shortcuts import render, redirect
from app01 import models

# Create your views here.
def depart_list(request):
    """ 部门列表 """
    # 去数据库中获取部门消息
    data_list = models.Department.objects.all()

    return render(request, 'depart_list.html', {'data_list': data_list})

def depart_add(request):
    """ 添加部门 """
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # 获取用户提交过来的数据
    title = request.POST.get("title")
    # 保存到数据库
    models.Department.objects.create(title=title)
    return redirect("/depart/list/")

def depart_delete(request):
    """ 删除部门 """
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")

def depart_edit(request, nid):
    """ 修改编辑部门 """
    if request.method == "GET":
        obj = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {'obj': obj})

    title = request.POST.get("title")
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")

def user_list(request):
    """ 用户管理 """
    queryset = models.UserInfo.objects.all()
    # for obj in queryset:
    #     print(obj.depart.title)  # 根据id自动去关联的表中获取那一行数据depart对象
    return render(request, "user_list.html", {"queryset":queryset})

def user_add(request):
    """ 添加用户 （原始方法）"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, "user_add.html", context)
    # 获取用户提交的数据
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')
    ac = request.POST.get('ac')
    ctime = request.POST.get('ctime')
    gd = request.POST.get('gd')
    dp = request.POST.get('dp')

    # 添加到数据库中
    models.UserInfo.objects.create(name=user,password=pwd,age=age,account=ac,create_time=ctime,gender=gd,depart_id=dp)

    # 添加成功后返回用户列表页面
    return redirect("/user/list")

from django import forms
class UserModelForm(forms.ModelForm):

    # 校验
    name = forms.CharField(min_length=2, label='用户名')

    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"})
        #     "password": forms.PasswordInput(attrs={"class": "form-control"})
        #     "age": forms.TextInput(attrs={"class": "form-control"})
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class=""样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
def user_model_form_add(request):
    """ 添加用户（基于ModelForm） """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {"form": form})

    # 用户POST提交数据据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据提交是对的
        form.save()  # 将提交的数据存储到数据库中
        return redirect("/user/list/")
    return render(request, 'user_model_form_add.html', {"form": form})