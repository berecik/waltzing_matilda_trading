from .base import INSTALLED_APPS, MIDDLEWARE, TEMPLATES

DJANGO_CMS = True

### Django CMS ###
# https://docs.django-cms.org/en/latest/introduction/01-install.html

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

CMS_ADMIN_APPS = [
    'djangocms_admin_style',
]

CMS_APPS = [
    # Django CMS
    'cms',
    'menus',
    'treebeard',
    # Django Sekizai is required by the CMS for static files management.
    'sekizai',
    'filer',
    'easy_thumbnails',
    'mptt',
]

CMS_PLUGINS_APPS = [
    'djangocms_link',
    'djangocms_file',
    'djangocms_picture',
    'djangocms_video',
    'djangocms_googlemap',
    'djangocms_snippet',
    'djangocms_style',
    'djangocms_text_ckeditor',
]

INSTALLED_APPS += CMS_APPS
INSTALLED_APPS += CMS_PLUGINS_APPS

MIDDLEWARE += [
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

CMS_TEMPLATES = [
    ('home.html', 'Home page template'),
]

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'sekizai.context_processors.sekizai',
    'cms.context_processors.cms_settings',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'
