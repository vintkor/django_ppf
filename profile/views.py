from django.shortcuts import render
from django.views.generic import FormView
from .forms import AuthForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from catalog.models import Category


class AuthView(FormView):
    form_class = AuthForm
    template_name = 'profile/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
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
