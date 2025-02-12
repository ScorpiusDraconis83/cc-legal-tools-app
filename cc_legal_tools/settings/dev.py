# This application is expected to *always* be run in a dev context. This file
# is exists to both make it easier to allow that to change in the future and to
# help organize the settings.
#
# Additionally, this settings file is used by ephemeral deployments (ex. GitHub
# Actions).

# Standard library
import sys

# Third-party
from django.core.management.utils import get_random_secret_key

# First-party/Local
from cc_legal_tools.settings.base import *  # noqa: F403

ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]"]
INTERNAL_IPS = ALLOWED_HOSTS

#: Don't send emails, just print them on stdout
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-SECRET_KEY
# As this app is used in a ephemeral manner (only run for development and to
# publish static files), a rotating secret key works well.
SECRET_KEY = get_random_secret_key()

# Enable tools like Firefox Web Developer: View Responsive Layouts
MIDDLEWARE.remove(  # noqa: F405
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
)

# Make it obvious if there are unresolved variables in templates
#
# cc-legal-tools-data: .github/workflows/checks.yml contains a check for the
# string "INVALID_VARIABLE" to ensure it isn't sent to production.
new_value = "INVALID_VARIABLE(%s)"
TEMPLATES[0]["OPTIONS"]["string_if_invalid"] = new_value  # noqa: F405

if (
    "dumpdata" not in sys.argv
    and "loaddata" not in sys.argv
    and "publish" not in sys.argv
    and "test" not in sys.argv
):
    # 1) "dumpdata": avoid the Django Debug Toolbar when dumping data
    # 2) "loaddata": avoid the Django Debug Toolbar when loading data
    # 3) "publish": avoid debug output in published files
    # 4) "test": the Django Debug Toolbar can't be used with tests:
    #      HINT: Django changes the DEBUG setting to False when running tests.
    #      By default the Django Debug Toolbar is installed because DEBUG is
    #      set to True. For most cases, you need to avoid installing the
    #      toolbar when running tests. If you feel this check is in error, you
    #      can set DEBUG_TOOLBAR_CONFIG['IS_RUNNING_TESTS'] = False to bypass
    #      this check.
    DEBUG = True
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}
    INSTALLED_APPS += [  # noqa: F405
        "debug_toolbar",
    ]
    MIDDLEWARE += [  # noqa: F405
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
