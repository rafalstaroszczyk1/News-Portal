from django.urls import path
from .views import MainView, NewsDetail, HomeView, NewsCreate, DeleteView, UpdateView
from . import views

urlpatterns = [
    path('', HomeView.as_view()),
    path('news/', MainView.as_view(), name='news'),
    path('news/<int:link>/', NewsDetail.as_view(), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/delete/<int:link>/', DeleteView.as_view(), name='news_delete'),
    path('news/update/<int:link>/', UpdateView.as_view(), name='news_update'),
]