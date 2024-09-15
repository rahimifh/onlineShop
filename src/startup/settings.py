import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


#### Secret Key - Debug - Allowed Hosts
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = eval(os.environ.get("DEBUG"))


ALLOWED_HOSTS = eval(os.environ.get("ALLOWED_HOSTS"))


#### CORS/CSRF Options And Settings
CORS_ALLOWED_ORIGINS = eval(os.environ.get("CORS_ALLOWED_ORIGINS"))
CSRF_TRUSTED_ORIGINS = eval(os.environ.get("CSRF_TRUSTED_ORIGINS"))
CORS_ORIGIN_ALLOW_ALL = eval(os.environ.get("CORS_ORIGIN_ALLOW_ALL"))
CORS_ALLOW_HEADERS = eval(os.environ.get("CORS_ALLOW_HEADERS"))
SITE_ID = 1 

#### Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",  # add sites to installed_apps
    "django.contrib.sitemaps",
    # third party apps
    "jalali_date",
    "corsheaders",
    "django_jalali",
    "fontawesomefree",
    "ckeditor",  # CKEditor config
    "ckeditor_uploader",  # CKEditor media uploader
    "import_export",
    "core",
    "account",
    "payment",
    "CRM",
    "blog",
    "dashboard",
    "Products",
]

# DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
# DBBACKUP_STORAGE_OPTIONS = {'location': './backup/dir/'}
MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "htmlmin.middleware.HtmlMinifyMiddleware",
    "htmlmin.middleware.MarkRequestMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # 'whitenoise.middleware.WhiteNoiseMiddleware', # Serve static in production without nginx or apache
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "startup.urls"
AUTH_USER_MODEL = "account.Account"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {
                "staticfiles": "django.templatetags.static",
            },
        },
    },
]


WSGI_APPLICATION = "startup.wsgi.application"

#### Rest Framework Settings
RENDERER = ("rest_framework.renderers.JSONRenderer",)
if DEBUG:
    RENDERER += ("rest_framework.renderers.BrowsableAPIRenderer",)



#### Database Settings
DATABASES = {"default": eval(os.environ.get("DATABASE_INFO"))}


#### Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


#### EMAIL SETTINGS
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = eval(os.environ.get("EMAIL_USE_TLS"))
EMAIL_PORT = eval(os.environ.get("EMAIL_PORT"))
# EMAIL_USE_SSL = eval(os.environ.get('EMAIL_USE_SSL'))


#### Internationalization
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE")
TIME_ZONE = os.environ.get("TIME_ZONE")
USE_I18N = eval(os.environ.get("USE_I18N"))
USE_L10N = eval(os.environ.get("USE_L10N"))
USE_TZ = eval(os.environ.get("USE_TZ"))


#### STATIC FILES (CSS, JavaScript, Images)
STATIC_URL = os.environ.get("STATIC_URL")
STATICFILES_DIRS = eval(os.environ.get("STATICFILES_DIRS"))

if DEBUG:
    STATIC_ROOT = os.environ.get("STATIC_ROOT_DEV")
else:
    STATIC_ROOT = os.environ.get("STATIC_ROOT")

# django compressor
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.DefaultStorageFinder",
    "compressor.finders.CompressorFinder",
)

# Compression settings and conf
COMPRESS_ROOT = STATIC_ROOT
# COMPRESS_ROOT = BASE_DIR / 'assets'
# COMPRESS_ENABLED = not DEBUG
COMPRESS_ENABLED = True
# COMPRESS_OFFLINE = True
COMPRESS_CSS_HASHING_METHOD = "content"
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": [
        "compressor.filters.jsmin.JSMinFilter",
    ],
}
# COMPRESS_STORAGE = "staticfiles.storage.StaticFileStorage"
HTML_MINIFY = True
# KEEP_COMMENTS_ON_MINIFYING = True


