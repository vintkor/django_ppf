from django.shortcuts import render
from django.views.generic import FormView, View
from .forms import AuthForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from catalog.models import Category
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


def user_logout(request):
    logout(request)
    return redirect('/')


class AuthView(FormView):
    form_class = AuthForm
    template_name = 'user_profile/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super(AuthView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(level=0)
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect('/')


class ProfileDetailView(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(id=self.request.user.id)
        return render(request, 'user_profile/profile.html', {'user': user})
