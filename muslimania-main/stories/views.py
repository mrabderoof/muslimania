from http.client import HTTPResponse
from django.views.generic import ListView, DetailView

from stories.forms import AuthorCreateForm, EditStoryForm, CreateBookForm, CreateChapterForm, CreatePublisherForm, EditBookForm, StoryForm
from .models import Publisher, Book, Author, Story
from .forms import Comment, CommentForm

from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone


class BooksListView(ListView):
    model = Book
    context_object_name = 'my_favorite_books'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Publisher.objects.all()
        context['value'] = 'book'
        return context

class PublisherListView(ListView):
    model = Publisher
    context_object_name = 'my_favorite_publishers'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.all()
        context['value'] = 'publisher'
        return context

class PublisherBookListView(ListView):
    
    template_name = 'stories/books_by_publisher.html'
    paginate_by = 2

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['publisher'] = self.publisher
        return context


class BookListView(ListView):
    queryset = Book.objects.order_by('-publication_date')
    context_object_name = 'book_list'
    

class AcmeBookListView(ListView):
    
    context_object_name = 'book_list'
    queryset = Book.objects.filter(publisher__name='ACME Publishing')
    template_name = 'stories/acme_list.html'


class PublisherDetailView(DetailView):
    
    context_object_name = 'publisher'
    queryset = Publisher.objects.all()

class BookDetailView(DetailView):
    model = Book
    template_name = 'stories/book_view.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookDetailView, self).get_context_data(**kwargs)

        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.filter(pk=self.kwargs.get('pk'))
        return context

class BookView(DetailView):
    model = Book
    template_name = 'stories/book_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        slug = self.kwargs["slug"]

        form = CommentForm()
        post = get_object_or_404(Book, pk=pk, slug=slug)
        comments = Story.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Book.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, email=email, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)

class AuthorDetailView(DetailView):
    
    queryset = Author.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj


def author_create(request):
    context = {}
    form = AuthorCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        try:
            return redirect('books')
        except:
            pass
    context = {
        'form': form,
    }
    return render(request, "views/profile_create_view.html", context)

def book_create_view(request):
    context = {}
    form = CreateBookForm(request.POST or None)
    if form.is_valid():
        form.save()
        try:
            return redirect('books')
        except:
            pass
    context = {
        'form': form,
    }
    return render(request, "views/profile_create_view.html", context)

def story_create(request):
    context = {}
    form = CreateChapterForm(request.POST or None)
    if form.is_valid():
        form.save()
        try:
            return redirect('books')
        except:
            pass
    context = {
        'form': form,
    }
    return render(request, "views/profile_create_view.html", context)

def story_update(request, id):
    context = {}
    obj = get_object_or_404(Book,id=id)
    form = EditStoryForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        try:
            return redirect('books')
        except:
            pass
    context['form'] = form
    return render(request, "views/profile_update_view.html", context)

def story_delete(request, id):
    context = {}
    obj = get_object_or_404(Book,id=id)
    form = EditStoryForm(request.POST or None, instance=obj)
    if request.method=="POST":
        obj.delete()
        try:
            return redirect('books')
        except:
            pass
    context['form'] = form
    return render(request, "views/profile_delete_view.html", context)


def chapter_create(request):
    context = {}
    form = ChapterCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        try:
            return redirect('books')
        except:
            pass
    context = {
        'form': form,
    }
    return render(request, "views/profile_create_view.html", context)

def book_update(request, id):
    context = {}
    obj = get_object_or_404(Book,id=id)
    form = EditBookForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        try:
            return redirect('/stories/books/'+id)
        except:
            pass
    context['form'] = form
    return render(request, "views/profile_update_view.html", context)

def book_delete(request, id):
    context = {}
    obj = get_object_or_404(Book,id=id)
    form = EditBookForm(request.POST or None, instance=obj)
    if request.method=="POST":
        obj.delete()
        try:
            return redirect('/users/profiles')
        except:
            pass
    context['form'] = form
    return render(request, "views/profile_delete_view.html", context)



def publisher_create_view(request):
    context = {}
    form = CreatePublisherForm(request.POST or None)
    if form.is_valid():
        form.save()
        try:
            return redirect('publishers')
        except:
            pass
    context = {
        'form': form,
    }
    return render(request, "views/profile_create_view.html", context)
