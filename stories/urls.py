from django.urls import path
from .views import PublisherListView, PublisherBookListView, AuthorDetailView, BookDetailView, BooksListView
from . import views
from .views import BookView, CommentView, HomeView, AddDislike, AddLike, PostView, PostCreateView, PostUpdateView, PostDeleteView

app_name = 'posts'

urlpatterns = [

    path('books/', HomeView.as_view(), name='stories'),
    path('comment/<int:id>/', CommentView, name='comment_update'),

    path('bookslist/', BooksListView.as_view(), name="books_lists"),
    path('books/<pk>/<slug:slug>', BookView.as_view(), name='books_slug'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    path('books/create/', views.book_create_view, name="book_create_view"),
    path('books/<id>/delete/', views.book_delete, name="book_delete"),
    path('books/<id>/update/', views.book_update, name="book_update"),

    path('books/<int:pk>/<slug:slug>/like', AddLike.as_view(), name='like'),
    path('books/<int:pk>/<slug:slug>/dislike', AddDislike.as_view(), name='dislike'),

    path('books/chapter_create/', views.chapter_create, name="chapter_create"),
    path('books/<id>/chapter_update/', views.story_update, name="chapter_update"),
    path('books/<id>/chapter_delete/', views.story_delete, name="chapter_delete"),
    
    path('books/publishers/<publisher>/', PublisherBookListView.as_view(), name="book_by"),
    
    path('<int:pk>/<slug:slug>', PostView.as_view(), name='post'),

    path('post/<int:pk>/<slug:slug>/like', AddLike.as_view(), name='like'),
    path('post/<int:pk>/<slug:slug>/dislike', AddDislike.as_view(), name='dislike'),

    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('publishers/', PublisherListView.as_view(), name="publishers"),
    path('publishers/create/', views.publisher_create_view, name="publisher_create"),

    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='authors'),
    path('authors/create/', views.author_create, name='authors_create'),    

]