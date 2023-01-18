from django.urls import path
from .views import PublisherListView, PublisherBookListView, AuthorDetailView, BookDetailView, BooksListView
from . import views
from .views import BookView

urlpatterns = [
    path('books/', BooksListView.as_view(), name="books"),
    path('books/<pk>/<slug:slug>', BookView.as_view(), name='books'),

    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.book_create_view, name="book_create_view"),
    
    path('books/<id>/delete/', views.book_delete, name="book_delete"),
    path('books/<id>/update/', views.book_update, name="book_update"),


    path('books/chapter_create/', views.story_create, name="chapter_create"),
    path('books/<id>/chapter_update/', views.story_update, name="chapter_update"),
    path('books/<id>/chapter_delete/', views.story_delete, name="chapter_delete"),

    
    path('books/publishers/<publisher>/', PublisherBookListView.as_view(), name="book_by"),

    path('publishers/', PublisherListView.as_view(), name="publishers"),
    path('publishers/create/', views.publisher_create_view, name="publisher_create"),

    
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='authors'),
    path('authors/create/', views.author_create, name='authors_create'),    
]