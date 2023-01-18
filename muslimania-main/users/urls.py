from django.urls import path
from .views import *
from stories.views import author_create

urlpatterns = [

    path('register/', register, name='register'), 
    path('dashboard/', dashboard, name='dashboard'), 
    
    path('authors/', authors_list, name='authors'), 
    path('authors/create/', author_create, name='authors_create'),

    path('prophets/', prophets_list, name='prophets'), 
    path('prophets/create/', author_create, name='prophets_create'),

    path('login/', user_login, name='login'), 
    path('logout/', user_logout, name='logout'), 

    path('profiles/create', profile_create_view, name='profile_create_view'), 

    path('profiles/', profile_list, name='profiles'), 
    path('profiles/<id>/', profile_detail_view, name='profile_detail_view'), 

    path('profiles/<id>/update', profile_update_view, name='profile_update_view'), 
    path('profiles/<id>/delete', profile_delete_view, name='profile_delete_view'), 

    path('', users_list, name='users'), 
    path('create/', author_create, name='users_create'),

]