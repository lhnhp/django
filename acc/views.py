from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    return render(request, "acc/index.html")

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        user = authenticate(username=un, password=pw)
        if user:
            login(request, user)
            messages.success(request, f"{user} 으로 로그인하셨습니다.")
            return redirect("acc:index")
        else:
            messages.error(request, "계정정보가 일치하지 않데요!! ")
    return render(request, "acc/login.html")


def logout_user(request):
    logout(request)
    return redirect("acc:index")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        ua = request.POST.get("uage")
        co = request.POST.get("com")
        upc = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un,password=up,age=ua,comment=co,pic=upc)
        except:#username 중복시 
            messages.warning(request, "이미 등록되어 있는 계정입니다.")
        return redirect("acc:index")
        
    return render(request, "acc/signup.html")


def profile(request):
    return render(request, "acc/profile.html")



def delete(request):
    ck = request.POST.get("ckpass")
    if check_password(ck, request.user.password):
        request.user.pic.delete()
        request.user.delete()
        return redirect("acc:index")
    else:
        messages.info(request, "성공적으로 삭제되었습니다!")
    return redirect("acc:profile")

def edit(request):
    if request.method == "POST":
        u = request.user
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        ua = request.POST.get("uage")
        co = request.POST.get("com")
        upc = request.FILES.get("upic")
        u.username=un
        if up:
            u.set_password(up)#비번 암호화
        u.age=ua
        u.comment=co
        if upc:
            u.pic.delete()
            u.pic=upc
        u.save()
        login(request, u)#수정후 자동로그인
        return redirect("acc:profile")
    return render(request, "acc/edit.html")
