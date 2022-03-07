from django.shortcuts import render ,redirect
from book.models import Book
# Create your views here.
from django.contrib import messages

def index(request):
    b = request.user.book_set.all()
    
    context = {
        
        "bset" : b
        
    }
    
    return render(request, "book/index.html" ,context)


def create(request):
    if request.method == "POST":
        sn = request.POST.get("sname")
        su = request.POST.get("surl")
        sc = request.POST.get("scom")
        im = bool(request.POST.get("impo"))
        
        Book(user=request.user,site_name=sn,site_url=su,comment=sc,impo=im).save()
        messages.success(request, "북마크되었습니다.")
        return redirect("book:index")

    return render(request, "book/create.html")
