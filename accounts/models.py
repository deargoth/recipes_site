import string
from random import SystemRandom
from collections import defaultdict
from PIL import Image

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager
from templates.static import site_messages


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(
        default='Nothing to see here', blank=True, null=True, verbose_name=_('Biography'))
    image = models.ImageField(
        upload_to='profile_photos/%Y/%m', blank=True, null=True, verbose_name=_('Image'))
    slug = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = settings.MEDIA_ROOT / image.name
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def clean(self):
        error_messages = defaultdict(list)
        profile_slug = Profile.objects.filter(slug=self.slug).first()

        if profile_slug:
            if profile_slug.pk != self.pk:
                error_messages['slug'].append(
                    site_messages.error['slug_already_exists'])

        if error_messages:
            raise ValidationError(error_messages)

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.user.first_name}-{rand_letters}')

        self.slug = slugify(self.slug)

        if not self.biography:
            self.biography = 'Nothing to see here'

        super().save(*args, **kwargs)

        if self.image:
            self.resize_image(self.image, 200)

    def __str__(self):
        return self.user.first_name
