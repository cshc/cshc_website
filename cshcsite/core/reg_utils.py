import hashlib
import random
from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings
from django.contrib.sites.models import Site
from registration.models import RegistrationProfile
from templated_emails.utils import send_templated_email


# Copied + modified from registration.models.RegistrationManager
def create_profile(user, simulate=False):
    """
    Create a ``RegistrationProfile`` for a given
    ``User``, and return the ``RegistrationProfile``.

    The activation key for the ``RegistrationProfile`` will be a
    SHA1 hash, generated from a combination of the ``User``'s
    username and a random salt.

    """
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    email = user.email
    if isinstance(email, unicode):
        email = email.encode('utf-8')
    activation_key = hashlib.sha1(salt+email).hexdigest()
    if simulate:
        return RegistrationProfile(user=user,
                       activation_key=activation_key)
    else:
        return RegistrationProfile.objects.create(user=user,
                       activation_key=activation_key)

# Copied + modified from registration.models.RegistrationManager
@transaction.commit_on_success
def create_inactive_user(email, password, first_name, last_name,
                         site, send_email=True):
    """
    Create a new, inactive ``User``, generate a
    ``RegistrationProfile`` and email its activation key to the
    ``User``, returning the new ``User``.

    By default, an activation email will be sent to the new
    user. To disable this, pass ``send_email=False``.

    """
    new_user = get_user_model().objects.create_user(email, password)
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.is_active = False
    new_user.save()

    registration_profile = create_profile(new_user)

    if send_email:
        send_activation_email(registration_profile, site)

    return new_user

def send_activation_email(registration_profile, site):
    """
    Send an activation email to the user associated with this
    ``RegistrationProfile``.

    The activation email will make use of two templates:

    ``emails/activation/short.txt``
        This template will be used for the subject line of the
        email. Because it is used as the subject line of an email,
        this template's output **must** be only a single line of
        text; output longer than one line will be forcibly joined
        into only a single line.

    ``emails/activation/email.txt`` / ``emails/activation/email.html``
        This template will be used for the body of the email. Text and
        HTML versions will be provided.

    These templates will each receive the following context
    variables:

    ``activation_key``
        The activation key for the new account.

    ``expiration_days``
        The number of days remaining during which the account may
        be activated.

    ``site``
        An object representing the site on which the user
        registered; depending on whether ``django.contrib.sites``
        is installed, this may be an instance of either
        ``django.contrib.sites.models.Site`` (if the sites
        application is installed) or
        ``django.contrib.sites.models.RequestSite`` (if
        not). Consult the documentation for the Django sites
        framework for details regarding these objects' interfaces.

    """
    context = {'activation_key': registration_profile.activation_key,
               'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
               'site': site,
               'user': registration_profile.user,
               'base_url': "http://" + Site.objects.all()[0].domain}

    send_templated_email([registration_profile.user.email], 'emails/activation', context)