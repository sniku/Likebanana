# Django settings for likebanana project.
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media/")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2-e+@%-_=$ixfy&9@_epzj!%p#h(=b77-89$(27#l1f==b+&oj'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'likebanana.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = (
    'templatetags',
    'likebanana.bananadeployer',
)

WEB_URL = 'http://127.0.0.1/' # URL to your site (preferably internal, especially if you are behind load balancer)

BANANALOG = '/var/log/likebanana.log'

SERVERS = {
    'web': (
        # first web server is treated as default one.

        # name      # server IP          # SSH user      # path to git directory with code              # your production banch # SSH key authorised by server (no passphase)
        ('web01', {'host': '127.0.0.1', 'user': 'root', 'path': '/home/snik/workspaces/getanewsletter', 'branch_name': 'staging', 'ssh_key':'/root/.ssh/key_main_no_passphase'}),
    )
}