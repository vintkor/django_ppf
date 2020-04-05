try:
    from django_ppf.prod_settings import *
except:
    import os
    from django.utils.translation import ugettext_lazy as _

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = '2!i8bq5vui&=z8cw0ps(mkgbs!34sprtuq+q!1xu)v&8r4s1^2'

    DEBUG = True

    SITE_URL = 'https://ppf-company.com.ua'

    ALLOWED_HOSTS = ['*']
    INTERNAL_IPS = '127.0.0.1'

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
        'django_celery_results',
        'django_cool_paginator',
        'django_social_share',
        'django_json_widget',
        'storages',

        'user_profile',
        'catalog',
        'geo',
        'news',
        'currency',
        'assistant',
        'partners',
        'company',
        'telegram_bot',
        'library',
        'pages',
        'solutions',
        'spider',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'htmlmin.middleware.HtmlMinifyMiddleware',
        'htmlmin.middleware.MarkRequestMiddleware',
        'assistant.middleware.CurrentUserMiddleware',
    ]

    MIDDLEWARE_CLASSES = (
        'assistant.middleware.CurrentUserMiddleware',
    )

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

    LANGUAGE_CODE = 'ru'

    gettext = lambda s: s
    LANGUAGES = (
        ('ru', gettext('Russian')),
        ('uk', gettext('Ukrainian')),
    )

    MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
    MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'ru'
    MODELTRANSLATION_DEBUG = False

    MODELTRANSLATION_TRANSLATION_FILES = [
        'catalog.translation',
    ]

    TIME_ZONE = 'Europe/Kiev'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )

    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )

    AWS_ACCESS_KEY_ID = 'some_key'
    AWS_SECRET_ACCESS_KEY = 'some_key_'
    AWS_STORAGE_BUCKET_NAME = 'ppf-media'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    DEFAULT_FILE_STORAGE = 'django_ppf.storage_backends.PublicMediaStorage'

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

    CELERY_BROKER_URL = 'amqp://localhost'
    CELERY_IMPORTS = (
        "assistant.tasks",
    )

    COOL_PAGINATOR_NEXT_NAME = _('Next')
    COOL_PAGINATOR_PREVIOUS_NAME = _('Prev')
