# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings

from .forms import LinkForm, LoginForm, CreateProfileForm, EditProfileForm, CreateUserForm
from .models import ProfileModel
from .filters import StoryFilter, BookFilter, AuthorFilter

from stories.models import Author, Book

@login_required
def dashboard(request):
    return render(request, 'social/dashboard.html', {'dashboard':'dashboard'})


def redirect_after_login(request):
    nxt = request.GET.get("next", None)
    if nxt is None:
        return redirect(settings.LOGIN_REDIRECT_URL)    
    else:
        return redirect(nxt)


def authors_list(request):
    story_list = Author.objects.order_by('name')
    story_filter = AuthorFilter(request.GET, queryset=story_list)

    paginator = Paginator(story_filter.qs, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { "page_obj": page_obj, "filter": story_filter, "value": "authors"}

    return render(request, "views/profiles.html", context)

def users_list(request):
    story_list = Author.objects.order_by('name')
    story_filter = AuthorFilter(request.GET, queryset=story_list)

    paginator = Paginator(story_filter.qs, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { "page_obj": page_obj, "filter": story_filter, "value": "users"}

    return render(request, "views/profiles.html", context)

def prophets_list(request):
    story_list = Author.objects.order_by('name')
    story_filter = AuthorFilter(request.GET, queryset=story_list)

    paginator = Paginator(story_filter.qs, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { "page_obj": page_obj, "filter": story_filter, "value": "prophets"}

    return render(request, "views/profiles.html", context)



def profile_create_view(request):
    context = {}
    form = CreateProfileForm(request.POST or None)
    form2 = LinkForm(request.POST or None)
    if form.is_valid():
        form.save()
        form2.save()
        try:
            return redirect_after_login(request)
        except:
            pass
    context = {
        'form': form,
        'form2': form2,
    }
    return render(request, "views/profile_create_view.html", context)


def profile_list(request):
    story_list = ProfileModel.objects.order_by('name')
    story_filter = StoryFilter(request.GET, queryset=story_list)

    paginator = Paginator(story_filter.qs, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { "page_obj": page_obj, "filter": story_filter, 'value':'profiles'}

    return render(request, "views/profiles.html", context)


def profile_detail_view(request, id):
    about = Book.objects.filter(about__in=id)
    authors = Book.objects.filter(authors__in=id)
    

    story_filter = BookFilter(request.GET, queryset=Book.objects.all())
    context_404 = { "data": get_object_or_404(ProfileModel,id=id), "filter": story_filter, "about":about, "authors":authors, "value": "prophets"}
    return render(request, "views/profile_detail_view.html", context_404)

       
def profile_update_view(request, id):
    context = {}
    obj = get_object_or_404(ProfileModel,id=id)
    form = EditProfileForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        try:
            return redirect('/users/profile/'+id)
        except:
            pass
    context['form'] = form
    return render(request, "views/profile_update_view.html", context)

def profile_delete_view(request, id):
    context = {}
    obj = get_object_or_404(ProfileModel,id=id)
    form = EditProfileForm(request.POST or None, instance=obj)
    if request.method=="POST":
        obj.delete()
        try:
            return redirect('/users/profiles')
        except:
            pass
    context['form'] = form
    return render(request, "views/profile_delete_view.html", context)

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request,'Authenticated successfully')
                    return redirect_after_login(request)
                else:
                    messages.info(request,'Disabled account')  
                    return redirect_after_login(request)

            else:
                messages.info(request,'Invalid account')
                return redirect_after_login(request)

    else:
        form = LoginForm()
    return render(request, 'social/login.html', {'form':form})

def register(request):
    if request.method == "POST":
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect_after_login(request)
    else:
        user_form = CreateUserForm()
    return render(request, 'social/register.html', {'user_form':user_form})


def user_logout(request):
    logout(request)
    return redirect('home')