from .base import INSTALLED_APPS, TAGGIT

INSTALLED_APPS += [
    'taggit',
    'taggit_autosuggest',
]
TAGGIT_CASE_INSENSITIVE = True

# Because the behavior when True is set leads
# to situations where slugs
# can be entirely stripped to an empty string,
# we recommend not activating this.
# TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True

TAGGIT = True
