from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from stories.forms import AuthorCreateForm, EditStoryForm, CreateBookForm, CreateChapterForm, CreatePublisherForm, EditBookForm
from .models import Publisher, Book, Author, Story, Post
from .forms import Comment, CommentForm
from django.views import View

from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib import messages
from django.utils.text import slugify
from django.urls import reverse_lazy

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

class HomeView(ListView):
    template_name = 'post_list.html'
    queryset = Post.objects.all()
    paginate_by = 2


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image", "tags"]

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been created successfully.')
        return reverse_lazy("posts:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image", "tags"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update

        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been updated successfully.')
        return reverse_lazy("posts:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully.')
        return reverse_lazy("posts:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

class PostView(DetailView):
    model = Post
    template_name = "post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        slug = self.kwargs["slug"]
        form = CommentForm()

        post = get_object_or_404(Post, pk=pk, slug=slug)
        comments = Comment.objects.filter(post=post)
        exist = []
        comments_filtered = []

        for comment in comments:
            if not comment.header in exist:
                exist.append(comment.header)
                comments_filtered.append(comment)

        context['post'] = post 
        context['comments'] = comments_filtered
        context['form'] = form
        
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments

        context['form'] = form

        if form.is_valid():
            header = form.cleaned_data['header']
            content = form.cleaned_data['content']

            Comment.objects.create(
                header=header, content=content, post=post, contributer=request.user
            )

            form = CommentForm()
            context['form'] = form

            return self.render_to_response(context=context)

        return self.render_to_response(context=context)
    
    def edit(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            header = form.cleaned_data['header']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                    header=header, content=content, post=post, contributer=request.user
                )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            post.dislikes.remove(request.user)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like: 
            post.likes.add(request.user)
        
        if is_like:
            post.likes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        is_like = False
        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break
        if is_like:
            post.likes.remove(request.user)
        is_dislike = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if not is_dislike: 
            post.dislikes.add(request.user)
        
        if is_dislike:
            post.dislikes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

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

class PublisherDetailView(DetailView):
    
    context_object_name = 'publisher'
    queryset = Publisher.objects.all()

class AcmeBookListView(ListView):
    
    context_object_name = 'book_list'
    queryset = Book.objects.filter(publisher__name='ACME Publishing')
    template_name = 'stories/acme_list.html'

class BookListView(ListView):
    queryset = Book.objects.order_by('-publication_date')
    context_object_name = 'book_list'

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

def CommentView(request, id):
    comments = Comment.objects.all()
    context = {"comments": comments}
    obj = get_object_or_404(Comment,id=id)
    form = CommentForm(request.POST or None, instance=obj)
    contribs = Comment.objects.filter(id=id)
    
    if form.is_valid():
        flag = 0
        for comment in comments:
            if str(comment.contributer) == str(request.user.username):
                flag = 1
                form.save()
                try:
                    return redirect('/comment/'+id)
                except:
                    pass

        if flag == 0:
                header = form.cleaned_data['header']
                content = form.cleaned_data['content']
                for comment in comments:
                    post = comment.post
                
                comment = Comment.objects.create(
                    header=header, content=content, post=post, contributer=request.user
                )

    context['form'] = form
    context['contribs'] = contribs
    return render(request, "stories/comment_update_view.html", context)

def chapter_create(request):
    context = {}
    comments = Comment.objects.all()
    form = CreateChapterForm(request.POST or None)
    if form.is_valid():
        flag = 0
        header = form.cleaned_data['header']
        for comment in comments:
            if str(comment.contributer) == str(request.user.username):
                if str(header) == str(comment.header):
                    flag = 1
                    try:
                        return redirect('stories')
                    except:
                        pass
        if flag == 0:
            form.save()

    return render(request, "stories/comment_create.html", context)