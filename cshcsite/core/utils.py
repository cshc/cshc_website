""" Resuable utilities
"""

from django.conf import settings

def get_absolute_static_url(request):
    """ Returns the absolute URL for settings.STATIC_URL.

        This is useful because the thumbnail template tag doesn't
        support relative urls. In our case we know if we're not in
        DEBUG mode STATIC_URL is absolute anyway (Amazon S3). If we
        are in DEBUG mode we need to convert the relative static url
        to an absolute url using the request.build_absolute_uri()
        utility method.
    """
    static_url = settings.STATIC_URL
    if settings.DEBUG:
        static_url = request.build_absolute_uri(static_url)
    return static_url


SUFFIXES = {1: 'st', 2: 'nd', 3: 'rd'}

def ordinal(num):
    """ Returns the ordinal string from a number.

        Ref: http://codereview.stackexchange.com/a/41301
    """
    # Check for 10-20 because those are the digits that
    # don't follow the normal counting scheme.
    if 10 <= num % 100 <= 20:
        suffix = 'th'
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, 'th')
    return str(num) + suffix
