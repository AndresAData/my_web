from django.urls import path
from .views import HomeView

app_name = 'portafolios'


urlpatterns = [
    path('', HomeView, name='home'),
]