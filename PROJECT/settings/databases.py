from decouple import config

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('MYSQL_DB'),
        'HOST': config('HOST'),
        'PORT': config('PORT'),
        'USER': config('USER'),
        'PASSWORD': config('PASSWORD'),
    }
}
