from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

def is_admin(user):
    return user.is_staff

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.home, name='home'),
    path('analytics/', login_required(views.analytics), name='analytics'),
    path('users/', user_passes_test(is_admin)(views.UserListView.as_view()), name='user_list'),
    path('users/create/', user_passes_test(is_admin)(views.UserCreateView.as_view()), name='user_create'),
    path('users/<int:pk>/update/', user_passes_test(is_admin)(views.UserUpdateView.as_view()), name='user_update'),
    path('users/<int:pk>/delete/', user_passes_test(is_admin)(views.UserDeleteView.as_view()), name='user_delete'),
] 