from django.urls import path
from . import views

urlpatterns = [
    path('api/movies', views.movie_list),
    path('api/movies/<slug:movie_title>', views.movie_detail)
]
