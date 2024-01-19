from django.urls import path
from .views import *

urlpatterns = [
    path("", Home.as_view(), name='home'),
    path("explore/", Explore.as_view(), name='explore'),
    path("explore/<str:cat>", CategoryView.as_view(), name='category'),
    path("main/", LoggedAll.as_view(), name='main'),
    path("post/<slug:slug>", PostDetail.as_view(), name='post'),
    path("log-in/", LogIn.as_view(), name='log_in'),
    path("log-out/", log_out, name='log_out'),
    path("sign-up/", SignUp.as_view(), name='sign_up'),
    path("create/", add_post, name='add_post'),
    path("search/", search_text, name='search'),
    path("profile/", Profile.as_view(), name='profile'),
    path("profile/edit/", profile_edit, name='profile_edit'),
    path("profile/search/", profile_search, name='profile_search'),
    path("profile/create/", create_profile, name='profile_create'),
]