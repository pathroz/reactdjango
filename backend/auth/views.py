# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import UserProfile
from .forms import LoginForm, ProfileUpdateForm, SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, UpdateView

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "registration/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    
    context = {}
    context['segment'] = 'newstaffaccount'
    context['active_menu'] = 'dashboard'
    context['page1'] = 'DASHBOARD'
    context['page2'] = 'New Staff Register'
    context['form'] = form
    context['msg'] = msg
    context['success'] = success

    return render(request, "registration/newstaffaccount.html", context=context)



# class SettingsViewPage(LoginRequiredMixin, TemplateView):
#     template_name = 'pages/home/settings.html'
#     login_url = '/'
#     redirect_field_name = 'redirect_to'

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#             context = super().get_context_data(**kwargs)

#             context['segment'] = 'settingS'
#             context['active_menu'] = 'dashboard'
#             context['page1'] = 'DASHBOARD'
#             context['page2'] = 'SETTINGS'

#             return context
class SettingsViewPage(LoginRequiredMixin, UpdateView):
    template_name = 'pages/home/settings.html'
    context_object_name = 'user'
    login_url = '/'
    redirect_field_name = 'redirect_to'
    queryset = UserProfile.objects.all()
    form_class = ProfileUpdateForm

    def get_context_data(self, **kwargs):
        context = super(SettingsViewPage, self).get_context_data(**kwargs)
        user = self.request.user
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile, initial={'username': user.get_username, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'location': user.profile.Location, 'phoneno':  user.profile.PhoneNo  })
        context['segment'] = 'settings'
        context['active_menu'] = 'dashboard'
        context['page1'] = 'DASHBOARD'
        context['page2'] = 'SETTINGS'
        return context

    def form_valid(self, form):
        profile = form.save(commit=False)
        user = profile.user
        user.last_name = form.cleaned_data['last_name']
        user.first_name = form.cleaned_data['first_name']
        user.email = form.cleaned_data['email']
        profile.Location = form.cleaned_data['location']
        profile.PhoneNo = form.cleaned_data['phoneno']
        user.save()
        profile.save()
        return HttpResponseRedirect(reverse('settings', kwargs={'pk': self.get_object().id}))



