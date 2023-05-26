from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from PIL import Image
from collections import defaultdict

from templates.static import site_messages
from tag.models import Tag
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name=_("Title"))
    description = models.CharField(max_length=255, verbose_name=_("Description"))
    slug = models.SlugField(null=True, blank=True)
    preparation_time = models.PositiveIntegerField(verbose_name=_("Preparation time"))
    preparation_time_unit = models.CharField(
        max_length=65, verbose_name=_("Preparation time unit")
    )
    servings = models.PositiveIntegerField(verbose_name=_("Servings"))
    servings_unit = models.CharField(max_length=65, verbose_name=_("Servings unit"))
    preparation_steps = models.TextField(verbose_name=_("Preparation steps"))
    preparation_steps_is_html = models.BooleanField(
        default=False, verbose_name=_("Preparation steps is HTML")
    )
    image = models.ImageField(
        upload_to="pictures/%Y/%m/%d", blank=True, null=True, verbose_name=_("Image")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    is_published = models.BooleanField(default=False, verbose_name=_("Is published"))
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Autor")
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Category"),
    )

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

        recipe_on_db = Recipe.objects.filter(title__iexact=self.title).first()

        if recipe_on_db:
            if recipe_on_db.pk != self.pk:
                error_messages["title"].append(
                    site_messages.error["recipe_with_same_title"]
                )

        if error_messages:
            raise ValidationError(error_messages)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.title)
            self.slug = slug

        super().save(*args, **kwargs)

        if self.image:
            self.resize_image(self.image, 840)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:details", kwargs={"pk": self.pk})
