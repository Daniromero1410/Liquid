from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

class UserListView(ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'is_active', 'is_staff']
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

@login_required
def home(request):
    return render(request, 'accounts/home.html')

@login_required
def analytics(request):
    # Get basic analytics data
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    
    # Get users created in the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'recent_users': recent_users,
    }
    return render(request, 'accounts/analytics.html', context)