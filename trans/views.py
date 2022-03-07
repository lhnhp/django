from django.shortcuts import render ,redirect
import googletrans
from googletrans import Translator
# Create your views here.

def index(request):
    d = {"set" :"언어선택"}
    for i in googletrans.LANGUAGES:
        d[i] = googletrans.LANGUAGES[i]
    
    context = { "ndict" : d }
    if request.method == "GET":
        to = request.GET.get("to")
        a = request.GET.get("as")
        be = request.GET.get("be")
        translator = Translator()
        if to:
            inter = translator.translate(to, src=a, dest=be)
            context.update({
                "to" : to,
                "as" : a,
                "be" : be,
                "end" : inter.text
            })
    return render(request, "trans/index.html", context)








