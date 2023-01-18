from random import choices
import django_filters

import users

from .models import ProfileModel
from stories.models import Author, Book

class ListingFilter(django_filters.FilterSet):

    class Meta:
        model = ProfileModel
        fields = {'name': {'icontains'}, 'sex':{'exact'}}

class StoryFilter(django_filters.FilterSet):
    
    class Meta:
        model = ProfileModel
        fields = {'name':{'icontains'}}


class AuthorFilter(django_filters.FilterSet):
    
    class Meta:
        model = Author
        fields = {'name':{'icontains'}}

class BookFilter(django_filters.FilterSet):
    
    class Meta:
        model = Book
        fields = {'about':{'icontains'}}

# class UserFilter(django_filters.FilterSet):
    
#     class Meta:
#         model = users
#         fields = {'name':{'icontains'}}