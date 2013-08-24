from django.contrib.sites.models import Site
from templated_emails.utils import send_templated_email
from core.models import CshcUser

def email_user(user, password, sim):
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': password,
        'base_url': "http://" + Site.objects.all()[0].domain
    }
    print 'Emailing {}:'.format(user.get_full_name())
    if not sim:
        send_templated_email([user.email], 'emails/account_created', context)


def create_password(user, sim):
    # Generate a random password
    password = CshcUser.objects.make_random_password(length=6)
    # Save the password for the user
    print "Saving new password '{}' for {}".format(password, user.get_full_name())
    user.set_password(password)
    if not sim:
        user.save()
    return password
