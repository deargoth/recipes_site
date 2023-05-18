import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Recipe


def delete_image(instance):
    try:
        os.remove(instance.image.path)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")


@receiver(pre_delete, sender=Recipe)
def recipe_image_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.get(pk=instance.pk)
    delete_image(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_image_update(sender, instance, raw, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if old_instance:
        is_new_cover = old_instance.image != instance.image

        if old_instance.image:
            if is_new_cover:
                delete_image(old_instance)
