from django.shortcuts import render
from my_apps.portafolios.models import Project
# Create your views here.


def HomeView(request):
    return render(request, 'portafolios/home.html')


def PortafolioView(request):
    
    tag = request.GET.get("tag")
    
    projects = (
        Project.objects
        .published()
        .with_relations()
        .ordered()
    )
    
    if tag:
        projects = projects.with_tag(tag)
    
    return render(request, 'portafolios/portafolio.html', {
        'projects': projects
    })