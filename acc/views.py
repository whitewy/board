from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        user = authenticate(username=un, password=pw)
        if user:
            login(request, user)
            messages.success(request, f"{user} 님 환영합니다!!")
            return redirect("acc:index")
        else:
            messages.error(request, "계정정보가 일치하지 않습니다.")
        
    return render(request, "acc/login.html")

def update(request):
    if request.method == "POST":
        u = request.user
        pw = request.POST.get("upass")
        co = request.POST.get("comment")
        pi = request.FILES.get("upic")
        if pw:
            u.set_password(pw)
        if pi:
            u.pic.delete()
            u.pic = pi
        u.comment = co
        u.save()
        login(request, u)
        return redirect("acc:profile")

    return render(request, "acc/update.html")

def delete(request):
    request.user.pic.delete()
    request.user.delete()
    return redirect("acc:index")

def profile(request):
    return render(request, "acc/profile.html")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        ag = request.POST.get("age")
        co = request.POST.get("ucomm")
        pi = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un, password=pw, age=ag, comment=co, pic=pi)
            return redirect("acc:login")
        except:
            messages.error(request, "이미 사용중인 USERNAME 입니다.")  
    return render(request, "acc/signup.html")

def logout_user(request):
    logout(request)
    return redirect("acc:index")

# Create your views here.
def index(request):
    return render(request, "acc/index.html")

