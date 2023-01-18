from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render, get_object_or_404

from .models import GeeksModel
from .forms import GeeksForm

def home(request):
    context = { "dataset": GeeksModel.objects.all()}
    return render(request, "home.html", context)

def info(request):
    context = { "dataset": GeeksModel.objects.all()}
    return render(request, "info.html", context)


def profiles(request):
    context = { "dataset": GeeksModel.objects.all()}
    return render(request, "profiles.html", context)


def create_view(request):
    context = {}
    form = GeeksForm(request.POST or None)
    if form.is_valid():
        form.save()
        try:
            return redirect('/crud/list/')
        except:
            pass
    context['form'] = form
    return render(request, "views/create_view.html", context)

def list_view(request):
    context = { "dataset": GeeksModel.objects.all()}
    return render(request, "views/list_view.html", context)

def detail_view(request, id):
    context_404 = { "data": get_object_or_404(GeeksModel,id=id)}
    return render(request, "views/detail_view.html", context_404)

def update_view(request, id):
    context = {}
    obj = get_object_or_404(GeeksModel,id=id)
    form = GeeksForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        try:
            return redirect('/crud/list/'+id)
        except:
            pass
    context['form'] = form
    return render(request, "views/update_view.html", context)

def delete_view(request, id):
    context = {}
    obj = get_object_or_404(GeeksModel,id=id)
    form = GeeksForm(request.POST or None, instance=obj)
    if request.method=="POST":
        obj.delete()
        try:
            return redirect('/crud/list/')
        except:
            pass
    context['form'] = form
    return render(request, "views/delete_view.html", context)
