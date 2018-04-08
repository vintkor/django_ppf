try:
    from django_ppf.prod_settings import *
except:
    """
    Django settings for django_ppf project.
    
    Generated by 'django-admin startproject' using Django 1.11.7.
    
    For more information on this file, see
    https://docs.djangoproject.com/en/1.11/topics/settings/
    
    For the full list of settings and their values, see
    https://docs.djangoproject.com/en/1.11/ref/settings/
    """

    import os

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '2!i8bq5vui&=z8cw0ps(mkgbs!34sprtuq+q!1xu)v&8r4s1^2'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    SITE_URL = 'https://ppf-company.com.ua'

    ALLOWED_HOSTS = ['*']
    INTERNAL_IPS = '127.0.0.1'


    # Application definition

    INSTALLED_APPS = [
        'modeltranslation',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sitemaps',

        'debug_toolbar',
        'mptt',
        'ckeditor',
        'ckeditor_uploader',
        'rangefilter',
        'sorl.thumbnail',
        'django_nose',
        'phonenumber_field',

        'profile',
        'catalog',
        'geo',
        'news',
        'currency',
        'assistant',
        'partners',
        'company',
        'telegram_bot',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'htmlmin.middleware.HtmlMinifyMiddleware',
        'htmlmin.middleware.MarkRequestMiddleware',
    ]

    ROOT_URLCONF = 'django_ppf.urls'

    TELEGRAM_API_URL = 'https://api.telegram.org/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates', 'django_ppf/templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.template.context_processors.i18n',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'django_ppf.wsgi.application'


    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django_ppf',
            'USER': 'root',
            'PASSWORD': '7108471084',
            'HOST': '127.0.0.1',
            'PORT': '',
            'OPTIONS': {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }


    # Password validation
    # https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/1.11/topics/i18n/

    LANGUAGES = (
        ('ru', 'Russian'),
        ('uk', 'Ukrainian'),
        # ('en', 'English'),
    )

    LANGUAGE_CODE = 'ru'

    MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
    MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'ru'
    MODELTRANSLATION_DEBUG = True

    MODELTRANSLATION_TRANSLATION_FILES = (
        'catalog.translation',
    )

    TIME_ZONE = 'Europe/Kiev'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.11/howto/static-files/

    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    CKEDITOR_UPLOAD_PATH = 'uploads/'
    MPTT_ADMIN_LEVEL_INDENT = 20

    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    NOSE_ARGS = [
        '--cover-erase',
        '--cover-package=assistant, news',
        '--with-coverage',
        '--cover-html',
    ]

    CKEDITOR_CONFIGS = {
        'default': {
            # 'skin': 'moono',
            # 'skin': 'office2013',
            'toolbar_Basic': [
                ['Source', '-', 'Bold', 'Italic']
            ],
            'toolbar_YourCustomToolbarConfig': [
                {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
                {'name': 'clipboard',
                 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
                {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
                {'name': 'basicstyles',
                 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
                {'name': 'paragraph',
                 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                           '-',
                           'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                           'Language']},
                {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
                {'name': 'insert',
                 'items': ['Image', 'Youtube', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak',
                           'Iframe']},
                '/',
                {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
                {'name': 'colors', 'items': ['TextColor', 'BGColor']},
                {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
                {'name': 'about', 'items': ['About']},
                {'name': 'yourcustomtools', 'items': ['Preview', 'Maximize', ]},
            ],
            'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
            # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
            # 'height': 291,
            # 'width': '100%',
            # 'filebrowserWindowHeight': 725,
            # 'filebrowserWindowWidth': 940,
            # 'toolbarCanCollapse': True,
            # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
            'tabSpaces': 4,
            'extraPlugins': ','.join([
                'uploadimage',  # the upload image feature
                # your extra plugins here
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                # 'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                # 'youtube',
                'elementspath'
            ]),
        }
    }
