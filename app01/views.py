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