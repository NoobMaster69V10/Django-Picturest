from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView
from .models import *
from .models import Profile as UserProfile
from .forms import *


class Home(ListView):
    """ Home page """
    model = Post
    template_name = 'picturest/index.html'
    context_object_name = 'posts'


class Explore(View):
    def get(self, request):
        cats = Category.objects.all()
        posts = Post.objects.all()
        return render(request, 'picturest/explore.html', {'cats': cats, 'posts': posts})


class CategoryView(View):
    def get(self, request, cat):
        category = Category.objects.get(url=cat)
        cats = Post.objects.filter(category=category.pk).all()

        return render(request, 'picturest/category.html', {'cat': cats, 'category': cat})


class LoggedAll(ListView):
    model = Post
    template_name = 'picturest/main-logged.html'
    context_object_name = 'posts'


class PostDetail(View):
    """ Post detil """

    def get(self, request, slug):
        context = {}
        form = AddCommentForm()
        context['form'] = form

        post = Post.objects.get(url=slug)
        comments = Comments.objects.filter(post=slug).all()
        return render(request, 'picturest/post.html', {'post': post, 'comments': comments, 'form': form})

    def post(self, request, slug):
        if request.method == "POST":
            form = AddCommentForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                user = request.user.id
                owner = User.objects.get(id=request.user.id)
                post = slug
                comment = Comments.objects.create(
                    user=user,
                    text=text,
                    post=post,
                    owner=owner,
                )
                comment.save()
                return redirect(f'/post/{slug}')


class Profile(View):
    """ Profile """

    def get(self, request):
        posts = Post.objects.filter(user=request.user).all()
        return render(request, 'picturest/profile.html', {'posts': posts})


def profile_edit(request):
    context = {}
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            image = form.cleaned_data.get('image')
            user = User.objects.get(id=request.user.id)

            if image:
                user.profile.name = name
                user.profile.image = image
                user.profile.save()
                return redirect('profile')
            else:
                user.profile.name = name
                user.profile.save()
                return redirect('profile')
    else:
        form = EditProfileForm()
    context['form'] = form
    return render(request, 'picturest/profile-edit.html', context)


class LogIn(LoginView):
    """ Log in view """
    form_class = LoginUserForm
    template_name = 'picturest/log-in.html'

    def get_success_url(self):
        return reverse_lazy('main')


def log_out(request):
    """ Log out view """
    logout(request)
    return redirect('home')


def create_profile(request):
    """ Creates profile for user after sign up """
    user = User.objects.last()
    prof = UserProfile.objects.create(user=user)
    prof.save()
    return redirect('log_in')


class SignUp(CreateView):
    """ Sign up view """
    form_class = RegisterUserForm
    template_name = 'picturest/sign-up.html'
    success_url = reverse_lazy('profile_create')


def add_post(request):
    """ Add post view """
    context = {}
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            image = form.cleaned_data.get('image')
            category = form.cleaned_data.get('category')

            obj = Post.objects.create(
                title=title,
                image=image,
                description=description,
                category=category,
                owner=request.user.id,
                user=User.objects.get(id=request.user.id)
            )
            obj.save()
            return redirect('main')
    else:
        form = AddPostForm()
    context['form'] = form
    return render(request, 'picturest/add_post.html', context)


def search_text(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)
        return render(request, 'picturest/search.html', {'posts': posts, 'search_word': searched})


def profile_search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched, user=request.user)
        return render(request, 'picturest/profile_search.html', {'posts': posts, 'search_word': searched})
