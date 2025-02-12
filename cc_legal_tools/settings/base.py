"""
Django settings for CC-Legal-Tools project.
"""

# Standard library
import copy
import mimetypes
import os

# Third-party
import colorlog  # noqa: F401
from django.conf.locale import LANG_INFO

# Paths #######################################################################
# SETTINGS_DIR is where this settings file is
SETTINGS_DIR = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
# DJANGO_ROOT is the directory under root that contains the settings directory,
#             urls.py, and other global stuff.
DJANGO_ROOT = os.path.dirname(SETTINGS_DIR)
# PROJECT_ROOT is the top directory under source control
PROJECT_ROOT = os.path.dirname(DJANGO_ROOT)
# Location of the data repository directory.
# Look in environment for DATA_REPOSITORY_DIR. Default is next to this one.
DATA_REPOSITORY_DIR = os.path.abspath(
    os.path.realpath(
        os.getenv(
            "DATA_REPOSITORY_DIR",
            os.path.join(PROJECT_ROOT, "..", "cc-legal-tools-data"),
        )
    )
)
DISTILL_DIR = os.path.abspath(
    os.path.realpath(os.path.join(DATA_REPOSITORY_DIR, "docs"))
)
LEGACY_DIR = os.path.abspath(
    os.path.realpath(os.path.join(DATA_REPOSITORY_DIR, "legacy"))
)
# Localication paths
DEEDS_UX_LOCALE_PATH = os.path.abspath(
    os.path.realpath(os.path.join(DATA_REPOSITORY_DIR, "locale"))
)
LEGAL_CODE_LOCALE_PATH = os.path.abspath(
    os.path.realpath(os.path.join(DATA_REPOSITORY_DIR, "legalcode"))
)
LOCALE_PATHS = (
    DEEDS_UX_LOCALE_PATH,
    LEGAL_CODE_LOCALE_PATH,
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath(
    os.path.realpath(os.path.join(PROJECT_ROOT, "tmp", "public", "static"))
)
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "static/"
# Additional locations of static files
STATICFILES_DIRS = (
    os.path.abspath(os.path.realpath(os.path.join(DJANGO_ROOT, "static"))),
)


# Application definition ######################################################
CANONICAL_SITE = "https://creativecommons.org"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "i18n",
    "legal_tools",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cc_legal_tools.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_ROOT, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                # django.contrib.messages.context_processors.messages must be
                # enabled in order to use the admin application
                "django.contrib.messages.context_processors.messages",
                "dealer.contrib.django.context_processor",
            ],
        },
    },
]

# The caching API is used, but there are no caching MIDDLEWARE, above, as we
# are not using site caching (which adds overhead without benefit for our uses)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 600,
        "OPTIONS": {"CULL_FREQUENCY": 0, "MAX_ENTRIES": 3000},
    },
}

WSGI_APPLICATION = "cc_legal_tools.wsgi.application"

mimetypes.add_type("application/rdf+xml", ".rdf", True)


# Database ####################################################################
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(PROJECT_ROOT, "db.sqlite3"),
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "tmp", "public", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# https://docs.djangoproject.com/en/4.2/topics/logging/
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
    },
    "formatters": {
        "basic": {
            "format": "%(levelname)s %(asctime)s %(name)s: %(message)s",
        },
        "format_mgmt": {
            # https://github.com/borntyping/python-colorlog
            "()": "colorlog.ColoredFormatter",
            "datefmt": "%H:%M:%S",
            "format": (
                "%(log_color)s%(levelname).4s %(asctime)s%(reset)s"
                " %(message)s"
            ),
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "basic",
        },
        "handle_mgmt": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "format_mgmt",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "i18n.management.commands": {
            "handlers": ["handle_mgmt"],
            "level": "DEBUG",
            "propagate": False,
        },
        "legal_tools.management.commands": {
            "handlers": ["handle_mgmt"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": [
            "console",
        ],
        "level": "WARNING",
    },
}


# Internationalization ########################################################
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# Language code for this installation.
LANGUAGE_CODE = "en"  # "en" matches our default language code in Transifex

DEEDS_UX_RESOURCE_NAME = "Deeds & UX"
DEEDS_UX_RESOURCE_SLUG = "deeds_ux"

# Percent translated that languages should be at or above
TRANSLATION_THRESHOLD = 60

TRANSIFEX = {
    "API_TOKEN": os.getenv("TRANSIFEX_API_TOKEN", "[!] MISSING [!]"),
    "ORGANIZATION_SLUG": "creativecommons",
    "DEEDS_UX_TEAM_ID": 11342,
    "DEEDS_UX_PROJECT_SLUG": "CC",
    "DEEDS_UX_RESOURCE_SLUGS": [DEEDS_UX_RESOURCE_SLUG],
    "LEGAL_CODE_PROJECT_SLUG": "cc-legal-code",
    "LEGAL_CODE_TEAM_ID": 153501,
    "LEGAL_CODE_RESOURCE_SLUGS": [
        "by-nc-nd_40",
        "by-nc-sa_40",
        "by-nc_40",
        "by-nd_40",
        "by-sa_40",
        "by_40",
        "zero_10",
    ],
}


# Preserve Django language information
# - This is used for translation/internationalization troubleshooting
# - The following line MUST come before any modifications of LANG_INFO
DJANGO_LANG_INFO = copy.deepcopy(LANG_INFO)


# Teach Django about a few more languages (sorted by language code)

# Azerbaijani (Django defaults to RTL?!?)
LANG_INFO["az"]["bidi"] = False

# Aragonese (Babel / CLDR 42 does not contain locale information)
LANG_INFO["an"] = {
    "bidi": False,
    "code": "an",
    "name": "Aragonese",
    "name_local": "aragonés",
}
# Maori
LANG_INFO["mi"] = {"code": "mi"}  # Remaining data from Babel
# Malay
LANG_INFO["ms"] = {"code": "ms"}  # Remaining data from Babel
# Maltese
LANG_INFO["mt"] = {"code": "mt"}  # Remaining data from Babel
# Northern Sotho (Babel / CLDR 42 does not contain locale information)
LANG_INFO["nso"] = {
    "bidi": False,
    "code": "nso",
    "name": "Northern Sotho",
    "name_local": "Sesotho sa Leboa",
}
# Aranese (Babel / CLDR 42 includes oc-ES [Occitan (Spain)] but not oc-Aranes)
LANG_INFO["oc-aranes"] = {
    "bidi": False,
    "code": "oc-aranes",
    "name": "Aranese",
    "name_local": "aranés",
}
# Sinhala (Sri Lanka)
LANG_INFO["si-lk"] = {"code": "si-lk"}  # Remaining data from Babel
# Zulu
LANG_INFO["zu"] = {"code": "zu"}  # Remaining data from Babel


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "Etc/UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# https://docs.djangoproject.com/en/4.2/topics/auth/passwords/#password-validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth."
            "password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth."
            "password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth."
            "password_validation.NumericPasswordValidator"
        ),
    },
]

# Make things more secure by default. Run "python manage.py check --deploy"
# for even more suggestions that you might want to add to the settings,
# depending on how the site uses SSL.
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

# The git branch where the official, approved, used in production translations
# are.
OFFICIAL_GIT_BRANCH = "main"

# Path to private keyfile to use when pushing up to data repo
TRANSLATION_REPOSITORY_DEPLOY_KEY = os.getenv(
    "TRANSLATION_REPOSITORY_DEPLOY_KEY", ""
)
