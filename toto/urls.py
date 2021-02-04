from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.signup, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
    path('all-totos/', views.totos, name='toto'),
    path('new-toto/', views.create_toto, name='new-toto'),
    path('profile/<username>', views.profile, name='profile'),
    path('profile/<username>/edit/', views.edit_profile, name='edit-profile'),
    path('join_toto/<id>', views.join_toto, name='join-toto'),
    path('leave_toto/<id>', views.leave_toto, name='leave-toto'),
    path('single_toto/<toto_id>', views.single_toto, name='single-toto'),
    path('<toto_id>/new-post', views.create_post, name='post'),
    path('<toto_id>/members', views.toto_members, name='members'),
    path('search/', views.search_business, name='search'),
]
