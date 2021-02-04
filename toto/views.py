from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, BusinessForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Lindatoto, Profile, Business, Post
from .forms import UpdateProfileForm, LindatotoForm, PostForm
from django.contrib.auth.models import User


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def totos(request):
    all_totos = Lindatoto.objects.all()
    all_totos = all_totos[::-1]
    params = {
        'all_totos': all_totos,
    }
    return render(request, 'all_totos.html', params)


def create_toto(request):
    if request.method == 'POST':
        form = LindatotoForm(request.POST, request.FILES)
        if form.is_valid():
            toto = form.save(commit=False)
            toto.admin = request.user.profile
            toto.save()
            return redirect('toto')
    else:
        form = LindatotoForm()
    return render(request, 'newtoto.html', {'form': form})


def single_toto(request, toto_id):
    toto = Lindatoto.objects.get(id=toto_id)
    business = Business.objects.filter(lindatoto=toto)
    posts = Post.objects.filter(toto=toto)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.lindatoto = toto
            b_form.user = request.user.profile
            b_form.save()
            return redirect('single-toto', toto.id)
    else:
        form = BusinessForm()
    params = {
        'toto': toto,
        'business': business,
        'form': form,
        'posts': posts
    }
    return render(request, 'single_toto.html', params)


def toto_members(request, toto_id):
    toto = Lindatoto.objects.get(id=toto_id)
    members = Profile.objects.filter(lindatoto=toto)
    return render(request, 'members.html', {'members': members})


def create_post(request, toto_id):
    toto = Lindatoto.objects.get(id=toto_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.toto = toto
            post.user = request.user.profile
            post.save()
            return redirect('single-toto', toto.id)
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})


def join_toto(request, id):
    lindatoto = get_object_or_404(Lindatoto, id=id)
    request.user.profile.lindatoto = lindatoto
    request.user.profile.save()
    return redirect('toto')


def leave_toto(request, id):
    toto = get_object_or_404(Lindatoto, id=id)
    request.user.profile.lindatoto = None
    request.user.profile.save()
    return redirect('toto')


def profile(request, username):
    return render(request, 'profile.html')


def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
    else:
        form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'editprofile.html', {'form': form})


def search_business(request):
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, "results.html")
