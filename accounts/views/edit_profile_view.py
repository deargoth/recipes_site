from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import get_user_model

from templates.static import site_messages
from accounts.models import Profile
from accounts import forms


User = get_user_model()


class EditProfile(View):
    template_name = 'accounts/edit_profile.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.profile = Profile.objects.get(
            user=request.user)

        self.context = {
            'profile': self.profile,
            'form_user': forms.UserProfileForm(data=request.POST or None,
                                               instance=request.user),
            'form_profile': forms.ProfileChangeForm(data=request.POST or None,
                                                    files=request.FILES or None,
                                                    instance=self.profile),
        }
        self.form_user = self.context['form_user']
        self.form_profile = self.context['form_profile']

        self.render = render(request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render

    def post(self, *args, **kwargs):
        if not self.form_user.is_valid() or not self.form_profile.is_valid():
            return self.render

        self.form_profile.save(commit=False)
        self.form_profile.user = self.request.user

        self.form_user.save()
        self.form_profile.save()

        messages.success(self.request,
                         site_messages.success['profile_updated'])
        return redirect('accounts:edit_profile', self.profile.slug)
