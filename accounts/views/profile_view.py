from typing import Any
from django.db import models
from django.views.generic.detail import DetailView

from accounts.models import Profile


class ProfileView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'accounts/profile.html'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.select_related('user')

        return qs
