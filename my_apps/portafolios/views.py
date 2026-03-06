from django.shortcuts import render
from my_apps.portafolios.models import Project, Tag
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

    tags = Tag.objects.all()

    return render(request, "portafolios/projects.html", {
        "projects": projects,
        "tags": tags,
        "active_tag": tag
    })