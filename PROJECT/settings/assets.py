from .environment import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'templates/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'templates/static'
]
# STATIC_ROOT =

# Images
# ------

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'
