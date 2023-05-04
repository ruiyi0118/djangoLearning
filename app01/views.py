from django.core.exceptions import ValidationError
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
    return render(request, "user_list.html", {"queryset": queryset})


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
    models.UserInfo.objects.create(name=user, password=pwd, age=age, account=ac, create_time=ctime, gender=gd,
                                   depart_id=dp)

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


def user_edit(request, nid):
    """ 编辑用户 """
    if request.method == 'GET':
        # 根据ID去数据库获取要编辑的那一行的数据
        row_object = models.UserInfo.objects.filter(id=nid).first()

        # instance=row_object将每个值在text框中显示出来，预显示
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    row_object = models.UserInfo.objects.filter(id=nid).first()
    # instance=row_object 更新数据，不加这个是添加
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    """ 删除用户 """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def pretty_list(request):
    """ 靓号列表 """
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["mobile__contains"] = value

    data_list = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    return render(request, 'pretty_list.html', {'data_list': data_list, "search_data": value})


from django.core.validators import RegexValidator


class PrettyModelForm(forms.ModelForm):
    # 验证方法1：通过正则表达式校验
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')],
    )

    class Meta:
        model = models.PrettyNum
        # fields = ["mobile","price","level","status"]
        # exclude = ['level']  除了level全都带
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class=""样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证方法2：钩子方法
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        if models.PrettyNum.objects.filter(mobile=txt_mobile).exists():
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        return txt_mobile

def pretty_add(request):
    """ 添加靓号 """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    # 用户POST提交数据据，数据校验
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据提交是对的
        form.save()  # 将提交的数据存储到数据库中
        return redirect("/pretty/list/")
    return render(request, 'pretty_add.html', {"form": form})

class PrettyExitModelForm(forms.ModelForm):
    # 手机号不可更改，但显示
    mobile = forms.CharField(disabled=True, label='手机号')
    class Meta:
        model = models.PrettyNum
        # fields = ["mobile","price","level","status"]
        # exclude = ['level']  除了level全都带
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class=""样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

def pretty_edit(request, nid):
    """ 编辑靓号 """
    if request.method == 'GET':
        # 根据ID去数据库获取要编辑的那一行的数据
        row_object = models.PrettyNum.objects.filter(id=nid).first()

        # instance=row_object将每个值在text框中显示出来，预显示
        form = PrettyExitModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})

    row_object = models.PrettyNum.objects.filter(id=nid).first()
    # instance=row_object 更新数据，不加这个是添加
    form = PrettyExitModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, 'pretty_edit.html', {'form': form})

def pretty_delete(request, nid):
    """ 删除靓号 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')