""" Reusable utility methods for management commands.
"""

import csv
from django.contrib.sites.models import Site
from templated_emails.utils import send_templated_email
from core.models import CshcUser

def send_welcome_email_to_user(reg_profile, password, sim):
    """ Sends a welcome email to the user (after they've just registered).

        Welcome email will include the activation link the user will need to
        click on to activate their account (and verify their email address).
    """
    context = {
        'activation_key': reg_profile.activation_key,
        'first_name': reg_profile.user.first_name,
        'last_name': reg_profile.user.last_name,
        'email': reg_profile.user.email,
        'password': password,
        'base_url': "//" + Site.objects.all()[0].domain
    }
    print 'Emailing {}'.format(reg_profile.user.get_full_name())
    if not sim:
        send_templated_email([reg_profile.user.email], 'emails/account_created', context)


def create_password(user, sim):
    """ Creates a new password for a user.
    """
    # Generate a random password
    password = CshcUser.objects.make_random_password(length=6)
    # Save the password for the user
    print "Saving new password '{}' for {}".format(password, user.get_full_name())
    user.set_password(password)
    if not sim:
        user.save()
    return password


def import_csv_data(file_path, cls):
    """ Generic helper method to import data from a CSV file.

        Returns an array of objects of type cls (supplied as an argument).
    """
    results = []
    with open(file_path, 'rb') as source_file:
        reader = csv.reader(source_file)
        first_row = True
        for csv_row in reader:
            # Ignore the first row (field names)
            if first_row:
                first_row = False
                continue
            res = cls(csv_row)
            results.append(res)

    return results
