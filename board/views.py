from django.shortcuts import render , redirect
from .models import Board ,Reply
from django.utils import timezone
from django.core.paginator import Paginator
from acc.models import User
from django.contrib import messages
# Create your views here.


def index(request):
    page = request.GET.get("page",1)
    kw =request.GET.get("kw","")
    cate =request.GET.get("cate","")
    
    if kw:
        if cate == "sub":
            b =  Board.objects.filter(subject__contains=kw)
                    
        elif cate == "wri":
            try:
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
                                    
        elif cate == "con":
            b =  Board.objects.filter(content__contains=kw)
            
        else:
            b = Board.objects.all()
    
    else:
        b = Board.objects.all()
        
        
    b= b.order_by("-pubdate")#정렬= 내림차순은 앞에 - 붙히면된다
    
    pag =Paginator(b,10)
    obj = pag.get_page(page)
    
    context = {
        "bset" : obj,
        "cate" : cate,
        "kw" : kw,        
        
    }
    
    return render(request, "board/index.html",context)


def detail(request,bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b ,
        "rset" : r
    }
    return render(request, "board/detail.html",context)



def delete(request,bpk):
    b = Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
        messages.success(request, "성공적으로 삭제되었습니다.")
    else:
        messages.warning(request, "삭제되지 않았습니다")
    return redirect("board:index")

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        if s and c:
            Board(subject=s, writer=request.user, content=c, pubdate=timezone.now()).save()
            return redirect("board:index")
    return render(request, "board/create.html")


def update(request,bpk):
    b = Board.objects.get(id=bpk)
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("com")
        if request.user == b.writer:
            b.subject = s
            b.content = c
            b.save()
            messages.info(request, "업데이트 되었습니다.")
            return redirect("board:detail",bpk)

        else:
            messages.warning(request, "업데이트가 정상적으로 처리되지않았습니다.")
    context = {
        "b" : b
    }
    return render(request, "board/update.html",context)


def creply(request,bpk):
    c = request.POST.get("com")
    b = Board.objects.get(id=bpk)
    Reply(b=b,replyer=request.user,comment=c,pubdate=timezone.now()).save()
        
    return redirect("board:detail",bpk)

def dreply(request,bpk,rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
        messages.success(request, "댓글삭제 완료")
    else:
        messages.warning(request, "삭제되지 않았습니다")
    return redirect("board:detail",bpk)
    
    
    
    
def likey(request,bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    
    return redirect("board:detail",bpk)

def cancel(request,bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    
    return redirect("board:detail",bpk)