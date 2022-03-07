from django.shortcuts import render ,redirect
import pdfplumber
# Create your views here.



def index(request):
    context = {}
    if request.method == "POST":
        p = request.FILES.get("pdf")
        pdf = pdfplumber.open(p)
        plum = len(pdf.pages)
        st = ""
        for i in range(plum):
            page = pdf.pages[i]
            st += "="*50 + "\n"
            st += f"{i+1} PAGE" + "\n"
            st += "="*50 + "\n"
            st += page.extract_text()
            st += "\n"
        context["st"] = st
 
    return render(request, "pdfread/index.html" ,context)



