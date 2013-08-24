#!/usr/bin/env python
# -*-encoding: utf-8-*-
import traceback
from django.core.management.base import BaseCommand
from django.template import loader, Context
from django.contrib.sites.models import Site
from optparse import make_option
from core.models import CshcUser

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually save the password and email the users)'),
    )
    help = 'Initializes each user that doesn\'t have a password set. A random password is ' + \
           'generated and an email is sent to the user with their password.'

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except:
            traceback.print_exc()

    def _handle(self, *args, **options):
        sim = options['simulate']
        if sim:
            print "#### SIMULATION ONLY ####"

        # Get all users that don't have a password set.
        users = filter(lambda u: not u.has_usable_password(), CshcUser.objects.all())

        # For each user
        for u in users:
            # Generate a random password
            password = CshcUser.objects.make_random_password(length=6)
            # Save the password for the user
            print "Saving new password '{}' for {}".format(password, u.get_full_name())
            u.set_password(password)
            if not sim:
            	u.save()
            # Email the user with their new password
            self.email_user(u, password, sim)

    def email_user(self, user, password, sim):
        t = loader.get_template('core/account_created_email.txt')
        c = Context({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': password,
            'base_url': "http://" + Site.objects.all()[0].domain
        })

        subject = "Your new Cambridge South Hockey Club website account"

        message = t.render(c)
        print 'Emailing {}:'.format(user.get_full_name())
        print '\tSubject: ' + subject
        print '\tMessage: ' + message
        if not sim:
            user.email_user(subject, message)

