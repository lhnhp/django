from django.shortcuts import render ,redirect
from .models import Topic,Choice
from django.utils import timezone
from django.contrib import messages
# Create your views here.

def index(request):
    t = Topic.objects.all()
    t = t.order_by("-pubdate")
    context = {
        
        "tset" : t
        
    }    
    
    return render(request, "vote/index.html" ,context)


def detail(request,tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        "t" : t ,
        "cset" :c
    }
    
    
        
    return render(request, "vote/detail.html" , context)



def vote(request,tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        #토픽에 투표하지않았던 사람들만 종속문장 실행됨
        t.voter.add(request.user)
        
        cpk = request.POST.get("ch")
        c = Choice.objects.get(id=cpk)
        c.choicer.add(request.user)
        messages.info(request, "투표완료")
        
    return redirect("vote:detail",tpk)



def cancle(request,tpk):
    t = Topic.objects.get(id=tpk)
    u = request.user
    print(1)
    if u in t.voter.all():
        print(2)
        t.voter.remove(u)
        
        u.choice_set.get(topic=t).choicer.remove(u)
            
    
    return redirect("vote:detail",tpk)


def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        names = request.POST.getlist("boname")
        files = request.FILES.getlist("bopic")
        comns = request.POST.getlist("bocom")
        
        if len(names) >1:
            t = Topic(subject=s, maker=request.user,content=c,pubdate=timezone.now())
            t.save()
            
            for i,j,k in zip(names,files,comns):
                Choice(topic=t,chname=i,chpic=j,chcom=k).save()
                messages.success(request, "새로운 투표가 생성되었습니다.")
                
            return redirect("vote:index")
        
    return render(request, "vote/create.html")