#### MEDIA FILES
MEDIA_URL = os.environ.get("MEDIA_URL")
if DEBUG:
    MEDIA_ROOT = eval(os.environ.get("MEDIA_ROOT_DEV"))
else:
    MEDIA_ROOT = eval(os.environ.get("MEDIA_ROOT"))


# Ckeditor Settings and Configs
CKEDITOR_BASEPATH = os.environ.get("CKEDITOR_BASEPATH")
CKEDITOR_UPLOAD_PATH = os.environ.get("CKEDITOR_UPLOAD_PATH")
CKEDITOR_IMAGE_BACKEND = "pillow"

# CKEDITOR custom fonts
CKEDITOR_FONT_LIST = "Arial; B Nazanin; B koodak Bold; B Nasim Bold; vazirMatnRegular; vazirMatnBold; vazirMatnExtraBold;"

# CKEDITOR CONFIGS
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar_Custom": [
            {
                "name": "document",
                "items": [
                    "Source",
                    "-",
                    "Save",
                    "NewPage",
                    "Preview",
                    "Print",
                    "-",
                    "Templates",
                ],
            },
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "PasteText",
                    "PasteFromWord",
                    "-",
                    "Undo",
                    "Redo",
                ],
            },
            {"name": "editing", "items": ["Find", "Replace", "-", "SelectAll"]},
            {
                "name": "forms",
                "items": [
                    "Form",
                    "Checkbox",
                    "Radio",
                    "TextField",
                    "Textarea",
                    "Select",
                    "Button",
                    "ImageButton",
                    "HiddenField",
                ],
            },
            "/",
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "CreateDiv",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                    "-",
                    "BidiLtr",
                    "BidiRtl",
                    "Language",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            {
                "name": "insert",
                "items": [
                    "Image",
                    "Youtube",
                    "Flash",
                    "Table",
                    "HorizontalRule",
                    "Smiley",
                    "SpecialChar",
                    "PageBreak",
                    "Iframe",
                ],
            },
            "/",
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "tools", "items": ["Maximize", "ShowBlocks"]},
            {"name": "about", "items": ["CodeSnippet"]},
            {"name": "about", "items": ["About"]},
            "/",  # put this to force next toolbar on new line
            {
                "name": "yourcustomtools",
                "items": [
                    # put the name of your editor.ui.addButton here
                    "Preview",
                    "Maximize",
                ],
            },
        ],
        "font_names": CKEDITOR_FONT_LIST,
        "toolbar": "Custom",  # put selected toolbar config here
        "toolbarGroups": [
            {"name": "document", "groups": ["mode", "document", "doctools"]}
        ],
        "height": 400,
        # 'width': '100%',
        "filebrowserWindowHeight": 725,
        "filebrowserWindowWidth": 940,
        "toolbarCanCollapse": True,
        "mathJaxLib": "//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML",
        "tabSpaces": 4,
        "extraPlugins": ",".join(
            [
                "uploadimage",  # the upload image feature
                # your extra plugins here
                "div",
                "autolink",
                "autoembed",
                "embedsemantic",
                "autogrow",
                "devtools",
                "widget",
                "lineutils",
                "clipboard",
                "dialog",
                "dialogui",
                "elementspath",
                "codesnippet",
            ]
        ),
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = os.environ.get("DEFAULT_AUTO_FIELD")
#
# INTERNAL_IPS = [
#     # ...
#     "127.0.0.1",
#     # ...
# ]
#
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.history.HistoryPanel',
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
#     'debug_toolbar.panels.profiling.ProfilingPanel',
# ]
#
# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK" : lambda request: True,
#     'INTERCEPT_REDIRECTS': False,
#     'DISABLE_PANELS': [
#         'debug_toolbar.panels.redirects.RedirectsPanel',
#     ],
#     'SHOW_TEMPLATE_CONTEXT': True,
# }


mimetypes.add_type("application/javascript", ".js", True)
