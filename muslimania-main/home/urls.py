from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('info/', views.info, name='info'),
    path('profiles/', views.profiles, name='profiles'),

    path('list/', views.list_view),
    path('create/', views.create_view),
    path('list/<id>/', views.detail_view),
    path('list/<id>/update/', views.update_view),
    path('list/<id>/delete/', views.delete_view),

]