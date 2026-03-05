from django.urls import path
from .views import HomeView, PortafolioView

app_name = 'portafolios'


urlpatterns = [
    path('', HomeView, name='home'),
    path('portafolio/', PortafolioView, name='projects'),
]